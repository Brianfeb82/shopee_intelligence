# Shopee Thailand Intelligence System 🛍️🚀

An end-to-end data science project for analyzing customer journeys, predicting churn, and optimizing marketing campaigns for Shopee Thailand.

## 🌟 Key Features
- **Exploratory Data Analysis**: Visualizing sales trends and product performance.
- **Conversion Funnel**: Tracking customer behavior from discovery to purchase.
- **Churn Prediction (XGBoost)**: 99%+ accuracy in identifying at-risk customers.
- **Campaign Optimization Engine**: Automated coupon allocation and targeting based on RFM segments.
- **Interactive Dashboard**: Built with Streamlit for real-time insight discovery.
- **Automated Notifications**: Simulated cross-channel messaging (Email & App Push).

## 🛠️ Tech Stack
- **Language**: Python 3.9+
- **Machine Learning**: XGBoost, Scikit-Learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Streamlit, Seaborn
- **Deployment**: Docker, Python-Dotenv

## 🚀 Quick Start
1. **Clone the repo**:
   ```bash
   git clone [your-repo-link]
   cd "Shoope Training"
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Dashboard**:
   ```bash
   streamlit run app.py
   ```

## 🐳 Docker Deployment
```bash
docker build -t shopee-intelligence .
docker run -p 8501:8501 shopee-intelligence
```

## 📂 Project Structure
- `app.py`: Main Streamlit Dashboard
- `churn_model_shopee.py`: Model training and feature engineering
- `campaign_engine.py`: Targeting and notification logic
- `outputs/`: Generated visualizations and model files
- `archive (1)/`: Dataset directory (excluded from Git)

---
Developed by [Your Name] | Powered by Shopee Thailand Data
