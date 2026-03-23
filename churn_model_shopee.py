import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os
import joblib

# Define paths
BASE_PATH = r"c:\Users\T14\Shoope Training\archive (1)"
OUTPUT_PATH = r"c:\Users\T14\Shoope Training\outputs"

def prepare_features():
    print("Preparing features...")
    orders = pd.read_csv(os.path.join(BASE_PATH, 'shopee_orders_thailand.csv'))
    reviews = pd.read_csv(os.path.join(BASE_PATH, 'shopee_reviews_thailand.csv'))
    sessions = pd.read_csv(os.path.join(BASE_PATH, 'shopee_website_sessions_thailand.csv'))
    customers = pd.read_csv(os.path.join(BASE_PATH, 'shopee_customers_thailand.csv'))
    order_items = pd.read_csv(os.path.join(BASE_PATH, 'shopee_order_items_thailand.csv'))

    # Convert dates
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    max_date = orders['order_date'].max()

    # 1. RFM Features
    rfm = orders.groupby('customer_id').agg({
        'order_date': lambda x: (max_date - x.max()).days,
        'order_id': 'count',
        'total_amount': 'sum'
    }).rename(columns={'order_date': 'recency', 'order_id': 'frequency', 'total_amount': 'monetary'})

    # 2. Target Variable (Churn = no order in last 60 days)
    rfm['is_churned'] = (rfm['recency'] > 60).astype(int)

    # 3. Tenure (Days since first order)
    tenure = orders.groupby('customer_id')['order_date'].min().apply(lambda x: (max_date - x).days)
    rfm['tenure'] = tenure

    # 4. Sentiment Features
    pos_keywords = ['helpful', 'perfect', 'good', 'excellent', 'amazing']
    reviews['is_positive'] = reviews['review_text'].str.contains('|'.join(pos_keywords), case=False, na=False).astype(int)
    
    # Link reviews to customers via orders
    # order_items has order_id, order_id has customer_id
    reviews_with_cust = reviews.merge(order_items[['order_item_id', 'order_id']], on='order_item_id')
    reviews_with_cust = reviews_with_cust.merge(orders[['order_id', 'customer_id']], on='order_id')
    
    cust_sentiment = reviews_with_cust.groupby('customer_id')['is_positive'].mean().rename('avg_sentiment')
    rfm = rfm.join(cust_sentiment, how='left').fillna({'avg_sentiment': 0.5}) # Default neutral

    # 5. Session Features
    session_counts = sessions.groupby('user_id')['session_id'].count().rename('session_frequency')
    rfm = rfm.join(session_counts, how='left').fillna({'session_frequency': 0})

    # 6. Demographic Features
    customers = customers.rename(columns={'customer_id': 'user_id'}) # Match session user_id
    customers = customers.set_index('user_id')
    rfm = rfm.join(customers[['gender', 'province']], how='left')
    
    # Handle categoricals
    rfm['gender'] = rfm['gender'].map({'Male': 0, 'Female': 1}).fillna(-1)
    rfm = pd.get_dummies(rfm, columns=['province'], drop_first=True)

    return rfm

def train_model(df):
    print("Training XGBoost model...")
    X = df.drop(['is_churned'], axis=1)
    y = df['is_churned']
    
    # Ensure all columns are numeric
    X = X.select_dtypes(include=[np.number])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        objective='binary:logistic',
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print("\nModel Evaluation:")
    print(classification_report(y_test, y_pred))
    
    # Feature Importance
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    print("\nTop 10 Important Features:")
    print(importance.head(10))
    
    # Save model
    joblib.dump(model, os.path.join(OUTPUT_PATH, 'churn_model_shopee.pkl'))
    joblib.dump(X.columns.tolist(), os.path.join(OUTPUT_PATH, 'model_features.pkl'))
    print(f"Model saved to {OUTPUT_PATH}")

def main():
    try:
        data = prepare_features()
        train_model(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
