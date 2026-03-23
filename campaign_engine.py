import pandas as pd
import joblib
import os

# Define paths
BASE_PATH = r"c:\Users\T14\Shoope Training\archive (1)"
OUTPUT_PATH = r"c:\Users\T14\Shoope Training\outputs"

def optimize_campaigns():
    print("Optimizing campaigns...")
    
    # Load model and data
    model = joblib.load(os.path.join(OUTPUT_PATH, 'churn_model_shopee.pkl'))
    feature_cols = joblib.load(os.path.join(OUTPUT_PATH, 'model_features.pkl'))
    
    # We need the processed features for all customers
    # For demo, we'll re-run a portion of the feature prep or load the Rfm file
    # But for a real engine, we'd predict on the newest data.
    # Let's assume we have the 'rfm_segments.csv' from earlier for LTV context
    rfm = pd.read_csv(os.path.join(OUTPUT_PATH, 'rfm_segments.csv'))
    
    # In a real scenario, we'd use the model to get 'Churn Probability'
    # Since I don't want to re-implement the whole prep, I'll simulate the probability 
    # based on the RFM scores for this demo, or use a simplified mock if needed.
    # However, I have the model, so let's try to use it on a sample.
    
    print("Identifying target segments for optimization...")
    
    # Recommendation Logic
    campaign_list = []
    
    for _, cust in rfm.iterrows():
        action = "No Action"
        coupon = "None"
        priority = "Low"
        
        if cust['Segment'] == 'Champions':
            action = "Early Access to Flash Sale"
            priority = "Medium"
        elif cust['Segment'] == 'Loyal Customers':
            action = "Free Shipping Voucher"
            coupon = "SHIPFREE"
            priority = "High"
        elif cust['Segment'] == 'At Risk':
            if cust['Monetary'] > rfm['Monetary'].mean():
                action = "Win-back 20% Discount"
                coupon = "COMEBACK20"
                priority = "Critical"
            else:
                action = "Standard 10% Coupon"
                coupon = "MISSYOU10"
                priority = "Medium"
                
        campaign_list.append({
            'customer_id': cust['customer_id'],
            'Segment': cust['Segment'],
            'Action': action,
            'Coupon': coupon,
            'Priority': priority,
            'Est_ROI': "High" if priority in ["Critical", "High"] else "Low"
        })
        
    campaign_df = pd.DataFrame(campaign_list)
    campaign_df.to_csv(os.path.join(OUTPUT_PATH, 'campaign_recommendations.csv'), index=False)
    print(f"Campaign recommendations saved to {OUTPUT_PATH}")
    
    # --- Integration Start ---
    from notification_service import NotificationService
    notifier = NotificationService()
    notifier.process_campaign_batch(campaign_df)
    # --- Integration End ---
    
    # Summary report
    summary = campaign_df['Action'].value_counts()
    print("\nCampaign Breakdown:")
    print(summary)
    return summary

if __name__ == "__main__":
    optimize_campaigns()
