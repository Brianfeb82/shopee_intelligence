import time
import random

class NotificationService:
    def __init__(self):
        self.channels = ['Email', 'Push', 'SMS']
        print("Notification Service Initialized.")

    def send_notification(self, customer_id, channel, message):
        """Simulates sending a notification."""
        # Simulated delay to mimic API call
        time.sleep(0.01) 
        status = "SENT" if random.random() > 0.05 else "FAILED"
        print(f"[{status}] Channel: {channel} | ID: {customer_id} | Msg: {message[:50]}...")
        return status

    def process_campaign_batch(self, campaign_df):
        print(f"\nProcessing batch of {len(campaign_df)} notifications...")
        results = []
        
        # We only notify for specific actions to avoid over-sampling in this demo
        targets = campaign_df[campaign_df['Action'] != 'No Action'].head(20) # Limit to 20 for log visibility
        
        for _, row in targets.iterrows():
            channel = 'Email' if 'Win-back' in row['Action'] else 'Push'
            msg = f"Hi {row['customer_id']}! {row['Action']}. Use code {row['Coupon']}."
            status = self.send_notification(row['customer_id'], channel, msg)
            results.append(status)
            
        print(f"Batch processing complete. Success rate: {results.count('SENT')/len(results)*100:.1f}%")
        return results

if __name__ == "__main__":
    # Test run
    service = NotificationService()
    service.send_notification("C12345", "Email", "Welcome back! Here is 20% off.")
