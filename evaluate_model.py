import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report
from churn_model_shopee import prepare_features # Reuse the prep function

# Define paths
OUTPUT_PATH = r"c:\Users\T14\Shoope Training\outputs"

def evaluate():
    print("Loading model and data for evaluation...")
    model = joblib.load(os.path.join(OUTPUT_PATH, 'churn_model_shopee.pkl'))
    feature_cols = joblib.load(os.path.join(OUTPUT_PATH, 'model_features.pkl'))
    
    # Get the data
    df = prepare_features()
    X = df[feature_cols]
    y = df['is_churned']
    
    # Predict
    y_pred = model.predict(X)
    y_prob = model.predict_proba(X)[:, 1]
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Churn', 'Churn'], yticklabels=['Not Churn', 'Churn'])
    plt.title('Confusion Matrix - Churn Prediction')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig(os.path.join(OUTPUT_PATH, 'confusion_matrix.png'))
    plt.close()
    
    # 2. ROC Curve
    fpr, tpr, _ = roc_curve(y, y_prob)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(OUTPUT_PATH, 'roc_curve.png'))
    plt.close()
    
    # 3. Save Summary
    report = classification_report(y, y_pred)
    with open(os.path.join(OUTPUT_PATH, 'performance_metrics.txt'), 'w') as f:
        f.write("--- Classification Report ---\n")
        f.write(report)
        f.write(f"\nROC AUC Score: {roc_auc:.4f}")
        
    print(f"Evaluation complete! Images saved in {OUTPUT_PATH}")

if __name__ == "__main__":
    evaluate()
