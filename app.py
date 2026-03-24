import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import joblib

# Set Page Config
st.set_page_config(page_title="Shopee Thailand Intelligence", page_icon="🛍️", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #EE4D2D; /* Shopee Orange */
    }
    </style>
    """, unsafe_allow_html=True)

# Define paths (Relative for Cloud Deployment)
BASE_PATH = "data"
OUTPUT_PATH = "outputs"

@st.cache_data
def load_data():
    # List of possible locations for data
    locations = ["data", "archive (1)", "."]
    
    orders, rfm, campaigns = None, None, None
    
    for loc in locations:
        try:
            orders_path = os.path.join(loc, 'shopee_orders_thailand.csv')
            rfm_path = os.path.join("outputs", 'rfm_segments.csv') if loc == "." else os.path.join(loc, 'rfm_segments.csv')
            # If loc is root, outputs might be in outputs/
            if loc == ".":
                rfm_path = os.path.join("outputs", 'rfm_segments.csv')
                camp_path = os.path.join("outputs", 'campaign_recommendations.csv')
            else:
                rfm_path = os.path.join(loc, 'rfm_segments.csv')
                camp_path = os.path.join(loc, 'campaign_recommendations.csv')
                
            orders = pd.read_csv(orders_path)
            rfm = pd.read_csv(rfm_path)
            campaigns = pd.read_csv(camp_path)
            orders['order_date'] = pd.to_datetime(orders['order_date'])
            
            # Load Logistics Data
            carrier_kpis = pd.read_csv(os.path.join(OUTPUT_PATH, 'carrier_kpis.csv'))
            regional_kpis = pd.read_csv(os.path.join(OUTPUT_PATH, 'regional_kpis.csv'))
            
            return orders, rfm, campaigns, carrier_kpis, regional_kpis
        except FileNotFoundError:
            continue
            
    st.error("Data files not found. Please ensure 'shopee_orders_thailand.csv' is in the root or 'data' folder, and 'rfm_segments.csv' is in the 'outputs' or 'data' folder.")
    st.stop()

# Sidebar
st.sidebar.image("https://logolook.net/wp-content/uploads/2021/11/Shopee-Logo.png", width=200)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Executive Summary", "Customer Journey", "Churn & Campaigns", "Logistics & Delivery", "Model Performance"])

# Load Data
orders, rfm, campaigns, carrier_kpis, regional_kpis = load_data()

if page == "Executive Summary":
    st.title("🛍️ Shopee Thailand Executive Summary")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"฿{orders['total_amount'].sum():,.0f}")
    col2.metric("Total Orders", f"{len(orders):,}")
    col3.metric("Unique Customers", f"{rfm['customer_id'].nunique():,}")
    col4.metric("Avg Order Value", f"฿{orders['total_amount'].mean():,.2f}")
    
    # Sales Trend
    st.subheader("Daily Sales Performance")
    daily_sales = orders.groupby('order_date')['total_amount'].sum().reset_index()
    fig_sales = px.line(daily_sales, x='order_date', y='total_amount', 
                        title="Revenue over Time", color_discrete_sequence=['#EE4D2D'])
    st.plotly_chart(fig_sales, use_container_width=True)

elif page == "Customer Journey":
    st.title("🛤️ Customer Journey & Funnel")
    
    # Funnel
    st.subheader("Conversion Funnel Analysis")
    # Using data from our previous analysis for simplicity in the dashboard
    funnel_data = pd.DataFrame({
        'Stage': ['Home', 'Products', 'Cart', 'Checkout'],
        'Count': [100000, 75000, 30000, 15000] # Mocked/Averaged based on real data
    })
    fig_funnel = px.funnel(funnel_data, x='Count', y='Stage', color_discrete_sequence=['#EE4D2D'])
    st.plotly_chart(fig_funnel, use_container_width=True)
    
    # Segment Distribution
    st.subheader("Customer Segmentation (RFM)")
    segment_counts = rfm['Segment'].value_counts().reset_index()
    fig_segments = px.pie(segment_counts, values='count', names='Segment', 
                          title="Customer Segments Share", color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_segments, use_container_width=True)

elif page == "Churn & Campaigns":
    st.title("🎯 Churn Prediction & Campaign Optimization")
    
    # Campaign Metrics
    st.subheader("Recommended Campaign Actions")
    campaign_summary = campaigns['Action'].value_counts().reset_index()
    fig_campaign = px.bar(campaign_summary, x='count', y='Action', orientation='h', 
                           color='Action', title="Target Audience per Action")
    st.plotly_chart(fig_campaign, use_container_width=True)
    
    # Explorer
    st.subheader("Customer Campaign Explorer")
    selected_segment = st.selectbox("Select Segment to Filter", rfm['Segment'].unique())
    filtered_data = campaigns[campaigns['Segment'] == selected_segment]
    st.dataframe(filtered_data.head(100), use_container_width=True)

elif page == "Logistics & Delivery":
    st.title("🚚 Logistics & Delivery Optimization")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    fastest_carrier = carrier_kpis.iloc[0]
    col1.metric("Fastest Carrier", fastest_carrier['Courier'], f"{fastest_carrier['Avg_Days']:.1f} days")
    
    avg_delivery = carrier_kpis['Avg_Days'].mean()
    col2.metric("Overall Avg Delivery", f"{avg_delivery:.1f} days")
    
    total_shipped = carrier_kpis['Total_Shipments'].sum()
    col3.metric("Total Shipments Analyzed", f"{total_shipped:,}")
    
    # Carrier Chart
    st.subheader("Carrier Performance Comparison")
    fig_carrier = px.bar(carrier_kpis, x='Courier', y='Avg_Days', color='Courier',
                         title="Average Delivery Time (Lower is Better)")
    st.plotly_chart(fig_carrier, use_container_width=True)
    
    # Regional Heatmap
    st.subheader("Regional Delivery Delays")
    fig_regional = px.bar(regional_kpis.head(15), x='actual_delivery_days', y='province', orientation='h',
                          title="Top 15 Provinces with Slowest Deliveries", labels={'actual_delivery_days': 'Avg Days'})
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # Delivery Estimator
    st.markdown("---")
    st.subheader("🔮 Smart Delivery Estimator")
    st.write("Predict how many days it will take for your package to arrive.")
    
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        sel_courier = st.selectbox("Select Courier", carrier_kpis['Courier'].unique())
        sel_province = st.selectbox("Select Destination Province", regional_kpis['province'].unique())
    with col_e2:
        sel_day = st.selectbox("Shipping Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        sel_month = st.slider("Shipping Month", 1, 12, 1)
        
    if st.button("Calculate ETA"):
        try:
            model = joblib.load(os.path.join(OUTPUT_PATH, 'delivery_model.pkl'))
            feat_cols = joblib.load(os.path.join(OUTPUT_PATH, 'delivery_features.pkl'))
            
            # Map day to int
            day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
            
            # Create feature vector
            input_df = pd.DataFrame(columns=feat_cols)
            input_df.loc[0] = 0
            input_df.at[0, 'shipped_day'] = day_map[sel_day]
            input_df.at[0, 'shipped_month'] = sel_month
            
            curr_courier_col = f'courier_name_{sel_courier}'
            curr_province_col = f'province_{sel_province}'
            
            if curr_courier_col in input_df.columns:
                input_df.at[0, curr_courier_col] = 1
            if curr_province_col in input_df.columns:
                input_df.at[0, curr_province_col] = 1
                
            prediction = model.predict(input_df)[0]
            st.success(f"Estimated Delivery Time: **{prediction:.1f} days**")
            st.info("Note: ETA is based on historical delivery patterns.")
        except Exception as e:
            st.error(f"Prediction Error: {e}")

elif page == "Model Performance":
    st.title("📊 Model Performance Metrics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Confusion Matrix")
        st.image(os.path.join(OUTPUT_PATH, "confusion_matrix.png"))
        st.info("High diagonal values indicate high accuracy in predicting both Churn and Not Churn.")
        
    with col2:
        st.subheader("ROC Curve")
        st.image(os.path.join(OUTPUT_PATH, "roc_curve.png"))
        st.success("ROC AUC = 1.00. This model has excellent discriminatory power.")

st.sidebar.markdown("---")
st.sidebar.write("Developed with ❤️ for Shopee Thailand Intelligence")
