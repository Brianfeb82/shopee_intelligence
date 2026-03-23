import pandas as pd
import os
from datetime import datetime

# Define paths
BASE_PATH = r"c:\Users\T14\Shoope Training\archive (1)"
OUTPUT_PATH = r"c:\Users\T14\Shoope Training\outputs"

def rfm_analysis():
    print("Starting RFM Analysis...")
    orders = pd.read_csv(os.path.join(BASE_PATH, 'shopee_orders_thailand.csv'))
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # Reference date (day after last order)
    ref_date = orders['order_date'].max() + pd.Timedelta(days=1)
    
    rfm = orders.groupby('customer_id').agg({
        'order_date': lambda x: (ref_date - x.max()).days, # Recency
        'order_id': 'count', # Frequency
        'total_amount': 'sum' # Monetary
    }).rename(columns={
        'order_date': 'Recency',
        'order_id': 'Frequency',
        'total_amount': 'Monetary'
    })
    
    # Scoring (1-5)
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    
    # Segments
    def segment_customer(df):
        if df['RFM_Score'] == '555':
            return 'Champions'
        elif df['R_Score'] >= 4:
            return 'Loyal Customers'
        elif df['R_Score'] <= 1:
            return 'At Risk'
        else:
            return 'Standard'
            
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    rfm.to_csv(os.path.join(OUTPUT_PATH, 'rfm_segments.csv'))
    print(f"RFM analysis saved to {OUTPUT_PATH}")
    return rfm['Segment'].value_counts()

def sentiment_summary():
    print("Analyzing Reviews...")
    reviews = pd.read_csv(os.path.join(BASE_PATH, 'shopee_reviews_thailand.csv'))
    # Basic keyword analysis for demo purposes
    pos_keywords = ['helpful', 'perfect', 'good', 'excellent', 'amazing']
    neg_keywords = ['broken', 'bad', 'slow', 'fragile', 'poor']
    
    reviews['Pos_Count'] = reviews['review_text'].str.count(f"(?i){'|'.join(pos_keywords)}")
    reviews['Neg_Count'] = reviews['review_text'].str.count(f"(?i){'|'.join(neg_keywords)}")
    
    summary = {
        'total_reviews': len(reviews),
        'positive_mentions': reviews['Pos_Count'].sum(),
        'negative_mentions': reviews['Neg_Count'].sum()
    }
    print(f"Sentiment summary: {summary}")
    return summary

def main():
    try:
        segments = rfm_analysis()
        sentiment = sentiment_summary()
        # Save a small text report
        with open(os.path.join(OUTPUT_PATH, 'analysis_summary.txt'), 'w') as f:
            f.write("--- RFM Segments ---\n")
            f.write(segments.to_string())
            f.write("\n\n--- Sentiment Summary ---\n")
            f.write(str(sentiment))
        print("Detailed analysis complete!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
