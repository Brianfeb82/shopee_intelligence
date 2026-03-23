import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set aesthetic style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Define paths
BASE_PATH = r"c:\Users\T14\Shoope Training\archive (1)"
OUTPUT_PATH = r"c:\Users\T14\Shoope Training\outputs"

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

def load_data():
    print("Loading datasets...")
    data = {
        'orders': pd.read_csv(os.path.join(BASE_PATH, 'shopee_orders_thailand.csv')),
        'customers': pd.read_csv(os.path.join(BASE_PATH, 'shopee_customers_thailand.csv')),
        'order_items': pd.read_csv(os.path.join(BASE_PATH, 'shopee_order_items_thailand.csv')),
        'products': pd.read_csv(os.path.join(BASE_PATH, 'shopee_products_thailand.csv')),
        'sessions': pd.read_csv(os.path.join(BASE_PATH, 'shopee_website_sessions_thailand.csv')),
        'activities': pd.read_csv(os.path.join(BASE_PATH, 'shopee_session_activities_thailand.csv'))
    }
    # Convert dates
    data['orders']['order_date'] = pd.to_datetime(data['orders']['order_date'])
    data['sessions']['session_date'] = pd.to_datetime(data['sessions']['session_date'])
    return data

def analyze_sales(data):
    print("Analyzing sales performance...")
    orders = data['orders']
    
    # Daily Sales Trend
    daily_sales = orders.groupby('order_date')['total_amount'].sum().reset_index()
    plt.figure()
    sns.lineplot(data=daily_sales, x='order_date', y='total_amount', marker='o', color='#EE4D2D') # Shopee Orange
    plt.title('Daily Sales Revenue (THB)')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, 'daily_sales_trend.png'))
    plt.close()

def analyze_funnel(data):
    print("Analyzing customer journey funnel...")
    activities = data['activities']
    sessions = data['sessions']
    
    # Activity mapping
    funnel_stages = {
        'Home': activities[activities['page_url'] == '/home']['session_id'].nunique(),
        'Products': activities[activities['page_url'] == '/products']['session_id'].nunique(),
        'Cart': activities[activities['page_url'] == '/cart']['session_id'].nunique(),
        'Checkout': activities[activities['page_url'] == '/checkout']['session_id'].nunique()
    }
    
    # Add Orders to funnel
    funnel_data = pd.DataFrame(list(funnel_stages.items()), columns=['Stage', 'Count'])
    
    plt.figure()
    sns.barplot(data=funnel_data, x='Stage', y='Count', palette='viridis')
    plt.title('Customer Journey Funnel (Session Counts)')
    plt.ylabel('Unique Sessions')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_PATH, 'funnel_analysis.png'))
    plt.close()

def main():
    try:
        data = load_data()
        analyze_sales(data)
        analyze_funnel(data)
        print(f"Analysis complete! Figures saved in: {OUTPUT_PATH}")
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    main()
