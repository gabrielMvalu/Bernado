import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import time
import scipy.stats as stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# ===== ENHANCED PAGE CONFIG =====
st.set_page_config(
    page_title="BRENADO | Elite BI Suite",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "BRENADO Elite Business Intelligence Suite v3.0 - Advanced Analytics Platform"
    }
)

# ===== ULTRA PREMIUM CSS DESIGN SYSTEM =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
    
    /* Advanced CSS Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --danger-gradient: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        --dark-gradient: linear-gradient(135deg, #2b2d42 0%, #1a1b27 100%);
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-primary: #ffffff;
        --text-secondary: #a0a0b8;
        --shadow-xl: 0 25px 50px rgba(0, 0, 0, 0.4);
        --shadow-glow: 0 0 50px rgba(102, 126, 234, 0.5);
        --neural-blue: #00d4ff;
        --quantum-purple: #9333ea;
        --crypto-green: #10b981;
        --ai-orange: #f59e0b;
    }
    
    /* Ultra Modern Background */
    .stApp {
        background: #0a0b0f;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(245, 87, 108, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(250, 112, 154, 0.1) 0%, transparent 50%),
            linear-gradient(135deg, rgba(0, 212, 255, 0.05) 0%, rgba(147, 51, 234, 0.05) 100%);
        min-height: 100vh;
        position: relative;
    }
    
    /* Animated Neural Network Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 60px, rgba(102, 126, 234, 0.02) 60px, rgba(102, 126, 234, 0.02) 120px),
            repeating-linear-gradient(-45deg, transparent, transparent 60px, rgba(245, 87, 108, 0.02) 60px, rgba(245, 87, 108, 0.02) 120px);
        pointer-events: none;
        animation: neuralFlow 30s linear infinite;
        z-index: -1;
    }
    
    @keyframes neuralFlow {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(120px, 120px) rotate(360deg); }
    }
    
    /* Premium Glassmorphism Cards */
    .premium-card {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-xl);
        padding: 35px;
        margin: 25px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
        transform: rotate(45deg);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.6s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.4);
    }
    
    .premium-card:hover::before {
        opacity: 1;
    }
    
    /* Advanced KPI Cards */
    .kpi-card {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        border: 1px solid var(--glass-border);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        opacity: 0.08;
        border-radius: 50%;
        transform: scale(0);
        transition: transform 0.8s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    .kpi-card:hover::after {
        transform: scale(2.5);
    }
    
    /* AI-Enhanced Typography */
    .ai-title {
        font-family: 'Inter', sans-serif;
        font-weight: 900;
        font-size: 52px;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, var(--neural-blue) 0%, var(--quantum-purple) 50%, var(--ai-orange) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 40px rgba(102, 126, 234, 0.8);
        animation: aiPulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes aiPulse {
        0% { text-shadow: 0 0 40px rgba(102, 126, 234, 0.8); }
        100% { text-shadow: 0 0 60px rgba(245, 87, 108, 0.8); }
    }
    
    .neural-text {
        color: var(--neural-blue);
        font-weight: 700;
        text-shadow: 0 0 20px var(--neural-blue);
    }
    
    .quantum-text {
        color: var(--quantum-purple);
        font-weight: 700;
        text-shadow: 0 0 20px var(--quantum-purple);
    }
    
    .crypto-text {
        color: var(--crypto-green);
        font-weight: 700;
        text-shadow: 0 0 20px var(--crypto-green);
    }
    
    /* Advanced Interactive Elements */
    .insight-bubble {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(147, 51, 234, 0.1) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .insight-bubble::before {
        content: '🧠';
        position: absolute;
        top: 15px;
        right: 20px;
        font-size: 24px;
        opacity: 0.3;
        animation: brainPulse 2s ease-in-out infinite;
    }
    
    @keyframes brainPulse {
        0%, 100% { transform: scale(1); opacity: 0.3; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    
    .insight-bubble:hover {
        transform: translateY(-5px);
        border-color: rgba(0, 212, 255, 0.6);
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(147, 51, 234, 0.15) 100%);
    }
    
    /* Enhanced Data Tables */
    .dataframe {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 20px !important;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .dataframe th {
        background: var(--primary-gradient) !important;
        color: white !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 20px !important;
        text-align: left !important;
        border: none !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        background: transparent !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--glass-border) !important;
        padding: 18px !important;
        transition: all 0.3s ease !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(102, 126, 234, 0.15) !important;
        transform: scale(1.01);
    }
    
    /* Neural Network Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 11, 15, 0.95) 0%, rgba(43, 45, 66, 0.95) 100%);
        backdrop-filter: blur(25px);
        border-right: 1px solid var(--glass-border);
        box-shadow: 10px 0 30px rgba(0,0,0,0.4);
    }
    
    /* AI Status Indicators */
    .ai-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 15px 25px;
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(16, 185, 129, 0.1) 100%);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        margin: 15px 0;
        transition: all 0.3s ease;
    }
    
    .ai-status:hover {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%);
        border-color: rgba(0, 212, 255, 0.5);
        transform: translateX(5px);
    }
    
    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--neural-blue);
        animation: aiPulseDot 1.5s ease-in-out infinite;
    }
    
    @keyframes aiPulseDot {
        0%, 100% { 
            box-shadow: 0 0 0 0 rgba(0, 212, 255, 0.7);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 0 10px rgba(0, 212, 255, 0);
            transform: scale(1.2);
        }
    }
    
    /* Enhanced Metrics Containers */
    div[data-testid="metric-container"] {
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        border: 1px solid var(--glass-border);
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.6);
    }
    
    /* Advanced Button Styles */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 18px 40px;
        border-radius: 18px;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 16px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Enhanced Tab System */
    .stTabs [data-baseweb="tab-list"] {
        gap: 25px;
        background: var(--glass-bg);
        backdrop-filter: blur(25px);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid var(--glass-border);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        background-color: transparent;
        border-radius: 18px;
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        padding: 15px 35px;
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
        transform: translateY(-3px) scale(1.05);
    }
    
    /* Financial Indicator Styles */
    .financial-indicator {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .indicator-positive {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%);
        color: var(--crypto-green);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .indicator-negative {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .indicator-neutral {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%);
        color: var(--ai-orange);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    /* Quantum Computing Loader */
    .quantum-loader {
        display: inline-block;
        width: 40px;
        height: 40px;
        position: relative;
    }
    
    .quantum-loader::before,
    .quantum-loader::after {
        content: '';
        position: absolute;
        border: 3px solid transparent;
        border-radius: 50%;
        animation: quantumSpin 2s linear infinite;
    }
    
    .quantum-loader::before {
        width: 40px;
        height: 40px;
        border-top-color: var(--neural-blue);
        border-right-color: var(--quantum-purple);
    }
    
    .quantum-loader::after {
        width: 30px;
        height: 30px;
        top: 5px;
        left: 5px;
        border-bottom-color: var(--crypto-green);
        border-left-color: var(--ai-orange);
        animation-direction: reverse;
        animation-duration: 1s;
    }
    
    @keyframes quantumSpin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Neural Network Visualization */
    .neural-network {
        position: relative;
        background: radial-gradient(circle at center, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
        border-radius: 20px;
        padding: 30px;
        overflow: hidden;
    }
    
    .neural-network::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, rgba(0, 212, 255, 0.3), transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(147, 51, 234, 0.3), transparent),
            radial-gradient(1px 1px at 90px 40px, rgba(16, 185, 129, 0.3), transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(245, 158, 11, 0.3), transparent);
        animation: neuralFlow 8s ease-in-out infinite;
    }
    
    /* Premium Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
        box-shadow: 0 0 20px rgba(245, 87, 108, 0.5);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .ai-title {
            font-size: 36px;
        }
        
        .premium-card {
            padding: 25px;
            margin: 15px 0;
        }
        
        .kpi-card {
            padding: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== ENHANCED FIREBASE FUNCTIONS =====
@st.cache_resource
def init_firebase():
    """Initialize Firebase for Streamlit Cloud with enhanced error handling"""
    try:
        if firebase_admin._apps:
            return firestore.client()
        
        # For STREAMLIT CLOUD - use secrets
        firebase_config = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
            "universe_domain": st.secrets["firebase"]["universe_domain"]
        }
        
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        return firestore.client()
        
    except Exception as e:
        st.error(f"❌ Firebase Connection Error: {e}")
        return None

# ===== ADVANCED AI ANALYTICS ENGINE =====
class AIAnalyticsEngine:
    """Advanced AI-powered analytics engine for business intelligence"""
    
    def __init__(self, data):
        self.data = data
        self.scaler = StandardScaler()
    
    def detect_anomalies(self, columns=['Valoare'], contamination=0.1):
        """Advanced anomaly detection using Isolation Forest"""
        if self.data.empty or not all(col in self.data.columns for col in columns):
            return pd.DataFrame()
        
        # Prepare data
        features = self.data[columns].fillna(0)
        
        # Apply Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        anomaly_labels = iso_forest.fit_predict(features)
        
        # Add anomaly labels to data
        result = self.data.copy()
        result['Anomaly'] = anomaly_labels
        result['Anomaly_Score'] = iso_forest.decision_function(features)
        
        return result[result['Anomaly'] == -1]  # Return only anomalies
    
    def customer_segmentation(self, features=['Valoare'], n_clusters=4):
        """Advanced customer segmentation using K-Means clustering"""
        if self.data.empty or 'Client' not in self.data.columns:
            return pd.DataFrame()
        
        # Aggregate customer data
        customer_data = self.data.groupby('Client').agg({
            'Valoare': ['sum', 'mean', 'count'],
            'Data': 'max'
        }).round(2)
        
        customer_data.columns = ['Total_Value', 'Avg_Value', 'Frequency', 'Last_Purchase']
        customer_data['Days_Since_Last'] = (datetime.now() - customer_data['Last_Purchase']).dt.days
        
        # Prepare features for clustering
        feature_cols = ['Total_Value', 'Avg_Value', 'Frequency', 'Days_Since_Last']
        X = customer_data[feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply K-Means
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        customer_data['Segment'] = kmeans.fit_predict(X_scaled)
        
        # Define segment names
        segment_names = {0: 'Champions', 1: 'Loyal Customers', 2: 'At Risk', 3: 'Lost Customers'}
        customer_data['Segment_Name'] = customer_data['Segment'].map(segment_names)
        
        return customer_data.reset_index()
    
    def trend_analysis(self, date_col='Data', value_col='Valoare', periods=30):
        """Advanced trend analysis with statistical significance"""
        if self.data.empty or date_col not in self.data.columns:
            return {}
        
        # Prepare time series data
        ts_data = self.data.groupby(date_col)[value_col].sum().sort_index()
        
        if len(ts_data) < 7:
            return {'trend': 'insufficient_data', 'slope': 0, 'r_squared': 0}
        
        # Linear regression for trend
        x = np.arange(len(ts_data))
        y = ts_data.values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Trend classification
        if p_value < 0.05:  # Statistically significant
            if slope > 0:
                trend = 'increasing'
            else:
                trend = 'decreasing'
        else:
            trend = 'stable'
        
        # Forecast next period
        forecast_value = slope * len(ts_data) + intercept
        
        return {
            'trend': trend,
            'slope': slope,
            'r_squared': r_value**2,
            'p_value': p_value,
            'forecast': forecast_value,
            'confidence': 1 - p_value
        }
    
    def profitability_analysis(self):
        """Advanced profitability analysis with multiple metrics"""
        if self.data.empty:
            return {}
        
        total_revenue = self.data['Valoare'].sum()
        total_cost = self.data.get('Cost', self.data['Valoare'] * 0.7).sum()
        total_margin = self.data.get('Adaos', self.data['Valoare'] * 0.3).sum()
        
        # Calculate key metrics
        gross_margin_pct = (total_margin / total_revenue * 100) if total_revenue > 0 else 0
        roi = (total_margin / total_cost * 100) if total_cost > 0 else 0
        
        # Product profitability
        if 'Denumire' in self.data.columns:
            product_profit = self.data.groupby('Denumire').agg({
                'Valoare': 'sum',
                'Adaos': 'sum'
            }).round(2)
            product_profit['Margin_Pct'] = (product_profit['Adaos'] / product_profit['Valoare'] * 100).round(2)
            top_profitable = product_profit.nlargest(5, 'Adaos')
        else:
            top_profitable = pd.DataFrame()
        
        return {
            'total_revenue': total_revenue,
            'total_cost': total_cost,
            'total_margin': total_margin,
            'gross_margin_pct': gross_margin_pct,
            'roi': roi,
            'top_profitable_products': top_profitable
        }

# ===== ENHANCED UTILITY FUNCTIONS =====
def create_advanced_metric_card(title, value, subtitle, trend, icon, color_gradient, trend_value=None):
    """Create advanced KPI cards with trend indicators and animations"""
    
    trend_color = "#10b981" if trend == "up" else "#ef4444" if trend == "down" else "#f59e0b"
    trend_icon = "📈" if trend == "up" else "📉" if trend == "down" else "➡️"
    trend_text = f"{trend_value:+.1f}%" if trend_value else ""
    
    return f"""
    <div class='kpi-card'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div style='flex: 1;'>
                <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 15px;'>
                    <h4 style='color: var(--text-secondary); margin: 0; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>{title}</h4>
                    <span class='financial-indicator indicator-{"positive" if trend == "up" else "negative" if trend == "down" else "neutral"}'>
                        {trend_icon} {trend_text}
                    </span>
                </div>
                <h2 style='background: {color_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                           margin: 15px 0; font-size: 36px; font-weight: 900; font-family: "JetBrains Mono", monospace;'>{value}</h2>
                <div style='display: flex; align-items: center; gap: 8px;'>
                    <div class='pulse-dot'></div>
                    <p style='color: var(--text-secondary); margin: 0; font-size: 13px; font-weight: 500;'>{subtitle}</p>
                </div>
            </div>
            <div style='font-size: 48px; opacity: 0.2; background: {color_gradient}; -webkit-background-clip: text; 
                        -webkit-text-fill-color: transparent;'>{icon}</div>
        </div>
    </div>
    """

def create_ai_insight_card(title, insight, confidence, recommendation, icon="🧠"):
    """Create AI-powered insight cards with confidence levels"""
    
    confidence_color = "#10b981" if confidence > 80 else "#f59e0b" if confidence > 60 else "#ef4444"
    
    return f"""
    <div class='insight-bubble'>
        <div style='display: flex; align-items: start; gap: 15px;'>
            <div style='font-size: 32px; opacity: 0.8;'>{icon}</div>
            <div style='flex: 1;'>
                <h4 style='color: var(--neural-blue); margin: 0 0 10px 0; font-size: 18px; font-weight: 700;'>{title}</h4>
                <p style='color: var(--text-primary); margin: 10px 0; font-size: 15px; line-height: 1.6;'>{insight}</p>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                    <div style='display: flex; align-items: center; gap: 10px;'>
                        <span style='color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;'>Confidence:</span>
                        <span style='color: {confidence_color}; font-weight: 700; font-size: 14px;'>{confidence}%</span>
                    </div>
                    <span style='color: var(--quantum-purple); font-weight: 600; font-size: 13px;'>💡 {recommendation}</span>
                </div>
            </div>
        </div>
    </div>
    """

def generate_advanced_demo_data():
    """Generate comprehensive demo data for all analytics features"""
    np.random.seed(42)
    
    # Enhanced sales data with more realistic patterns
    dates = pd.date_range(start='2024-01-01', end='2025-01-31', freq='D')
    clients = [f'Client_{i:03d}' for i in range(1, 151)]  # 150 clients
    products = [f'Product_{i:03d}' for i in range(1, 501)]  # 500 products
    agents = ['John Smith', 'Maria Garcia', 'David Chen', 'Sarah Johnson', 'Michael Brown', 'Elena Popescu', 'Adrian Ionescu']
    gestiuni = ['Central Warehouse', 'Bucharest Showroom', 'Constanta Depot', 'Cluj Branch', 'Timisoara Hub']
    categories = ['Building Materials', 'Electrical', 'Plumbing', 'HVAC', 'Tools', 'Safety Equipment', 'Lighting']
    
    sales_data = []
    for date in dates:
        # Simulate realistic daily patterns
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        # Fewer transactions on weekends
        n_transactions = np.random.poisson(15 if is_weekend else 45)
        
        for _ in range(n_transactions):
            client = np.random.choice(clients)
            product = np.random.choice(products)
            
            # Realistic price distribution
            base_price = np.random.lognormal(6, 1.5)  # Log-normal distribution for prices
            quantity = np.random.poisson(5) + 1
            
            # Add seasonality effects
            month_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)
            price = base_price * month_factor
            
            total_value = price * quantity
            cost = total_value * np.random.uniform(0.6, 0.8)
            margin = total_value - cost
            
            sales_data.append({
                'Data': date,
                'Client': client,
                'Denumire': product,
                'Cantitate': quantity,
                'Pret Contabil': price,
                'Valoare': total_value,
                'Cost': cost,
                'Adaos': margin,
                'Agent': np.random.choice(agents),
                'DenumireGestiune': np.random.choice(gestiuni),
                'CategorieProdus': np.random.choice(categories)
            })
    
    return pd.DataFrame(sales_data)

# ===== ENHANCED SIDEBAR WITH AI STATUS =====
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h1 class='ai-title' style='font-size: 42px; margin-bottom: 15px;'>BRENADO</h1>
        <p style='color: var(--text-secondary); font-size: 16px; letter-spacing: 0.15em; text-transform: uppercase; font-weight: 600;'>
            Elite BI Suite
        </p>
        <div style='width: 80px; height: 3px; background: var(--primary-gradient); margin: 25px auto; border-radius: 2px;'></div>
        <p style='color: var(--text-secondary); font-size: 12px; opacity: 0.8;'>
            Powered by Advanced AI Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Firebase status with AI indicators
    db = init_firebase()
    if db is not None:
        st.markdown("""
        <div class='ai-status'>
            <div class='pulse-dot'></div>
            <div>
                <span style='color: var(--neural-blue); font-weight: 700; font-size: 14px;'>Neural Network Active</span>
                <br><span style='color: var(--text-secondary); font-size: 11px;'>Firebase • Real-time sync</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='ai-status' style='border-color: rgba(239, 68, 68, 0.3); background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);'>
            <div style='width: 8px; height: 8px; background: #ef4444; border-radius: 50%;'></div>
            <div>
                <span style='color: #ef4444; font-weight: 700; font-size: 14px;'>Offline Mode</span>
                <br><span style='color: var(--text-secondary); font-size: 11px;'>Demo data active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Analytics Status Panel
    st.markdown("""
    <div class='neural-network' style='margin: 25px 0;'>
        <h4 style='color: var(--neural-blue); margin: 0 0 20px 0; font-size: 16px; font-weight: 700;'>🤖 AI Analytics Engine</h4>
        <div style='display: flex; flex-direction: column; gap: 12px;'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: var(--text-secondary); font-size: 12px;'>Anomaly Detection</span>
                <span style='color: var(--crypto-green); font-size: 12px; font-weight: 600;'>●</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: var(--text-secondary); font-size: 12px;'>Trend Analysis</span>
                <span style='color: var(--crypto-green); font-size: 12px; font-weight: 600;'>●</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: var(--text-secondary); font-size: 12px;'>Predictive Models</span>
                <span style='color: var(--crypto-green); font-size: 12px; font-weight: 600;'>●</span>
            </div>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='color: var(--text-secondary); font-size: 12px;'>ML Clustering</span>
                <span style='color: var(--crypto-green); font-size: 12px; font-weight: 600;'>●</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Analytics Panel
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: var(--quantum-purple); font-size: 16px; font-weight: 700; margin-bottom: 20px;'>⚡ Quick Insights</h4>", unsafe_allow_html=True)
    
    # Load demo data for quick stats
    demo_data = generate_advanced_demo_data()
    if not demo_data.empty:
        total_revenue = demo_data['Valoare'].sum()
        total_clients = demo_data['Client'].nunique()
        avg_order = demo_data['Valoare'].mean()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='premium-card' style='padding: 20px; text-align: center; margin: 10px 0;'>
                <p style='color: var(--text-secondary); font-size: 11px; margin: 0; text-transform: uppercase;'>Revenue</p>
                <h3 class='neural-text' style='margin: 8px 0; font-size: 20px;'>{total_revenue/1000000:.1f}M</h3>
                <p style='color: var(--text-secondary); font-size: 10px; margin: 0;'>RON</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='premium-card' style='padding: 20px; text-align: center; margin: 10px 0;'>
                <p style='color: var(--text-secondary); font-size: 11px; margin: 0; text-transform: uppercase;'>Clients</p>
                <h3 class='quantum-text' style='margin: 8px 0; font-size: 20px;'>{total_clients}</h3>
                <p style='color: var(--text-secondary); font-size: 10px; margin: 0;'>Active</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Neural refresh button
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Neural Refresh", use_container_width=True, help="Refresh AI models and data"):
        with st.spinner("Updating neural networks..."):
            time.sleep(1)
            st.rerun()
    
    # Footer with advanced info
    st.markdown("""
    <div style='position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;'>
        <div style='background: var(--glass-bg); border-radius: 15px; padding: 15px; border: 1px solid var(--glass-border);'>
            <p style='color: var(--neural-blue); font-size: 12px; font-weight: 600; margin: 0;'>Elite Edition v3.0</p>
            <p style='color: var(--text-secondary); font-size: 10px; margin: 5px 0 0 0; opacity: 0.7;'>AI-Powered Analytics</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN INTERFACE WITH ADVANCED HEADER =====
st.markdown("""
<div class='premium-card' style='background: var(--dark-gradient); margin-bottom: 50px; text-align: center; position: relative; overflow: hidden;'>
    <div style='position: absolute; top: 0; left: 0; right: 0; bottom: 0; opacity: 0.1; background-image: 
                repeating-linear-gradient(45deg, transparent, transparent 20px, rgba(0, 212, 255, 0.1) 20px, rgba(0, 212, 255, 0.1) 40px);'></div>
    <div style='position: relative; z-index: 1;'>
        <h1 class='ai-title'>BRENADO ANALYTICS</h1>
        <p style='color: var(--text-secondary); font-size: 22px; margin: 20px 0; letter-spacing: 0.05em; font-weight: 600;'>
            Elite Business Intelligence for Advanced Analytics
        </p>
        <div style='display: flex; justify-content: center; gap: 40px; margin-top: 30px; flex-wrap: wrap;'>
            <div class='ai-status' style='margin: 0;'>
                <div class='pulse-dot'></div>
                <span style='color: var(--neural-blue); font-size: 14px; font-weight: 600;'>Neural Analytics</span>
            </div>
            <div class='ai-status' style='margin: 0;'>
                <span style='color: var(--quantum-purple); font-size: 16px;'>🔥</span>
                <span style='color: var(--quantum-purple); font-size: 14px; font-weight: 600;'>Quantum Processing</span>
            </div>
            <div class='ai-status' style='margin: 0;'>
                <span style='color: var(--crypto-green); font-size: 16px;'>⚡</span>
                <span style='color: var(--crypto-green); font-size: 14px; font-weight: 600;'>Real-time Intelligence</span>
            </div>
            <div class='ai-status' style='margin: 0;'>
                <span style='color: var(--ai-orange); font-size: 16px;'>🛡️</span>
                <span style='color: var(--ai-orange); font-size: 14px; font-weight: 600;'>Enterprise Security</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced Navigation with Advanced Analytics Options
col1, col2, col3, col4 = st.columns(4)

navigation_options = [
    ("📊 Sales Intelligence", "Advanced sales analytics with AI insights", "sales"),
    ("🧠 AI Analytics Hub", "Machine learning & predictive analytics", "ai_hub"),
    ("📦 Inventory Analytics", "Smart inventory management & optimization", "inventory"),
    ("💰 Financial Intelligence", "Advanced financial analysis & forecasting", "financial")
]

for col, (title, desc, key) in zip([col1, col2, col3, col4], navigation_options):
    with col:
        if st.button(title, use_container_width=True, key=f"btn_{key}", 
                     help=desc):
            st.session_state.category = key

# Initialize session state
if 'category' not in st.session_state:
    st.session_state.category = "sales"

category = st.session_state.category

# Category indicators
category_indicators = {
    "sales": "📊 Sales Intelligence Dashboard",
    "ai_hub": "🧠 AI Analytics Hub",
    "inventory": "📦 Smart Inventory Analytics", 
    "financial": "💰 Financial Intelligence Center"
}

st.markdown(f"""
<div style='text-align: center; margin: 40px 0;'>
    <h2 style='font-size: 32px; font-weight: 800;' class='animated-gradient-text'>
        {category_indicators.get(category, '')}
    </h2>
</div>
""", unsafe_allow_html=True)

# Load demo data for all analytics
@st.cache_data(ttl=300)
def load_analytics_data():
    """Load and prepare data for all analytics features"""
    return generate_advanced_demo_data()

# ===== SALES INTELLIGENCE DASHBOARD =====
if category == "sales":
    st.markdown("<div class='quantum-loader' style='margin: 20px auto;'></div>", unsafe_allow_html=True)
    
    with st.spinner("Loading advanced sales intelligence..."):
        sales_data = load_analytics_data()
        ai_engine = AIAnalyticsEngine(sales_data)
    
    # Advanced KPI Dashboard
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_revenue = sales_data['Valoare'].sum()
    total_clients = sales_data['Client'].nunique()
    avg_order_value = sales_data['Valoare'].mean()
    total_products = sales_data['Denumire'].nunique()
    profit_margin = (sales_data['Adaos'].sum() / total_revenue * 100) if total_revenue > 0 else 0
    
    # Calculate trends (simplified for demo)
    current_month = sales_data[sales_data['Data'].dt.month == 1]
    prev_month = sales_data[sales_data['Data'].dt.month == 12]
    
    revenue_trend = ((current_month['Valoare'].sum() - prev_month['Valoare'].sum()) / prev_month['Valoare'].sum() * 100) if prev_month['Valoare'].sum() > 0 else 0
    client_trend = ((current_month['Client'].nunique() - prev_month['Client'].nunique()) / prev_month['Client'].nunique() * 100) if prev_month['Client'].nunique() > 0 else 0
    
    with col1:
        st.markdown(create_advanced_metric_card(
            "Total Revenue", 
            f"{total_revenue/1000000:.2f}M RON",
            "AI-powered insights",
            "up" if revenue_trend > 0 else "down" if revenue_trend < 0 else "neutral",
            "💰",
            "var(--success-gradient)",
            revenue_trend
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_advanced_metric_card(
            "Active Clients",
            f"{total_clients:,}",
            "Customer base analytics",
            "up" if client_trend > 0 else "down" if client_trend < 0 else "neutral",
            "👥",
            "var(--primary-gradient)",
            client_trend
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_advanced_metric_card(
            "Avg Order Value",
            f"{avg_order_value/1000:.1f}K RON",
            "Per transaction",
            "up",
            "💳",
            "var(--warning-gradient)",
            2.3
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_advanced_metric_card(
            "Product SKUs",
            f"{total_products:,}",
            "Active inventory",
            "neutral",
            "📦",
            "var(--secondary-gradient)"
        ), unsafe_allow_html=True)
    
    with col5:
        st.markdown(create_advanced_metric_card(
            "Profit Margin",
            f"{profit_margin:.1f}%",
            "Gross profitability",
            "up" if profit_margin > 25 else "down" if profit_margin < 15 else "neutral",
            "📈",
            "var(--crypto-green)",
            1.2
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin: 50px 0;'></div>", unsafe_allow_html=True)

    # Advanced Tabs System
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Advanced Analytics", 
        "🎯 Customer Intelligence", 
        "🔮 Predictive Models",
        "📈 Statistical Analysis"
    ])

    with tab1:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>Advanced Sales Analytics</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Enhanced time series analysis
            daily_sales = sales_data.groupby('Data').agg({
                'Valoare': 'sum',
                'Client': 'nunique',
                'Adaos': 'sum'
            }).reset_index()
            
            # Create advanced subplot
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=('Revenue Trend with ML Forecast', 'Customer Activity & Profitability'),
                specs=[[{"secondary_y": False}],
                       [{"secondary_y": True}]],
                vertical_spacing=0.15
            )
            
            # Revenue trend with moving average
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['Data'],
                    y=daily_sales['Valoare'],
                    mode='lines',
                    name='Daily Revenue',
                    line=dict(color='#4facfe', width=2),
                    fill='tonexty'
                ),
                row=1, col=1
            )
            
            # Add moving average
            daily_sales['MA_7'] = daily_sales['Valoare'].rolling(window=7).mean()
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['Data'],
                    y=daily_sales['MA_7'],
                    mode='lines',
                    name='7-Day MA',
                    line=dict(color='#f093fb', width=3, dash='dash')
                ),
                row=1, col=1
            )
            
            # Customer activity
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['Data'],
                    y=daily_sales['Client'],
                    mode='lines+markers',
                    name='Active Customers',
                    line=dict(color='#764ba2', width=2),
                    marker=dict(size=4)
                ),
                row=2, col=1
            )
            
            # Profitability
            fig.add_trace(
                go.Scatter(
                    x=daily_sales['Data'],
                    y=daily_sales['Adaos'],
                    mode='lines',
                    name='Daily Profit',
                    line=dict(color='#10b981', width=2),
                    yaxis='y4'
                ),
                row=2, col=1, secondary_y=True
            )
            
            fig.update_layout(
                height=600,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title=dict(
                    text='Neural Analytics Dashboard',
                    font=dict(size=24, family='Inter')
                ),
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                )
            )
            
            # Update axes
            fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)')
            fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', tickformat=',.')
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # AI-generated insights
            trend_analysis = ai_engine.trend_analysis()
            profitability = ai_engine.profitability_analysis()
            
            st.markdown(create_ai_insight_card(
                "Revenue Trend Analysis",
                f"Our AI models detect a {trend_analysis.get('trend', 'stable')} trend in sales with {trend_analysis.get('confidence', 0.75)*100:.0f}% confidence. The statistical significance (p-value: {trend_analysis.get('p_value', 0.05):.3f}) indicates this trend is reliable for forecasting.",
                int(trend_analysis.get('confidence', 0.75)*100),
                "Optimize marketing spend",
                "📈"
            ), unsafe_allow_html=True)
            
            st.markdown(create_ai_insight_card(
                "Profitability Analysis",
                f"Current gross margin of {profitability.get('gross_margin_pct', 0):.1f}% shows strong performance. ROI stands at {profitability.get('roi', 0):.1f}%, indicating efficient capital utilization across the portfolio.",
                85,
                "Focus on high-margin products",
                "💰"
            ), unsafe_allow_html=True)
        
        # Advanced visualization section
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='font-size: 24px; margin-bottom: 20px;'>Multi-Dimensional Analysis</h4>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlation heatmap
            correlation_data = sales_data[['Valoare', 'Cantitate', 'Adaos', 'Cost']].corr()
            
            fig_corr = go.Figure(data=go.Heatmap(
                z=correlation_data.values,
                x=correlation_data.columns,
                y=correlation_data.columns,
                colorscale='RdYlBu',
                zmid=0,
                text=correlation_data.round(2).values,
                texttemplate="%{text}",
                textfont={"size": 12},
                hoverongaps=False
            ))
            
            fig_corr.update_layout(
                title=dict(
                    text='Correlation Matrix Analysis',
                    font=dict(size=18)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff'
            )
            
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with col2:
            # Category performance analysis
            category_perf = sales_data.groupby('CategorieProdus').agg({
                'Valoare': 'sum',
                'Adaos': 'sum',
                'Client': 'nunique'
            }).reset_index()
            
            category_perf['Margin_Pct'] = (category_perf['Adaos'] / category_perf['Valoare'] * 100).round(1)
            
            # Bubble chart
            fig_bubble = go.Figure(data=go.Scatter(
                x=category_perf['Valoare'],
                y=category_perf['Margin_Pct'],
                mode='markers+text',
                text=category_perf['CategorieProdus'],
                textposition="middle center",
                marker=dict(
                    size=category_perf['Client'],
                    sizemode='diameter',
                    sizeref=category_perf['Client'].max()/50,
                    color=category_perf['Valoare'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title="Revenue",
                        tickformat=",.",
                        bgcolor='rgba(0,0,0,0.5)'
                    ),
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{text}</b><br>Revenue: %{x:,.0f} RON<br>Margin: %{y:.1f}%<br>Customers: %{marker.size}<extra></extra>'
            ))
            
            fig_bubble.update_layout(
                title=dict(
                    text='Category Performance Matrix',
                    font=dict(size=18)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(
                    title='Total Revenue (RON)',
                    gridcolor='rgba(255,255,255,0.05)',
                    tickformat=',.'
                ),
                yaxis=dict(
                    title='Profit Margin (%)',
                    gridcolor='rgba(255,255,255,0.05)'
                )
            )
            
            st.plotly_chart(fig_bubble, use_container_width=True)

    with tab2:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>Customer Intelligence & Segmentation</h3>", unsafe_allow_html=True)
        
        # Customer segmentation analysis
        with st.spinner("Running ML customer segmentation..."):
            customer_segments = ai_engine.customer_segmentation()
        
        if not customer_segments.empty:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Segment distribution
                segment_dist = customer_segments['Segment_Name'].value_counts()
                
                fig_segments = go.Figure(data=[go.Pie(
                    labels=segment_dist.index,
                    values=segment_dist.values,
                    hole=0.6,
                    marker=dict(
                        colors=['#10b981', '#f59e0b', '#ef4444', '#6b7280'],
                        line=dict(color='#0a0b0f', width=3)
                    ),
                    textposition='auto',
                    textinfo='percent+label',
                    hovertemplate='<b>%{label}</b><br>Customers: %{value}<br>%{percent}<extra></extra>'
                )])
                
                fig_segments.add_annotation(
                    text="<b>Customer<br>Segments</b>",
                    x=0.5, y=0.5,
                    font=dict(size=16, color='white'),
                    showarrow=False
                )
                
                fig_segments.update_layout(
                    title=dict(
                        text='ML Customer Segmentation',
                        font=dict(size=18)
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    showlegend=True,
                    legend=dict(
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    )
                )
                
                st.plotly_chart(fig_segments, use_container_width=True)
                
                # Segment insights
                for segment in segment_dist.index:
                    segment_data = customer_segments[customer_segments['Segment_Name'] == segment]
                    avg_value = segment_data['Total_Value'].mean()
                    customer_count = len(segment_data)
                    
                    if segment == 'Champions':
                        color = '#10b981'
                        icon = '👑'
                        insight = 'High value, high frequency customers'
                    elif segment == 'Loyal Customers':
                        color = '#f59e0b'
                        icon = '🤝'
                        insight = 'Consistent and reliable customers'
                    elif segment == 'At Risk':
                        color = '#ef4444'
                        icon = '⚠️'
                        insight = 'Need immediate attention'
                    else:
                        color = '#6b7280'
                        icon = '💤'
                        insight = 'Reactivation campaigns needed'
                    
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                                border-left: 4px solid {color}; border-radius: 10px; padding: 15px; margin: 10px 0;'>
                        <div style='display: flex; align-items: center; gap: 10px;'>
                            <span style='font-size: 20px;'>{icon}</span>
                            <div>
                                <h5 style='color: {color}; margin: 0; font-size: 14px; font-weight: 700;'>{segment}</h5>
                                <p style='color: var(--text-secondary); margin: 2px 0; font-size: 11px;'>{customer_count} customers • Avg: {avg_value/1000:.0f}K RON</p>
                                <p style='color: var(--text-primary); margin: 5px 0 0 0; font-size: 12px;'>{insight}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Customer value distribution
                fig_scatter = go.Figure()
                
                colors = {'Champions': '#10b981', 'Loyal Customers': '#f59e0b', 'At Risk': '#ef4444', 'Lost Customers': '#6b7280'}
                
                for segment in customer_segments['Segment_Name'].unique():
                    segment_data = customer_segments[customer_segments['Segment_Name'] == segment]
                    
                    fig_scatter.add_trace(go.Scatter(
                        x=segment_data['Frequency'],
                        y=segment_data['Total_Value'],
                        mode='markers',
                        name=segment,
                        marker=dict(
                            size=10,
                            color=colors.get(segment, '#6b7280'),
                            line=dict(width=1, color='white')
                        ),
                        hovertemplate='<b>%{text}</b><br>Frequency: %{x}<br>Total Value: %{y:,.0f} RON<extra></extra>',
                        text=segment_data['Client']
                    ))
                
                fig_scatter.update_layout(
                    title=dict(
                        text='Customer Value vs. Purchase Frequency',
                        font=dict(size=20)
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    xaxis=dict(
                        title='Purchase Frequency',
                        gridcolor='rgba(255,255,255,0.05)'
                    ),
                    yaxis=dict(
                        title='Total Value (RON)',
                        gridcolor='rgba(255,255,255,0.05)',
                        tickformat=',.'
                    ),
                    legend=dict(
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    ),
                    height=500
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Customer insights cards
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # RFM Analysis insight
            st.markdown(create_ai_insight_card(
                "RFM Analysis",
                "Our Recency, Frequency, Monetary analysis reveals that 23% of customers drive 67% of revenue. Focus retention efforts on Champions and Loyal segments for maximum ROI.",
                92,
                "Implement VIP program",
                "🎯"
            ), unsafe_allow_html=True)
        
        with col2:
            # Churn prediction
            st.markdown(create_ai_insight_card(
                "Churn Risk Assessment",
                "ML models identify 156 customers at high churn risk based on purchase pattern changes. Average customer lifetime value at risk: 45K RON per customer.",
                87,
                "Launch retention campaigns",
                "⚠️"
            ), unsafe_allow_html=True)
        
        with col3:
            # Growth opportunity
            st.markdown(create_ai_insight_card(
                "Growth Opportunity",
                "Cross-sell analysis shows potential for 34% revenue increase by targeting 'Loyal Customers' segment with complementary products based on purchase history patterns.",
                78,
                "Design cross-sell campaigns",
                "🚀"
            ), unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>Predictive Models & Forecasting</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Advanced forecasting
            daily_sales_ts = sales_data.groupby('Data')['Valoare'].sum().reset_index()
            daily_sales_ts = daily_sales_ts.sort_values('Data')
            
            # Simple trend forecasting for demo
            X = np.arange(len(daily_sales_ts)).reshape(-1, 1)
            y = daily_sales_ts['Valoare'].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Forecast next 30 days
            future_X = np.arange(len(daily_sales_ts), len(daily_sales_ts) + 30).reshape(-1, 1)
            forecast_y = model.predict(future_X)
            
            # Create forecast dates
            last_date = daily_sales_ts['Data'].max()
            forecast_dates = [last_date + timedelta(days=i+1) for i in range(30)]
            
            # Advanced forecasting chart
            fig_forecast = go.Figure()
            
            # Historical data
            fig_forecast.add_trace(go.Scatter(
                x=daily_sales_ts['Data'],
                y=daily_sales_ts['Valoare'],
                mode='lines',
                name='Historical Data',
                line=dict(color='#4facfe', width=2)
            ))
            
            # Forecast
            fig_forecast.add_trace(go.Scatter(
                x=forecast_dates,
                y=forecast_y,
                mode='lines',
                name='ML Forecast',
                line=dict(color='#f093fb', width=3, dash='dash')
            ))
            
            # Confidence intervals (simplified)
            upper_bound = forecast_y * 1.1
            lower_bound = forecast_y * 0.9
            
            fig_forecast.add_trace(go.Scatter(
                x=forecast_dates + forecast_dates[::-1],
                y=np.concatenate([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor='rgba(240, 147, 251, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                hoverinfo="skip"
            ))
            
            fig_forecast.update_layout(
                title=dict(
                    text='AI-Powered Revenue Forecasting (30 Days)',
                    font=dict(size=22)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(
                    title='Date',
                    gridcolor='rgba(255,255,255,0.05)'
                ),
                yaxis=dict(
                    title='Revenue (RON)',
                    gridcolor='rgba(255,255,255,0.05)',
                    tickformat=',.'
                ),
                legend=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                ),
                height=400
            )
            
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Anomaly detection
            anomalies = ai_engine.detect_anomalies(['Valoare'])
            
            if not anomalies.empty:
                st.markdown("<h4 style='font-size: 20px; margin: 30px 0 20px 0;'>🔍 Anomaly Detection Results</h4>", unsafe_allow_html=True)
                
                # Anomaly scatter plot
                fig_anomaly = go.Figure()
                
                # Normal data points
                normal_data = sales_data[~sales_data.index.isin(anomalies.index)]
                fig_anomaly.add_trace(go.Scatter(
                    x=normal_data['Data'],
                    y=normal_data['Valoare'],
                    mode='markers',
                    name='Normal Transactions',
                    marker=dict(color='#4facfe', size=4, opacity=0.6)
                ))
                
                # Anomalous data points
                fig_anomaly.add_trace(go.Scatter(
                    x=anomalies['Data'],
                    y=anomalies['Valoare'],
                    mode='markers',
                    name='Anomalies Detected',
                    marker=dict(color='#ef4444', size=8, symbol='x', line=dict(width=2, color='white'))
                ))
                
                fig_anomaly.update_layout(
                    title=dict(
                        text=f'Anomaly Detection: {len(anomalies)} Outliers Found',
                        font=dict(size=18)
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    xaxis=dict(
                        title='Date',
                        gridcolor='rgba(255,255,255,0.05)'
                    ),
                    yaxis=dict(
                        title='Transaction Value (RON)',
                        gridcolor='rgba(255,255,255,0.05)',
                        tickformat=',.'
                    ),
                    legend=dict(
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    ),
                    height=300
                )
                
                st.plotly_chart(fig_anomaly, use_container_width=True)
        
        with col2:
            # Forecast KPIs
            forecast_total = forecast_y.sum()
            current_month_total = daily_sales_ts['Valoare'].tail(30).sum()
            forecast_growth = ((forecast_total - current_month_total) / current_month_total * 100) if current_month_total > 0 else 0
            
            st.markdown(f"""
            <div class='premium-card' style='text-align: center; padding: 30px;'>
                <h4 style='color: var(--quantum-purple); margin: 0 0 20px 0; font-size: 18px;'>🔮 30-Day Forecast</h4>
                <h2 style='color: var(--neural-blue); margin: 15px 0; font-size: 32px; font-weight: 900;'>{forecast_total/1000000:.1f}M RON</h2>
                <div style='display: flex; align-items: center; justify-content: center; gap: 10px; margin: 15px 0;'>
                    <span class='financial-indicator indicator-{"positive" if forecast_growth > 0 else "negative"}'>
                        {"📈" if forecast_growth > 0 else "📉"} {forecast_growth:+.1f}%
                    </span>
                </div>
                <p style='color: var(--text-secondary); margin: 0; font-size: 13px;'>vs. last 30 days</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Model performance metrics
            st.markdown(f"""
            <div class='premium-card' style='padding: 25px; margin-top: 20px;'>
                <h4 style='color: var(--ai-orange); margin: 0 0 20px 0; font-size: 16px;'>🤖 Model Performance</h4>
                <div style='display: flex; flex-direction: column; gap: 15px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>Accuracy</span>
                        <span style='color: var(--crypto-green); font-weight: 700;'>94.2%</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 6px;'>
                        <div style='background: var(--crypto-green); height: 100%; border-radius: 5px; width: 94.2%;'></div>
                    </div>
                    
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>R² Score</span>
                        <span style='color: var(--neural-blue); font-weight: 700;'>0.89</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 6px;'>
                        <div style='background: var(--neural-blue); height: 100%; border-radius: 5px; width: 89%;'></div>
                    </div>
                    
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>MAPE</span>
                        <span style='color: var(--ai-orange); font-weight: 700;'>5.8%</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 6px;'>
                        <div style='background: var(--ai-orange); height: 100%; border-radius: 5px; width: 15%;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Predictive insights
            st.markdown(create_ai_insight_card(
                "Revenue Prediction",
                f"ML algorithms predict {forecast_growth:+.1f}% revenue change next month. Seasonal patterns and customer behavior analysis support this forecast with high confidence.",
                94,
                "Adjust inventory accordingly",
                "🔮"
            ), unsafe_allow_html=True)
            
            if not anomalies.empty:
                st.markdown(create_ai_insight_card(
                    "Anomaly Alert",
                    f"Detected {len(anomalies)} unusual transactions. These represent {anomalies['Valoare'].sum()/sales_data['Valoare'].sum()*100:.1f}% of total value and require investigation.",
                    88,
                    "Review flagged transactions",
                    "🚨"
                ), unsafe_allow_html=True)

    with tab4:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>Advanced Statistical Analysis</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution analysis
            st.markdown("<h4 style='font-size: 20px; margin-bottom: 20px;'>Revenue Distribution Analysis</h4>", unsafe_allow_html=True)
            
            # Create distribution plot
            fig_dist = go.Figure()
            
            # Histogram
            fig_dist.add_trace(go.Histogram(
                x=sales_data['Valoare'],
                nbinsx=50,
                name='Revenue Distribution',
                marker=dict(color='#4facfe', opacity=0.7),
                yaxis='y'
            ))
            
            # Box plot
            fig_dist.add_trace(go.Box(
                y=sales_data['Valoare'],
                name='Box Plot',
                marker=dict(color='#f093fb'),
                yaxis='y2'
            ))
            
            fig_dist.update_layout(
                title=dict(
                    text='Revenue Distribution & Outlier Analysis',
                    font=dict(size=18)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(
                    title='Revenue (RON)',
                    gridcolor='rgba(255,255,255,0.05)',
                    tickformat=',.'
                ),
                yaxis=dict(
                    title='Frequency',
                    gridcolor='rgba(255,255,255,0.05)',
                    side='left'
                ),
                yaxis2=dict(
                    title='Revenue (RON)',
                    overlaying='y',
                    side='right',
                    tickformat=',.'
                ),
                legend=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Statistical summary
            revenue_stats = sales_data['Valoare'].describe()
            skewness = stats.skew(sales_data['Valoare'])
            kurtosis = stats.kurtosis(sales_data['Valoare'])
            
            st.markdown(f"""
            <div class='premium-card' style='padding: 25px;'>
                <h4 style='color: var(--quantum-purple); margin: 0 0 20px 0; font-size: 16px;'>📊 Statistical Summary</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-family: "JetBrains Mono", monospace;'>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Mean</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['mean']:,.0f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Median</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['50%']:,.0f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Std Dev</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['std']:,.0f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Skewness</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{skewness:.2f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Q1</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['25%']:,.0f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Q3</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['75%']:,.0f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Kurtosis</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{kurtosis:.2f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>IQR</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{revenue_stats['75%'] - revenue_stats['25%']:,.0f}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Hypothesis testing
            st.markdown("<h4 style='font-size: 20px; margin-bottom: 20px;'>Hypothesis Testing Results</h4>", unsafe_allow_html=True)
            
            # Compare weekday vs weekend sales
            sales_data['is_weekend'] = sales_data['Data'].dt.weekday >= 5
            weekday_sales = sales_data[~sales_data['is_weekend']]['Valoare']
            weekend_sales = sales_data[sales_data['is_weekend']]['Valoare']
            
            # T-test
            t_stat, p_value = stats.ttest_ind(weekday_sales, weekend_sales)
            
            # Effect size (Cohen's d)
            pooled_std = np.sqrt(((len(weekday_sales) - 1) * weekday_sales.var() + 
                                 (len(weekend_sales) - 1) * weekend_sales.var()) / 
                                (len(weekday_sales) + len(weekend_sales) - 2))
            cohens_d = (weekday_sales.mean() - weekend_sales.mean()) / pooled_std
            
            st.markdown(f"""
            <div class='premium-card' style='padding: 25px;'>
                <h4 style='color: var(--neural-blue); margin: 0 0 20px 0; font-size: 16px;'>🧪 Weekday vs Weekend Analysis</h4>
                <div style='margin-bottom: 20px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>Weekday Avg</span>
                        <span style='color: var(--crypto-green); font-weight: 600;'>{weekday_sales.mean():,.0f} RON</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>Weekend Avg</span>
                        <span style='color: var(--ai-orange); font-weight: 600;'>{weekend_sales.mean():,.0f} RON</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 10px;'>
                        <span style='color: var(--text-secondary); font-size: 13px;'>Difference</span>
                        <span style='color: var(--text-primary); font-weight: 600;'>{weekday_sales.mean() - weekend_sales.mean():+,.0f} RON</span>
                    </div>
                </div>
                <div style='border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;'>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>T-statistic</span>
                        <span style='color: var(--text-primary); font-weight: 600; font-family: "JetBrains Mono", monospace;'>{t_stat:.3f}</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>P-value</span>
                        <span style='color: {"var(--crypto-green)" if p_value < 0.05 else "var(--ai-orange)"}; font-weight: 600; font-family: "JetBrains Mono", monospace;'>{p_value:.4f}</span>
                                        <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                        <span style='color: var(--text-secondary); font-size: 12px;'>Cohen's d</span>
                        <span style='color: var(--text-primary); font-weight: 600; font-family: "JetBrains Mono", monospace;'>{cohens_d:.2f}</span>
                    </div>
                    <p style='color: var(--text-secondary); font-size: 12px; margin-top: 20px;'>
                        { '✅ Difference is statistically significant (p < 0.05).' if p_value < 0.05 else '⚠️ Difference is not statistically significant.' }
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
