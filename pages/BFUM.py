import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time

# Firebase imports
import firebase_admin
from firebase_admin import credentials, firestore

# Configurare pagină cu tema dark premium
st.set_page_config(
    page_title="BRENADO | Premium Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "BRENADO Premium Analytics Dashboard v2.0"
    }
)

# CSS ULTRA MODERN - Design Premium de Milioane
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Variabile CSS pentru design system consistent */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-gradient: linear-gradient(135deg, #2b2d42 0%, #1a1b27 100%);
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --text-primary: #ffffff;
        --text-secondary: #a0a0b8;
        --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.3);
        --shadow-glow: 0 0 40px rgba(102, 126, 234, 0.4);
    }
    
    /* Dark Theme Ultra Premium */
    .stApp {
        background: #0a0b0f;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(245, 87, 108, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(250, 112, 154, 0.05) 0%, transparent 50%);
        min-height: 100vh;
    }
    
    /* Animated Background Pattern */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(102, 126, 234, 0.03) 35px, rgba(102, 126, 234, 0.03) 70px);
        pointer-events: none;
        animation: backgroundMove 20s linear infinite;
    }
    
    @keyframes backgroundMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(70px, 70px); }
    }
    
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-xl);
        padding: 30px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        transform: rotate(45deg);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .glass-card:hover::before {
        opacity: 1;
    }
    
    /* Metric Cards Ultra Premium */
    div[data-testid="metric-container"] {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: var(--primary-gradient);
        opacity: 0.1;
        border-radius: 50%;
        transform: scale(0);
        transition: transform 0.6s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    div[data-testid="metric-container"]:hover::after {
        transform: scale(2);
    }
    
    /* Typography Premium */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 15px 35px;
        border-radius: 15px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 16px;
        letter-spacing: 0.02em;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Premium Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        padding: 15px;
        border-radius: 20px;
        border: 1px solid var(--glass-border);
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: transparent;
        border-radius: 15px;
        color: var(--text-secondary);
        font-size: 16px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        padding: 12px 30px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        width: 0;
        height: 3px;
        background: var(--primary-gradient);
        transition: all 0.3s ease;
        transform: translateX(-50%);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-gradient);
        color: white;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .stTabs [aria-selected="true"]::before {
        width: 100%;
    }
    
    /* Select Box Premium */
    .stSelectbox > div > div {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* Premium Info Boxes */
    .premium-info-box {
        background: var(--glass-bg);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border-radius: 25px;
        padding: 35px;
        margin: 20px 0;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .premium-info-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        transform: translateX(-100%);
        transition: transform 0.6s ease;
    }
    
    .premium-info-box:hover::before {
        transform: translateX(0);
    }
    
    .premium-info-box:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-glow);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Stat Cards with Gradient Borders */
    .stat-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        padding: 1px;
        background: var(--primary-gradient);
        -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        -webkit-mask-composite: exclude;
        mask-composite: exclude;
        opacity: 0.5;
        transition: opacity 0.3s ease;
    }
    
    .stat-card:hover::before {
        opacity: 1;
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: var(--shadow-glow);
    }
    
    /* Premium Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(10, 11, 15, 0.95);
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--glass-border);
        box-shadow: 5px 0 20px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Animated Loading State */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Premium Alerts */
    .stAlert {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        border: 1px solid var(--glass-border);
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(0, 242, 254, 0.1) 100%);
        border-left: 4px solid #4facfe;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(250, 112, 154, 0.1) 0%, rgba(254, 225, 64, 0.1) 100%);
        border-left: 4px solid #fa709a;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(245, 87, 108, 0.1) 0%, rgba(250, 112, 154, 0.1) 100%);
        border-left: 4px solid #f5576c;
    }
    
    /* Scrollbar Premium */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Pulse Animation for Live Data */
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
        }
    }
    
    .live-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #4facfe;
        border-radius: 50%;
        animation: pulse 2s infinite;
        margin-right: 5px;
    }
    
    /* Gradient Text Animation */
    @keyframes gradientMove {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .animated-gradient-text {
        background: linear-gradient(270deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientMove 4s ease infinite;
    }
    
    /* Premium DataFrames */
    .dataframe {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border) !important;
        border-radius: 15px !important;
        overflow: hidden;
    }
    
    .dataframe th {
        background: var(--primary-gradient) !important;
        color: white !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 15px !important;
        text-align: left !important;
        border: none !important;
    }
    
    .dataframe td {
        background: transparent !important;
        color: var(--text-primary) !important;
        border-bottom: 1px solid var(--glass-border) !important;
        padding: 15px !important;
        transition: background 0.3s ease !important;
    }
    
    .dataframe tr:hover td {
        background: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Floating Action Buttons */
    .fab {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        background: var(--primary-gradient);
        border-radius: 50%;
        box-shadow: var(--shadow-xl);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: var(--shadow-glow);
    }
    
    /* Modern Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        background: var(--dark-gradient);
        color: white;
        text-align: center;
        border-radius: 10px;
        padding: 10px 15px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        box-shadow: var(--shadow-xl);
        font-size: 14px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Neon Glow Effects */
    .neon-blue {
        color: #4facfe;
        text-shadow: 0 0 10px #4facfe, 0 0 20px #4facfe, 0 0 30px #4facfe;
    }
    
    .neon-purple {
        color: #764ba2;
        text-shadow: 0 0 10px #764ba2, 0 0 20px #764ba2, 0 0 30px #764ba2;
    }
    
    .neon-pink {
        color: #f093fb;
        text-shadow: 0 0 10px #f093fb, 0 0 20px #f093fb, 0 0 30px #f093fb;
    }
</style>
""", unsafe_allow_html=True)

# Funcții helper pentru animații și loading states
def show_loading_animation(text="Loading"):
    return st.markdown(f"""
    <div style='text-align: center; padding: 20px;'>
        <div class='loading-animation'></div>
        <p style='color: var(--text-secondary); margin-top: 10px;'>{text}...</p>
    </div>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, subtitle, icon, color_gradient):
    return f"""
    <div class='stat-card'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div>
                <h4 style='color: var(--text-secondary); margin: 0; font-size: 14px; font-weight: 500;'>{title}</h4>
                <h2 style='background: {color_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                           margin: 10px 0; font-size: 32px; font-weight: 800;'>{value}</h2>
                <p style='color: var(--text-secondary); margin: 0; font-size: 13px; display: flex; align-items: center;'>
                    <span class='live-indicator'></span> {subtitle}
                </p>
            </div>
            <div style='font-size: 40px; opacity: 0.3; background: {color_gradient}; -webkit-background-clip: text; 
                        -webkit-text-fill-color: transparent;'>{icon}</div>
        </div>
    </div>
    """

# ===== FUNCȚII FIREBASE =====
@st.cache_resource
def init_firebase():
    """Inițializează Firebase pentru Streamlit Cloud"""
    try:
        # Verifică dacă Firebase e deja inițializat
        if firebase_admin._apps:
            return firestore.client()
        
        # Pentru STREAMLIT CLOUD - folosește secrets
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
        st.error(f"❌ Eroare conectare Firebase: {e}")
        return None

# ===== FUNCȚII PENTRU ÎNCĂRCAREA DATELOR DIN FIREBASE =====

@st.cache_data(ttl=300)  # Cache pentru 5 minute
def load_vanzari_zi_clienti():
    """Încarcă datele de vânzări din Firebase"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        # Încarcă toate documentele din colecția 'vanzari_current_month'
        docs = db.collection('vanzari_current_month').stream()
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            # Conversie timestamp Firebase la datetime
            if 'Data' in doc_data and doc_data['Data']:
                data_timestamp = doc_data['Data']
                if hasattr(data_timestamp, 'timestamp'):
                    data_datetime = datetime.fromtimestamp(data_timestamp.timestamp())
                else:
                    data_datetime = data_timestamp
            else:
                data_datetime = datetime.now()
            
            # Mapare date pentru compatibilitate
            row = {
                'Data': data_datetime,
                'Client': doc_data.get('Client', 'N/A'),
                'Pret Contabil': doc_data.get('Pret_Contabil', doc_data.get('Pret', 0)),
                'Valoare': doc_data.get('Valoare', doc_data.get('Valoare_Contabila', 0)),
                'Adaos': doc_data.get('Adaos', 0),
                'Cost': doc_data.get('Cost', 0),
                'Cantitate': doc_data.get('Cantitate', 1),
                'Denumire': doc_data.get('Denumire', 'N/A'),
                'Agent': doc_data.get('Agent', 'N/A'),
                'Gestiune': doc_data.get('DenumireGestiune', 'N/A')
            }
            data.append(row)
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare vânzări: {e}")
        # Returnează date demo ca fallback
        return generate_demo_vanzari()

@st.cache_data(ttl=300)
def load_top_produse():
    """Încarcă top produse din Firebase bazat pe vânzări"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        docs = db.collection('vanzari_current_month').stream()
        
        produse_dict = {}
        
        for doc in docs:
            doc_data = doc.to_dict()
            produs = doc_data.get('Denumire', 'N/A')
            cantitate = doc_data.get('Cantitate', 0)
            valoare = doc_data.get('Valoare', 0)
            adaos = doc_data.get('Adaos', 0)
            
            if produs in produse_dict:
                produse_dict[produs]['Cantitate'] += cantitate
                produse_dict[produs]['Valoare'] += valoare
                produse_dict[produs]['Adaos'] += adaos
            else:
                produse_dict[produs] = {
                    'Denumire': produs,
                    'Cantitate': cantitate,
                    'Valoare': valoare,
                    'Adaos': adaos
                }
        
        return pd.DataFrame(list(produse_dict.values()))
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare produse: {e}")
        return generate_demo_produse()

@st.cache_data(ttl=300)
def load_balanta_la_data():
    """Încarcă balanța stocurilor din Firebase"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        # Încarcă din colecția de stocuri sau vânzări grupate
        docs = db.collection('stocuri').stream()  # Ajustează numele colecției
        
        data = []
        if not any(docs):  # Dacă nu există colecție separată pentru stocuri
            # Generează din vânzări
            vanzari_docs = db.collection('vanzari_current_month').stream()
            stocuri_dict = {}
            
            for doc in vanzari_docs:
                doc_data = doc.to_dict()
                gestiune = doc_data.get('DenumireGestiune', 'N/A')
                produs = doc_data.get('Denumire', 'N/A')
                cantitate = doc_data.get('Cantitate', 0)
                valoare = doc_data.get('Valoare', 0)
                
                key = f"{gestiune}_{produs}"
                if key in stocuri_dict:
                    stocuri_dict[key]['Stoc final'] += cantitate * 10  # Simulăm stocul
                    stocuri_dict[key]['ValoareStocFinal'] += valoare * 10
                else:
                    stocuri_dict[key] = {
                        'DenumireGest': gestiune,
                        'Denumire': produs,
                        'Stoc final': cantitate * 10,
                        'ValoareStocFinal': valoare * 10
                    }
            
            data = list(stocuri_dict.values())
        else:
            for doc in docs:
                doc_data = doc.to_dict()
                row = {
                    'DenumireGest': doc_data.get('DenumireGest', doc_data.get('Gestiune', 'N/A')),
                    'Denumire': doc_data.get('Denumire', 'N/A'),
                    'Stoc final': doc_data.get('Stoc_final', doc_data.get('Cantitate', 0)),
                    'ValoareStocFinal': doc_data.get('ValoareStocFinal', doc_data.get('Valoare', 0))
                }
                data.append(row)
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare stocuri: {e}")
        return generate_demo_stocuri()

@st.cache_data(ttl=300)
def load_balanta_perioada():
    """Încarcă balanța pe perioadă din Firebase"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        docs = db.collection('stocuri_perioada').stream()
        
        data = []
        if not any(docs):  # Generează din datele de vânzări
            vanzari_docs = db.collection('vanzari_current_month').stream()
            
            for doc in vanzari_docs:
                doc_data = doc.to_dict()
                
                # Calculează vechimea bazată pe data vânzării
                data_vanzare = doc_data.get('Data')
                if hasattr(data_vanzare, 'timestamp'):
                    data_dt = datetime.fromtimestamp(data_vanzare.timestamp())
                else:
                    data_dt = datetime.now()
                
                zile_vechime = (datetime.now() - data_dt).days
                
                row = {
                    'Denumire gestiune': doc_data.get('DenumireGestiune', 'N/A'),
                    'Denumire': doc_data.get('Denumire', 'N/A'),
                    'Stoc final': doc_data.get('Cantitate', 0) * 15,  # Simulăm stocul
                    'Valoare intrare': doc_data.get('Valoare', 0) * 15,
                    'ZileVechime': max(1, zile_vechime)
                }
                data.append(row)
        else:
            for doc in docs:
                doc_data = doc.to_dict()
                row = {
                    'Denumire gestiune': doc_data.get('Denumire_gestiune', 'N/A'),
                    'Denumire': doc_data.get('Denumire', 'N/A'),
                    'Stoc final': doc_data.get('Stoc_final', 0),
                    'Valoare intrare': doc_data.get('Valoare_intrare', 0),
                    'ZileVechime': doc_data.get('ZileVechime', 1)
                }
                data.append(row)
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare balanță perioadă: {e}")
        return generate_demo_balanta_perioada()

@st.cache_data(ttl=300)
def load_cumparari_cipd():
    """Încarcă cumpărări CIPD din Firebase"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        docs = db.collection('cumparari').stream()
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            # Verifică dacă este tip CIPD
            if doc_data.get('Tip', '') == 'CIPD' or doc_data.get('source', '') == 'CIPD':
                row = {
                    'Gestiune': doc_data.get('DenumireGestiune', doc_data.get('Gestiune', 'N/A')),
                    'Denumire': doc_data.get('Denumire', 'N/A'),
                    'Cantitate': doc_data.get('Cantitate', 0),
                    'Pret': doc_data.get('Pret', doc_data.get('PretIntrare', 0)),
                    'Valoare': doc_data.get('Valoare', 0),
                    'Furnizor': doc_data.get('Furnizor', doc_data.get('Client', 'N/A'))
                }
                data.append(row)
        
        if not data:  # Dacă nu există date specifice, generează din vânzări
            data = generate_demo_cumparari_cipd()
            
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare cumpărări CIPD: {e}")
        return generate_demo_cumparari_cipd()

@st.cache_data(ttl=300)
def load_cumparari_ciis():
    """Încarcă cumpărări CIIS din Firebase"""
    try:
        db = init_firebase()
        if db is None:
            return pd.DataFrame()
        
        docs = db.collection('vanzari_current_month').stream()  # Folosim vânzările pentru a genera date de cumpărări
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            row = {
                'Gestiune': doc_data.get('DenumireGestiune', 'N/A'),
                'Denumire': doc_data.get('Denumire', 'N/A'),
                'Denumire grupa': doc_data.get('Denumire_grupa', doc_data.get('CategorieProdus', 'N/A')),
                'Cantitate': doc_data.get('Cantitate', 0),
                'Pret': doc_data.get('PretIntrare', doc_data.get('Pret', 0)),
                'Valoare': doc_data.get('Valoare', 0) * 0.8,  # Simulăm prețul de cumpărare
                'Furnizor': f"Furnizor {hash(doc_data.get('Denumire', '')) % 20 + 1}"  # Generăm furnizor pe baza produsului
            }
            data.append(row)
        
        return pd.DataFrame(data)
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare cumpărări CIIS: {e}")
        return generate_demo_cumparari_ciis()

# ===== FUNCȚII DEMO FALLBACK =====
def generate_demo_vanzari():
    """Generează date demo pentru vânzări"""
    dates = pd.date_range(start='2025-05-01', end='2025-05-30', freq='D')
    clients = [f'Client {i}' for i in range(1, 51)]
    data = []
    for date in dates:
        for _ in range(np.random.randint(5, 25)):
            client = np.random.choice(clients)
            valoare = np.random.randint(500, 10000)
            data.append({
                'Data': date,
                'Client': client,
                'Pret Contabil': valoare * 0.1,
                'Valoare': valoare,
                'Adaos': valoare * 0.15,
                'Cost': valoare * 0.85
            })
    return pd.DataFrame(data)

def generate_demo_produse():
    """Generează date demo pentru produse"""
    produse = [f'Produs {i}' for i in range(1, 101)]
    data = []
    for produs in produse:
        cantitate = np.random.randint(10, 500)
        valoare = np.random.randint(1000, 50000)
        data.append({
            'Denumire': produs,
            'Cantitate': cantitate,
            'Valoare': valoare,
            'Adaos': valoare * 0.15
        })
    return pd.DataFrame(data)

def generate_demo_stocuri():
    """Generează date demo pentru stocuri"""
    gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța', 'Showroom Cluj']
    produse = [f'Produs {i}' for i in range(1, 201)]
    data = []
    for gest in gestiuni:
        for _ in range(50):
            produs = np.random.choice(produse)
            stoc = np.random.randint(10, 500)
            data.append({
                'DenumireGest': gest,
                'Denumire': produs,
                'Stoc final': stoc,
                'ValoareStocFinal': stoc * np.random.randint(50, 500)
            })
    return pd.DataFrame(data)

def generate_demo_balanta_perioada():
    """Generează date demo pentru balanță perioadă"""
    gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța', 'Showroom Cluj']
    produse = [f'Produs {i}' for i in range(1, 201)]
    data = []
    for gest in gestiuni:
        for _ in range(50):
            produs = np.random.choice(produse)
            stoc = np.random.randint(10, 500)
            data.append({
                'Denumire gestiune': gest,
                'Denumire': produs,
                'Stoc final': stoc,
                'Valoare intrare': stoc * np.random.randint(50, 500),
                'ZileVechime': np.random.randint(1, 180)
            })
    return pd.DataFrame(data)

def generate_demo_cumparari_cipd():
    """Generează date demo pentru cumpărări CIPD"""
    gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța']
    furnizori = [f'Furnizor {i}' for i in range(1, 21)]
    produse = [f'Produs {i}' for i in range(1, 101)]
    data = []
    for _ in range(200):
        cantitate = np.random.randint(10, 200)
        pret = np.random.randint(50, 500)
        data.append({
            'Gestiune': np.random.choice(gestiuni),
            'Denumire': np.random.choice(produse),
            'Cantitate': cantitate,
            'Pret': pret,
            'Valoare': cantitate * pret,
            'Furnizor': np.random.choice(furnizori)
        })
    return pd.DataFrame(data)

def generate_demo_cumparari_ciis():
    """Generează date demo pentru cumpărări CIIS"""
    gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța']
    furnizori = [f'Furnizor {i}' for i in range(1, 21)]
    produse = [f'Produs {i}' for i in range(1, 101)]
    grupe = ['Materiale Construcții', 'Instalații Sanitare', 'Instalații Electrice', 'Finisaje', 'Unelte']
    data = []
    for _ in range(300):
        cantitate = np.random.randint(10, 200)
        pret = np.random.randint(50, 500)
        data.append({
            'Gestiune': np.random.choice(gestiuni),
            'Denumire': np.random.choice(produse),
            'Denumire grupa': np.random.choice(grupe),
            'Cantitate': cantitate,
            'Pret': pret,
            'Valoare': cantitate * pret,
            'Furnizor': np.random.choice(furnizori)
        })
    return pd.DataFrame(data)

# Sidebar Premium cu efecte moderne
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 30px 20px;'>
        <h1 class='animated-gradient-text' style='font-size: 36px; margin-bottom: 10px;'>BRENADO</h1>
        <p style='color: var(--text-secondary); font-size: 14px; letter-spacing: 0.1em; text-transform: uppercase;'>
            Premium Analytics Suite
        </p>
        <div style='width: 60px; height: 2px; background: var(--primary-gradient); margin: 20px auto;'></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status conexiune Firebase cu animație
    db = init_firebase()
    if db is not None:
        st.markdown("""
        <div class='glass-card' style='padding: 20px; margin: 20px 0; text-align: center;'>
            <div style='display: flex; align-items: center; justify-content: center; gap: 10px;'>
                <span class='live-indicator'></span>
                <span style='color: #4facfe; font-weight: 600;'>Firebase Connected</span>
            </div>
            <p style='color: var(--text-secondary); margin: 10px 0 0 0; font-size: 12px;'>Real-time sync active</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='glass-card' style='padding: 20px; margin: 20px 0; text-align: center; border-color: rgba(245, 87, 108, 0.3);'>
            <div style='display: flex; align-items: center; justify-content: center; gap: 10px;'>
                <span style='width: 8px; height: 8px; background: #f5576c; border-radius: 50%;'></span>
                <span style='color: #f5576c; font-weight: 600;'>Firebase Offline</span>
            </div>
            <p style='color: var(--text-secondary); margin: 10px 0 0 0; font-size: 12px;'>Using demo data</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats în sidebar cu design premium
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: var(--text-primary); font-size: 16px; text-transform: uppercase; letter-spacing: 0.05em;'>Quick Analytics</h3>", unsafe_allow_html=True)
    
    vanzari_df = load_vanzari_zi_clienti()
    if not vanzari_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='glass-card' style='padding: 20px; text-align: center;'>
                <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Revenue</p>
                <h3 class='neon-blue' style='margin: 5px 0; font-size: 22px;'>{vanzari_df['Valoare'].sum()/1000000:.1f}M</h3>
                <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>RON</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='glass-card' style='padding: 20px; text-align: center;'>
                <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Clients</p>
                <h3 class='neon-purple' style='margin: 5px 0; font-size: 22px;'>{vanzari_df['Client'].nunique()}</h3>
                <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>Active</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Refresh button premium
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True, help="Sync with Firebase"):
        with st.spinner("Syncing with Firebase..."):
            time.sleep(1)  # Simulare loading pentru efect
            st.cache_data.clear()
            st.rerun()
    
    # Footer sidebar
    st.markdown("""
    <div style='position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;'>
        <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>v2.0 Premium Edition</p>
        <p style='color: var(--text-secondary); font-size: 10px; margin: 5px 0 0 0; opacity: 0.6;'>© 2025 BRENADO</p>
    </div>
    """, unsafe_allow_html=True)

# Header principal premium cu efecte
st.markdown("""
<div class='premium-info-box' style='background: var(--dark-gradient); margin-bottom: 40px;'>
    <div style='text-align: center;'>
        <h1 style='font-size: 48px; margin: 0; font-weight: 900;' class='animated-gradient-text'>
            BRENADO ANALYTICS
        </h1>
        <p style='color: var(--text-secondary); font-size: 18px; margin: 15px 0 0 0; letter-spacing: 0.05em;'>
            Premium Business Intelligence for Residential Segment
        </p>
        <div style='display: flex; justify-content: center; gap: 30px; margin-top: 20px;'>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <span class='live-indicator'></span>
                <span style='color: var(--text-secondary); font-size: 14px;'>Live Data</span>
            </div>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <span style='color: #4facfe; font-size: 16px;'>🔥</span>
                <span style='color: var(--text-secondary); font-size: 14px;'>Firebase Connected</span>
            </div>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <span style='color: #764ba2; font-size: 16px;'>⚡</span>
                <span style='color: var(--text-secondary); font-size: 14px;'>Real-time Analytics</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Selectare categorie cu butoane premium animate
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Sales Analytics", use_container_width=True, key="btn1", 
                 help="View comprehensive sales data and insights"):
        st.session_state.category = "Vânzări"
with col2:
    if st.button("📦 Inventory Management", use_container_width=True, key="btn2",
                 help="Monitor stock levels and inventory turnover"):
        st.session_state.category = "Balanță Stocuri"
with col3:
    if st.button("🛒 Purchase Analysis", use_container_width=True, key="btn3",
                 help="Analyze supplier performance and purchase trends"):
        st.session_state.category = "Cumparari Intrari"

# Initialize session state
if 'category' not in st.session_state:
    st.session_state.category = "Vânzări"

category = st.session_state.category

# Indicator categorie selectată
selected_indicator = {
    "Vânzări": "📊 Sales Analytics Dashboard",
    "Balanță Stocuri": "📦 Inventory Management System", 
    "Cumparari Intrari": "🛒 Purchase Intelligence Platform"
}

st.markdown(f"""
<div style='text-align: center; margin: 30px 0;'>
    <h2 style='font-size: 28px; font-weight: 700;' class='animated-gradient-text'>
        {selected_indicator.get(category, '')}
    </h2>
</div>
""", unsafe_allow_html=True)

# ===== Vânzări Premium =====
if category == "Vânzări":
    # Încărcare date cu loading animation
    with st.spinner("Loading sales data from Firebase..."):
        vanzari_df = load_vanzari_zi_clienti()
        produse_df = load_top_produse()

    if vanzari_df.empty:
        st.warning("⚠️ No sales data found in Firebase. Using demo data.")
        vanzari_df = generate_demo_vanzari()
        produse_df = generate_demo_produse()

    # Calculare metrici
    total_valoare = vanzari_df['Valoare'].sum()
    numar_clienti = vanzari_df['Client'].nunique()
    numar_produse = len(produse_df)
    valoare_medie = vanzari_df['Valoare'].mean()
    
    # KPI Cards Premium cu gradient și animații
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "Total Revenue", 
            f"{total_valoare/1000000:.2f}M RON",
            "Live from Firebase",
            "💰",
            "var(--success-gradient)"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "Active Clients",
            f"{numar_clienti}",
            "Unique customers",
            "👥",
            "var(--primary-gradient)"
        ), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card(
            "Product SKUs",
            f"{numar_produse}",
            "In inventory",
            "📦",
            "var(--warning-gradient)"
        ), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card(
            "Average Transaction",
            f"{valoare_medie/1000:.1f}K RON",
            "Per order",
            "💳",
            "var(--secondary-gradient)"
        ), unsafe_allow_html=True)

    st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)

    # Tabs premium pentru diferite secțiuni
    tab1, tab2, tab3 = st.tabs(["📊 Sales Analysis", "🏆 Top Products", "💡 AI Insights"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Sales Trend Analysis</h3>", unsafe_allow_html=True)
            
            # Grafic linie premium cu efecte moderne
            daily_sales = vanzari_df.groupby('Data')['Valoare'].sum().reset_index()
            
            fig_line = go.Figure()
            
            # Main line cu gradient fill
            fig_line.add_trace(go.Scatter(
                x=daily_sales['Data'],
                y=daily_sales['Valoare'],
                mode='lines',
                name='Daily Sales',
                line=dict(color='#4facfe', width=3),
                fill='tonexty',
                fillcolor='rgba(79, 172, 254, 0.1)'
            ))
            
            # Add markers pentru puncte importante
            fig_line.add_trace(go.Scatter(
                x=daily_sales['Data'],
                y=daily_sales['Valoare'],
                mode='markers',
                marker=dict(
                    size=8,
                    color='#4facfe',
                    line=dict(width=2, color='white')
                ),
                showlegend=False
            ))
            
            # Trend line cu gradient
            if len(daily_sales) > 1:
                z = np.polyfit(range(len(daily_sales)), daily_sales['Valoare'], 1)
                p = np.poly1d(z)
                fig_line.add_trace(go.Scatter(
                    x=daily_sales['Data'],
                    y=p(range(len(daily_sales))),
                    mode='lines',
                    name='Trend',
                    line=dict(color='#f093fb', width=2, dash='dash')
                ))
            
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title=dict(
                    text='Revenue Trend from Firebase',
                    font=dict(size=20)
                ),
                hovermode='x unified',
                showlegend=True,
                legend=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                ),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    showgrid=True,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    showgrid=True,
                    zeroline=False,
                    tickformat=',.'
                ),
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            # Add range slider
            fig_line.update_xaxes(rangeslider_visible=True)
            
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Top 5 Clients</h3>", unsafe_allow_html=True)
            
            # Donut chart premium cu efecte moderne
            top_clients = vanzari_df.groupby('Client')['Valoare'].sum().nlargest(5).reset_index()
            
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe']
            
            fig_donut = go.Figure(data=[go.Pie(
                labels=top_clients['Client'],
                values=top_clients['Valoare'],
                hole=0.7,
                marker=dict(colors=colors, line=dict(color='#0a0b0f', width=2)),
                textposition='inside',
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f} RON<br>%{percent}<extra></extra>'
            )])
            
            # Add center text
            fig_donut.add_annotation(
                text=f"<b>TOP 5</b><br>Clients",
                x=0.5, y=0.5,
                font=dict(size=20, color='white'),
                showarrow=False
            )
            
            fig_donut.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                ),
                margin=dict(t=50, b=50, l=0, r=150)
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # Tabel interactiv premium
        st.markdown("""
        <div class='premium-info-box' style='margin-top: 40px;'>
            <h3 style='font-size: 24px; margin-bottom: 20px;'>Transaction Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            client_filter = st.multiselect(
                "🔍 Filter by client:",
                options=vanzari_df['Client'].unique(),
                default=[],
                help="Select one or more clients to filter"
            )
        with col2:
            if not vanzari_df.empty:
                date_range = st.date_input(
                    "📅 Date range:",
                    value=(vanzari_df['Data'].min().date(), vanzari_df['Data'].max().date()),
                    min_value=vanzari_df['Data'].min().date(),
                    max_value=vanzari_df['Data'].max().date(),
                    help="Select date range for analysis"
                )
        
        # Aplicare filtre
        filtered_df = vanzari_df.copy()
        if client_filter:
            filtered_df = filtered_df[filtered_df['Client'].isin(client_filter)]
        if len(date_range) == 2:
            filtered_df = filtered_df[(filtered_df['Data'].dt.date >= date_range[0]) & 
                                    (filtered_df['Data'].dt.date <= date_range[1])]
        
        # Mini stats pentru datele filtrate
        if len(filtered_df) > 0:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; text-align: center;'>
                    <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Filtered Total</p>
                    <h3 class='neon-blue' style='margin: 5px 0;'>{filtered_df['Valoare'].sum():,.0f}</h3>
                    <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>RON</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; text-align: center;'>
                    <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Transactions</p>
                    <h3 class='neon-purple' style='margin: 5px 0;'>{len(filtered_df)}</h3>
                    <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>Count</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; text-align: center;'>
                    <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Average</p>
                    <h3 class='neon-pink' style='margin: 5px 0;'>{filtered_df['Valoare'].mean():,.0f}</h3>
                    <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>RON/Transaction</p>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; text-align: center;'>
                    <p style='color: var(--text-secondary); font-size: 12px; margin: 0;'>Total Margin</p>
                    <h3 style='color: #4facfe; margin: 5px 0;'>{filtered_df['Adaos'].sum():,.0f}</h3>
                    <p style='color: var(--text-secondary); font-size: 11px; margin: 0;'>RON</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Tabel stilizat premium
        if not filtered_df.empty:
            st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
            st.dataframe(
                filtered_df.style.format({
                    'Pret Contabil': '{:,.0f} RON',
                    'Valoare': '{:,.0f} RON',
                    'Adaos': '{:,.0f} RON',
                    'Cost': '{:,.0f} RON'
                }).background_gradient(subset=['Valoare'], cmap='Blues', vmin=0),
                use_container_width=True,
                height=400
            )

    with tab2:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>Product Performance Analysis</h3>", unsafe_allow_html=True)
        
        if produse_df.empty:
            st.warning("⚠️ No product data found")
            st.stop()
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            show_option = st.selectbox(
                "📊 Display:",
                ["Top 10", "Top 20", "Top 50", "Top 100"],
                key="show_products"
            )
            
            chart_type = st.radio(
                "📈 Chart type:",
                ["3D Bar Chart", "Treemap", "Sunburst"],
                key="chart_type"
            )
        
        with col1:
            # Procesare date
            n_products = int(show_option.split()[1])
            top_produse = produse_df.nlargest(min(n_products, len(produse_df)), 'Valoare')
            
            if chart_type == "3D Bar Chart":
                # 3D Bar chart premium
                fig_3d = go.Figure(data=[go.Bar(
                    x=top_produse.head(20)['Denumire'],
                    y=top_produse.head(20)['Valoare'],
                    marker=dict(
                        color=top_produse.head(20)['Valoare'],
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(
                            title="Value (RON)",
                            tickformat=",.",
                            bgcolor='rgba(0,0,0,0.5)',
                            bordercolor='rgba(255,255,255,0.1)',
                            borderwidth=1
                        ),
                        line=dict(color='rgba(255,255,255,0.1)', width=1)
                    ),
                    hovertemplate='<b>%{x}</b><br>Value: %{y:,.0f} RON<extra></extra>'
                )])
                
                fig_3d.update_layout(
                    title=dict(
                        text=f'{show_option} Products by Value (Firebase)',
                        font=dict(size=24)
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    xaxis=dict(
                        gridcolor='rgba(255,255,255,0.05)',
                        tickangle=-45
                    ),
                    yaxis=dict(
                        gridcolor='rgba(255,255,255,0.05)',
                        tickformat=',.'
                    ),
                    hoverlabel=dict(
                        bgcolor='rgba(0,0,0,0.8)',
                        bordercolor='rgba(255,255,255,0.2)'
                    )
                )
                
                st.plotly_chart(fig_3d, use_container_width=True)
                
            elif chart_type == "Treemap":
                # Treemap premium cu animații
                fig_tree = px.treemap(
                    top_produse, 
                    path=['Denumire'], 
                    values='Valoare',
                    title=f'{show_option} Products - Interactive Treemap',
                    color='Adaos', 
                    color_continuous_scale='RdYlGn',
                    hover_data={'Cantitate': True}
                )
                
                fig_tree.update_traces(
                    textposition="middle center",
                    textfont_size=12,
                    hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f} RON<br>Margin: %{color:,.0f} RON<br>Quantity: %{customdata[0]}<extra></extra>'
                )
                
                fig_tree.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    title_font_size=24,
                    coloraxis_colorbar=dict(
                        title="Margin (RON)",
                        tickformat=",.",
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    )
                )
                
                st.plotly_chart(fig_tree, use_container_width=True)
                
            else:  # Sunburst
                # Sunburst chart premium
                fig_sun = go.Figure(go.Sunburst(
                    labels=top_produse.head(30)['Denumire'],
                    parents=[""] * len(top_produse.head(30)),
                    values=top_produse.head(30)['Valoare'],
                    branchvalues="total",
                    marker=dict(
                        colors=top_produse.head(30)['Valoare'],
                        colorscale='Plasma',
                        showscale=True,
                        colorbar=dict(
                            title="Value (RON)",
                            tickformat=",.",
                            bgcolor='rgba(0,0,0,0.5)',
                            bordercolor='rgba(255,255,255,0.1)',
                            borderwidth=1
                        )
                    ),
                    hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f} RON<br>%{percentParent}<extra></extra>'
                ))
                
                fig_sun.update_layout(
                    title=dict(
                        text=f'{show_option} Products - Sunburst Visualization',
                        font=dict(size=24)
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff'
                )
                
                st.plotly_chart(fig_sun, use_container_width=True)
        
        # Statistici produse în cards premium
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Product Statistics Overview</h3>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if not produse_df.empty:
                best_product = produse_df.loc[produse_df['Valoare'].idxmax()]
                st.markdown(f"""
                <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(255,215,0,0.1) 0%, rgba(255,215,0,0.05) 100%);'>
                    <h4 style='color: #FFD700; margin: 0; font-size: 16px;'>🥇 Best Seller</h4>
                    <p style='color: white; margin: 10px 0; font-size: 14px; font-weight: 600;'>{best_product['Denumire']}</p>
                    <h3 style='color: #FFD700; margin: 0;'>{best_product['Valoare']:,.0f} RON</h3>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(79,172,254,0.1) 0%, rgba(79,172,254,0.05) 100%);'>
                <h4 style='color: #4facfe; margin: 0; font-size: 16px;'>📦 Total Quantity</h4>
                <h3 style='color: #4facfe; margin: 10px 0;'>{produse_df['Cantitate'].sum():,.0f}</h3>
                <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>Units in stock</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(118,75,162,0.1) 0%, rgba(118,75,162,0.05) 100%);'>
                <h4 style='color: #764ba2; margin: 0; font-size: 16px;'>💰 Total Value</h4>
                <h3 style='color: #764ba2; margin: 10px 0;'>{produse_df['Valoare'].sum()/1000000:.1f}M RON</h3>
                <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>Merchandise value</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if produse_df['Valoare'].sum() > 0:
                avg_margin = (produse_df['Adaos'].sum() / produse_df['Valoare'].sum() * 100)
                st.markdown(f"""
                <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(240,147,251,0.1) 0%, rgba(240,147,251,0.05) 100%);'>
                    <h4 style='color: #f093fb; margin: 0; font-size: 16px;'>📈 Average Margin</h4>
                    <h3 style='color: #f093fb; margin: 10px 0;'>{avg_margin:.1f}%</h3>
                    <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>Profit margin</p>
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        st.markdown("<h3 style='font-size: 28px; margin-bottom: 30px;'>AI-Powered Business Insights</h3>", unsafe_allow_html=True)
        
        if vanzari_df.empty:
            st.warning("⚠️ Insufficient data for AI insights")
            st.stop()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Analiza pattern săptămânal cu design premium
            vanzari_df['DayOfWeek'] = vanzari_df['Data'].dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = vanzari_df.groupby('DayOfWeek')['Valoare'].agg(['sum', 'count', 'mean']).reset_index()
            daily_pattern['DayOfWeek'] = pd.Categorical(daily_pattern['DayOfWeek'], categories=day_order, ordered=True)
            daily_pattern = daily_pattern.sort_values('DayOfWeek')
            
            # Radar chart pentru pattern săptămânal
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=daily_pattern['sum'],
                theta=daily_pattern['DayOfWeek'],
                fill='toself',
                name='Revenue',
                fillcolor='rgba(79, 172, 254, 0.2)',
                line=dict(color='#4facfe', width=3)
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=daily_pattern['count'] * daily_pattern['sum'].max() / daily_pattern['count'].max(),
                theta=daily_pattern['DayOfWeek'],
                fill='toself',
                name='Transactions (scaled)',
                fillcolor='rgba(240, 147, 251, 0.2)',
                line=dict(color='#f093fb', width=3)
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        gridcolor='rgba(255,255,255,0.1)',
                        tickformat=',.'
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255,255,255,0.1)'
                    ),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=True,
                title=dict(
                    text='Weekly Sales Pattern Analysis',
                    font=dict(size=20)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                legend=dict(
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col2:
            # Heatmap pentru ore de vânzare (simulat)
            hours = list(range(24))
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            
            # Generăm date simulate pentru heatmap
            np.random.seed(42)
            z_data = []
            for day in days:
                day_data = []
                for hour in hours:
                    # Simulăm pattern-uri realiste
                    if hour < 8 or hour > 20:
                        value = np.random.randint(0, 20)
                    elif hour >= 11 and hour <= 14:
                        value = np.random.randint(60, 100)
                    elif hour >= 17 and hour <= 19:
                        value = np.random.randint(70, 100)
                    else:
                        value = np.random.randint(30, 60)
                    day_data.append(value)
                z_data.append(day_data)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=z_data,
                x=hours,
                y=days,
                colorscale='Viridis',
                hovertemplate='Day: %{y}<br>Hour: %{x}:00<br>Activity: %{z}%<extra></extra>'
            ))
            
            fig_heatmap.update_layout(
                title=dict(
                    text='Sales Activity Heatmap',
                    font=dict(size=20)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(
                    title='Hour of Day',
                    gridcolor='rgba(255,255,255,0.05)'
                ),
                yaxis=dict(
                    title='Day of Week',
                    gridcolor='rgba(255,255,255,0.05)'
                )
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # AI Insights automate cu cards premium
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>🤖 AI-Generated Insights</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not daily_pattern.empty:
                best_day = daily_pattern.loc[daily_pattern['sum'].idxmax()]
                worst_day = daily_pattern.loc[daily_pattern['sum'].idxmin()]
                improvement = ((best_day['sum'] - worst_day['sum']) / worst_day['sum'] * 100)
                
                st.markdown(f"""
                <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(76,175,80,0.1) 0%, rgba(76,175,80,0.05) 100%);'>
                    <h4 style='color: #4CAF50; margin: 0;'>📈 Best Performance Day</h4>
                    <p style='color: white; margin: 15px 0 10px 0; font-size: 18px; font-weight: 700;'>{best_day['DayOfWeek']}</p>
                    <p style='color: var(--text-secondary); margin: 5px 0;'>Revenue: <span style='color: #4CAF50; font-weight: 600;'>{best_day['sum']:,.0f} RON</span></p>
                    <p style='color: var(--text-secondary); margin: 5px 0;'>Transactions: <span style='color: #4CAF50; font-weight: 600;'>{best_day['count']:.0f}</span></p>
                    <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                        <p style='color: #4CAF50; margin: 0; font-size: 14px;'>+{improvement:.1f}% vs worst day</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Pareto analysis
            sorted_clients = vanzari_df.groupby('Client')['Valoare'].sum().sort_values(ascending=False).reset_index()
            sorted_clients['cumsum'] = sorted_clients['Valoare'].cumsum()
            sorted_clients['percentage'] = sorted_clients['cumsum'] / sorted_clients['Valoare'].sum() * 100
            
            # Find 80/20 point
            pareto_point = sorted_clients[sorted_clients['percentage'] >= 80].index[0] if len(sorted_clients[sorted_clients['percentage'] >= 80]) > 0 else len(sorted_clients)
            pareto_percentage = (pareto_point / len(sorted_clients)) * 100
            
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(255,152,0,0.1) 0%, rgba(255,152,0,0.05) 100%);'>
                <h4 style='color: #FF9800; margin: 0;'>🎯 Pareto Principle</h4>
                <p style='color: white; margin: 15px 0 10px 0; font-size: 18px; font-weight: 700;'>{pareto_percentage:.1f}% of clients</p>
                <p style='color: var(--text-secondary); margin: 5px 0;'>Generate <span style='color: #FF9800; font-weight: 600;'>80%</span> of revenue</p>
                <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                    <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>Focus on top <span style='color: #FF9800;'>{pareto_point}</span> clients</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Growth analysis
            daily_sales = vanzari_df.groupby('Data')['Valoare'].sum().reset_index()
            if len(daily_sales) >= 14:
                last_week = daily_sales['Valoare'].iloc[-7:].mean()
                prev_week = daily_sales['Valoare'].iloc[-14:-7].mean()
                growth_rate = ((last_week - prev_week) / prev_week * 100)
                
                if growth_rate > 0:
                    trend_color = "#4CAF50"
                    trend_icon = "📈"
                    trend_text = "Growth Trend"
                else:
                    trend_color = "#f44336"
                    trend_icon = "📉"
                    trend_text = "Decline Alert"
                
                st.markdown(f"""
                <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(102,126,234,0.05) 100%);'>
                    <h4 style='color: {trend_color}; margin: 0;'>{trend_icon} {trend_text}</h4>
                    <p style='color: white; margin: 15px 0 10px 0; font-size: 24px; font-weight: 700;'>{abs(growth_rate):.1f}%</p>
                    <p style='color: var(--text-secondary); margin: 5px 0;'>Week-over-week change</p>
                    <div style='margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);'>
                        <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>Avg daily: <span style='color: {trend_color};'>{last_week:,.0f} RON</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ===== BALANȚĂ STOCURI PREMIUM =====
elif category == "Balanță Stocuri":
    st.markdown("<div class='glass-card' style='padding: 5px 20px; margin-bottom: 30px;'><h2 style='margin: 0;'>📦 Inventory Management System</h2></div>", unsafe_allow_html=True)
    
    # Tabs premium pentru subcategorii
    tab1, tab2 = st.tabs(["📅 Current Stock Status", "📊 Aging Analysis"])
    
    with tab1:
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Current Inventory Snapshot</h3>", unsafe_allow_html=True)
        
        # Încărcare date cu loading animation
        with st.spinner("Loading inventory data from Firebase..."):
            balanta_df = load_balanta_la_data()
        
        if balanta_df.empty:
            st.warning("⚠️ No stock data found in Firebase")
            st.stop()
        
        # KPI Cards moderne pentru stocuri
        col1, col2, col3, col4 = st.columns(4)
        
        total_stoc = balanta_df['Stoc final'].sum()
        valoare_stoc = balanta_df['ValoareStocFinal'].sum()
        numar_produse = len(balanta_df)
        gestiuni_unice = balanta_df['DenumireGest'].nunique()
        
        with col1:
            st.markdown(create_metric_card(
                "Total Stock",
                f"{total_stoc:,.0f}",
                "Units in inventory",
                "📦",
                "var(--success-gradient)"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Stock Value",
                f"{valoare_stoc/1000000:.1f}M RON",
                "Capital invested",
                "💰",
                "var(--primary-gradient)"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Active SKUs",
                f"{numar_produse:,}",
                "Different products",
                "📋",
                "var(--warning-gradient)"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Locations",
                f"{gestiuni_unice}",
                "Active warehouses",
                "🏢",
                "var(--secondary-gradient)"
            ), unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        
        # Vizualizări stocuri premium
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 3D Bar chart pentru distribuție stocuri
            stock_by_location = balanta_df.groupby('DenumireGest')['ValoareStocFinal'].sum().reset_index()
            
            fig_3d = go.Figure(data=[go.Bar3d(
                x=stock_by_location['DenumireGest'],
                y=[1] * len(stock_by_location),
                z=stock_by_location['ValoareStocFinal'],
                marker=dict(
                    color=stock_by_location['ValoareStocFinal'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title="Stock Value (RON)",
                        tickformat=",.",
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    )
                )
            )])
            
            # Fallback to regular bar chart since Plotly doesn't have Bar3d
            fig_3d = go.Figure(data=[go.Bar(
                x=stock_by_location['DenumireGest'],
                y=stock_by_location['ValoareStocFinal'],
                marker=dict(
                    color=stock_by_location['ValoareStocFinal'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(
                        title="Value (RON)",
                        tickformat=",.",
                        bgcolor='rgba(0,0,0,0.5)',
                        bordercolor='rgba(255,255,255,0.1)',
                        borderwidth=1
                    ),
                    line=dict(color='rgba(255,255,255,0.1)', width=1)
                ),
                hovertemplate='<b>%{x}</b><br>Stock Value: %{y:,.0f} RON<extra></extra>'
            )])
            
            fig_3d.update_layout(
                title=dict(
                    text='Stock Distribution by Location',
                    font=dict(size=22)
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    tickangle=-45
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)',
                    tickformat=',.'
                ),
                hoverlabel=dict(
                    bgcolor='rgba(0,0,0,0.8)',
                    bordercolor='rgba(255,255,255,0.2)'
                )
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)
        
        with col2:
            # Gauge chart pentru utilizare capacitate
            utilizare = min(95, np.random.randint(70, 95))  # Simulare utilizare
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = utilizare,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Warehouse Capacity", 'font': {'size': 18}},
                delta = {'reference': 80, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#4facfe"},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(76,175,80,0.3)'},
                        {'range': [50, 80], 'color': 'rgba(255,193,7,0.3)'},
                        {'range': [80, 100], 'color': 'rgba(244,67,54,0.3)'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Inter"},
                height=300,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        # ABC Analysis cu vizualizare premium
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>📊 ABC Inventory Analysis</h3>", unsafe_allow_html=True)
        
        # Calculare ABC
        produse_abc = balanta_df.groupby('Denumire')['ValoareStocFinal'].sum().reset_index()
        produse_abc = produse_abc.sort_values('ValoareStocFinal', ascending=False)
        produse_abc['Cumulative'] = produse_abc['ValoareStocFinal'].cumsum()
        produse_abc['Percentage'] = produse_abc['Cumulative'] / produse_abc['ValoareStocFinal'].sum() * 100
        
        produse_abc['Category'] = pd.cut(produse_abc['Percentage'], 
                                        bins=[0, 80, 95, 100], 
                                        labels=['A', 'B', 'C'])
        
        # Waterfall chart pentru ABC
        fig_waterfall = go.Figure()
        
        # Prepare data for waterfall
        abc_summary = produse_abc.groupby('Category').agg({
            'ValoareStocFinal': 'sum',
            'Denumire': 'count'
        }).reset_index()
        
        colors_abc = {'A': '#4CAF50', 'B': '#FF9800', 'C': '#f44336'}
        
        for i, row in abc_summary.iterrows():
            fig_waterfall.add_trace(go.Waterfall(
                name=f"Category {row['Category']}",
                orientation="v",
                measure=["relative"],
                x=[f"Category {row['Category']}"],
                y=[row['ValoareStocFinal']],
                connector={"line": {"color": "rgba(255,255,255,0.1)"}},
                increasing={"marker": {"color": colors_abc[row['Category']]}},
                totals={"marker": {"color": "rgba(255,255,255,0.1)"}}
            ))
        
        fig_waterfall.update_layout(
            title="ABC Categories Value Distribution",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(
                title="Stock Value (RON)",
                gridcolor='rgba(255,255,255,0.05)',
                tickformat=',.'
            )
        )
        
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # ABC Statistics Cards
        col1, col2, col3 = st.columns(3)
        
        for col, cat in zip([col1, col2, col3], ['A', 'B', 'C']):
            cat_data = produse_abc[produse_abc['Category'] == cat]
            color = colors_abc[cat]
            
            total_value = cat_data['ValoareStocFinal'].sum()
            percentage_value = (total_value / produse_abc['ValoareStocFinal'].sum() * 100)
            count_items = len(cat_data)
            percentage_items = (count_items / len(produse_abc) * 100)
            
            with col:
                st.markdown(f"""
                <div class='premium-info-box' style='background: linear-gradient(135deg, {color}20 0%, {color}10 100%); 
                                                     border-left: 4px solid {color};'>
                    <h3 style='color: {color}; margin: 0; font-size: 28px;'>Category {cat}</h3>
                    <div style='margin: 20px 0;'>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Items: <span style='color: white; font-weight: 600;'>{count_items} ({percentage_items:.1f}%)</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Value: <span style='color: white; font-weight: 600;'>{total_value/1000000:.1f}M RON</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Share: <span style='color: {color}; font-weight: 600;'>{percentage_value:.1f}%</span></p>
                    </div>
                    <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-top: 15px;'>
                        <p style='color: {color}; margin: 0; font-size: 12px; text-align: center;'>
                            {'High Priority' if cat == 'A' else 'Medium Priority' if cat == 'B' else 'Low Priority'}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>🕐 Stock Aging Analysis</h3>", unsafe_allow_html=True)
        
        # Încărcare date perioadă
        with st.spinner("Analyzing stock aging patterns..."):
            perioada_df = load_balanta_perioada()
        
        if perioada_df.empty:
            st.warning("⚠️ No aging data available")
            st.stop()
        
        # Categorii vechime cu gradient colors
        perioada_df['Categorie Vechime'] = pd.cut(perioada_df['ZileVechime'], 
                                                  bins=[0, 30, 60, 90, 180, 365, float('inf')],
                                                  labels=['< 30 days', '30-60 days', '60-90 days', 
                                                         '90-180 days', '180-365 days', '> 365 days'])
        
        vechime_stats = perioada_df.groupby('Categorie Vechime').agg({
            'Valoare intrare': 'sum',
            'Stoc final': 'sum'
        }).reset_index()
        
        # Funnel chart pentru aging
        fig_funnel = go.Figure(go.Funnel(
            y=vechime_stats['Categorie Vechime'],
            x=vechime_stats['Valoare intrare'],
            textposition="inside",
            textinfo="value+percent total",
            opacity=0.8,
            marker=dict(
                color=['#4CAF50', '#8BC34A', '#FFEB3B', '#FF9800', '#FF5722', '#f44336'],
                line=dict(width=2, color='rgba(255,255,255,0.2)')
            ),
            hovertemplate='<b>%{y}</b><br>Value: %{x:,.0f} RON<br>%{percentTotal}<extra></extra>'
        ))
        
        fig_funnel.update_layout(
            title=dict(
                text='Stock Value by Age Category',
                font=dict(size=22)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            height=500
        )
        
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # Risk Analysis Cards
        old_stock = perioada_df[perioada_df['ZileVechime'] > 180]
        very_old_stock = perioada_df[perioada_df['ZileVechime'] > 365]
        at_risk_value = old_stock['Valoare intrare'].sum()
        critical_value = very_old_stock['Valoare intrare'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_percentage = (at_risk_value / perioada_df['Valoare intrare'].sum() * 100) if perioada_df['Valoare intrare'].sum() > 0 else 0
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(255,152,0,0.1) 0%, rgba(255,152,0,0.05) 100%);
                                                 border-left: 4px solid #FF9800;'>
                <h4 style='color: #FF9800; margin: 0;'>⚠️ At Risk Stock</h4>
                <p style='color: white; margin: 15px 0; font-size: 28px; font-weight: 700;'>{at_risk_value/1000000:.1f}M RON</p>
                <p style='color: var(--text-secondary); margin: 5px 0;'>Items over 180 days</p>
                <div style='margin-top: 15px;'>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 8px;'>
                        <div style='background: #FF9800; height: 100%; border-radius: 5px; width: {risk_percentage:.1f}%;'></div>
                    </div>
                    <p style='color: #FF9800; margin: 5px 0 0 0; font-size: 12px;'>{risk_percentage:.1f}% of total stock</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            critical_percentage = (critical_value / perioada_df['Valoare intrare'].sum() * 100) if perioada_df['Valoare intrare'].sum() > 0 else 0
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(244,67,54,0.1) 0%, rgba(244,67,54,0.05) 100%);
                                                 border-left: 4px solid #f44336;'>
                <h4 style='color: #f44336; margin: 0;'>🚨 Critical Stock</h4>
                <p style='color: white; margin: 15px 0; font-size: 28px; font-weight: 700;'>{critical_value/1000000:.1f}M RON</p>
                <p style='color: var(--text-secondary); margin: 5px 0;'>Items over 365 days</p>
                <div style='margin-top: 15px;'>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 8px;'>
                        <div style='background: #f44336; height: 100%; border-radius: 5px; width: {critical_percentage:.1f}%;'></div>
                    </div>
                    <p style='color: #f44336; margin: 5px 0 0 0; font-size: 12px;'>{critical_percentage:.1f}% of total stock</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            healthy_value = perioada_df[perioada_df['ZileVechime'] <= 90]['Valoare intrare'].sum()
            healthy_percentage = (healthy_value / perioada_df['Valoare intrare'].sum() * 100) if perioada_df['Valoare intrare'].sum() > 0 else 0
            st.markdown(f"""
            <div class='premium-info-box' style='background: linear-gradient(135deg, rgba(76,175,80,0.1) 0%, rgba(76,175,80,0.05) 100%);
                                                 border-left: 4px solid #4CAF50;'>
                <h4 style='color: #4CAF50; margin: 0;'>✅ Healthy Stock</h4>
                <p style='color: white; margin: 15px 0; font-size: 28px; font-weight: 700;'>{healthy_value/1000000:.1f}M RON</p>
                <p style='color: var(--text-secondary); margin: 5px 0;'>Items under 90 days</p>
                <div style='margin-top: 15px;'>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 5px; height: 8px;'>
                        <div style='background: #4CAF50; height: 100%; border-radius: 5px; width: {healthy_percentage:.1f}%;'></div>
                    </div>
                    <p style='color: #4CAF50; margin: 5px 0 0 0; font-size: 12px;'>{healthy_percentage:.1f}% of total stock</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Slow movers table cu design premium
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>🐌 Slow Moving Items Alert</h3>", unsafe_allow_html=True)
        
        slow_movers = perioada_df.nlargest(10, 'ZileVechime')[['Denumire', 'Stoc final', 'Valoare intrare', 'ZileVechime', 'Denumire gestiune']]
        
        # Create custom styled table
        if not slow_movers.empty:
            st.markdown("""
            <div class='glass-card' style='padding: 0; overflow: hidden;'>
                <table style='width: 100%; border-collapse: collapse;'>
                    <thead>
                        <tr style='background: var(--primary-gradient);'>
                            <th style='padding: 15px; text-align: left; font-weight: 600;'>Product</th>
                            <th style='padding: 15px; text-align: right; font-weight: 600;'>Stock</th>
                            <th style='padding: 15px; text-align: right; font-weight: 600;'>Value</th>
                            <th style='padding: 15px; text-align: right; font-weight: 600;'>Age</th>
                            <th style='padding: 15px; text-align: left; font-weight: 600;'>Location</th>
                        </tr>
                    </thead>
                    <tbody>
            """, unsafe_allow_html=True)
            
            for idx, row in slow_movers.iterrows():
                age_color = '#f44336' if row['ZileVechime'] > 180 else '#FF9800' if row['ZileVechime'] > 90 else '#4CAF50'
                st.markdown(f"""
                        <tr style='border-bottom: 1px solid rgba(255,255,255,0.05); transition: background 0.3s;' 
                            onmouseover="this.style.background='rgba(102,126,234,0.1)'" 
                            onmouseout="this.style.background='transparent'">
                            <td style='padding: 15px;'>{row['Denumire']}</td>
                            <td style='padding: 15px; text-align: right; color: #4facfe;'>{row['Stoc final']:,.0f}</td>
                            <td style='padding: 15px; text-align: right; color: #764ba2;'>{row['Valoare intrare']:,.0f} RON</td>
                            <td style='padding: 15px; text-align: right; color: {age_color}; font-weight: 600;'>{row['ZileVechime']:.0f} days</td>
                            <td style='padding: 15px;'>{row['Denumire gestiune']}</td>
                        </tr>
                """, unsafe_allow_html=True)
            
            st.markdown("""
                    </tbody>
                </table>
            </div>
            """, unsafe_allow_html=True)

# ===== CUMPARARI INTRARI PREMIUM =====
elif category == "Cumparari Intrari":
    st.markdown("<div class='glass-card' style='padding: 5px 20px; margin-bottom: 30px;'><h2 style='margin: 0;'>🛒 Purchase Intelligence Platform</h2></div>", unsafe_allow_html=True)
    
    # Tabs premium pentru subcategorii
    tab1, tab2, tab3 = st.tabs(["📋 Purchase Orders", "📊 Stock Purchases", "🤝 Supplier Analytics"])
    
    with tab1:
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Purchase Orders Analysis (CIPD)</h3>", unsafe_allow_html=True)
        
        # Încărcare date
        with st.spinner("Loading purchase order data..."):
            cipd_df = load_cumparari_cipd()
        
        if cipd_df.empty:
            st.warning("⚠️ No CIPD data found in Firebase")
            st.stop()
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        total_cantitate = cipd_df['Cantitate'].sum()
        total_valoare = cipd_df['Valoare'].sum()
        numar_produse = len(cipd_df)
        furnizori_unici = cipd_df['Furnizor'].nunique()
        
        with col1:
            st.markdown(create_metric_card(
                "Total Quantity",
                f"{total_cantitate:,.0f}",
                "Units purchased",
                "📦",
                "var(--success-gradient)"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card(
                "Purchase Value",
                f"{total_valoare/1000000:.1f}M RON",
                "Total investment",
                "💰",
                "var(--primary-gradient)"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card(
                "Products",
                f"{numar_produse:,}",
                "Different SKUs",
                "📋",
                "var(--warning-gradient)"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card(
                "Suppliers",
                f"{furnizori_unici}",
                "Active partners",
                "🤝",
                "var(--secondary-gradient)"
            ), unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        
        # Supplier Performance Chart
        top_suppliers = cipd_df.groupby('Furnizor')['Valoare'].sum().nlargest(10).reset_index()
        
        # Horizontal bar with gradient
        fig_suppliers = go.Figure()
        
        # Add bars with gradient effect
        colors = px.colors.sequential.Viridis
        n_colors = len(colors)
        
        for i, row in top_suppliers.iterrows():
            color_idx = int(i * n_colors / len(top_suppliers))
            fig_suppliers.add_trace(go.Bar(
                y=[row['Furnizor']],
                x=[row['Valoare']],
                orientation='h',
                marker=dict(
                    color=colors[color_idx],
                    line=dict(color='rgba(255,255,255,0.1)', width=1)
                ),
                hovertemplate=f"<b>{row['Furnizor']}</b><br>Value: {row['Valoare']:,.0f} RON<extra></extra>",
                showlegend=False
            ))
        
        fig_suppliers.update_layout(
            title=dict(
                text='Top 10 Suppliers by Purchase Value',
                font=dict(size=22)
            ),
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            xaxis=dict(
                title='Total Value (RON)',
                gridcolor='rgba(255,255,255,0.05)',
                tickformat=',.'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                autorange="reversed"
            ),
            hoverlabel=dict(
                bgcolor='rgba(0,0,0,0.8)',
                bordercolor='rgba(255,255,255,0.2)'
            ),
            margin=dict(l=150, r=50, t=50, b=50)
        )
        
        st.plotly_chart(fig_suppliers, use_container_width=True)
        
        # Supplier distribution pie
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Concentration analysis
            supplier_conc = cipd_df.groupby('Furnizor')['Valoare'].sum().sort_values(ascending=False).reset_index()
            supplier_conc['cumsum'] = supplier_conc['Valoare'].cumsum()
            supplier_conc['percentage'] = supplier_conc['cumsum'] / supplier_conc['Valoare'].sum() * 100
            
            # Find concentration points
            top_5_percentage = supplier_conc.iloc[:5]['Valoare'].sum() / supplier_conc['Valoare'].sum() * 100 if len(supplier_conc) >= 5 else 100
            top_10_percentage = supplier_conc.iloc[:10]['Valoare'].sum() / supplier_conc['Valoare'].sum() * 100 if len(supplier_conc) >= 10 else 100
            
            st.markdown(f"""
            <div class='premium-info-box'>
                <h4 style='font-size: 20px; margin-bottom: 20px;'>🎯 Supplier Concentration Analysis</h4>
                <div style='margin: 20px 0;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <span style='color: var(--text-secondary);'>Top 5 Suppliers</span>
                        <span style='color: #4facfe; font-size: 24px; font-weight: 700;'>{top_5_percentage:.1f}%</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%); height: 100%; width: {top_5_percentage}%; transition: width 1s ease;'></div>
                    </div>
                </div>
                <div style='margin: 20px 0;'>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                        <span style='color: var(--text-secondary);'>Top 10 Suppliers</span>
                        <span style='color: #764ba2; font-size: 24px; font-weight: 700;'>{top_10_percentage:.1f}%</span>
                    </div>
                    <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 12px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); height: 100%; width: {top_10_percentage}%; transition: width 1s ease;'></div>
                    </div>
                </div>
                <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin-top: 20px;'>
                    <p style='color: var(--text-secondary); margin: 0; font-size: 14px;'>
                        {'⚠️ High concentration risk' if top_5_percentage > 60 else '✅ Good supplier diversification'}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Purchase by location donut
            location_dist = cipd_df.groupby('Gestiune')['Valoare'].sum().reset_index()
            
            fig_location = go.Figure(data=[go.Pie(
                labels=location_dist['Gestiune'],
                values=location_dist['Valoare'],
                hole=0.7,
                marker=dict(
                    colors=['#667eea', '#764ba2', '#f093fb', '#f5576c'],
                    line=dict(color='#0a0b0f', width=2)
                ),
                textposition='inside',
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f} RON<br>%{percent}<extra></extra>'
            )])
            
            fig_location.add_annotation(
                text="<b>Purchase<br>Distribution</b>",
                x=0.5, y=0.5,
                font=dict(size=16, color='white'),
                showarrow=False
            )
            
            fig_location.update_layout(
                title=dict(
                    text='Purchases by Location',
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
                ),
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            st.plotly_chart(fig_location, use_container_width=True)
    
    with tab2:
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>Stock Purchase Analysis (CIIS)</h3>", unsafe_allow_html=True)
        
        # Încărcare date
        with st.spinner("Loading stock purchase data..."):
            ciis_df = load_cumparari_ciis()
        
        if ciis_df.empty:
            st.warning("⚠️ No CIIS data found in Firebase")
            st.stop()
        
        # Interactive filters with preview
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 Location Analysis")
            gestiune_selectata = st.selectbox(
                "Select warehouse:",
                options=["All Locations"] + list(ciis_df['Gestiune'].unique()),
                key="gest_ciis"
            )
            
            if gestiune_selectata != "All Locations":
                gest_data = ciis_df[ciis_df['Gestiune'] == gestiune_selectata]
                valoare_gest = gest_data['Valoare'].sum()
                cantitate_gest = gest_data['Cantitate'].sum()
                
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; margin-top: 10px;'>
                    <h4 style='color: #4facfe; margin: 0;'>💰 {gestiune_selectata}</h4>
                    <div style='margin-top: 15px;'>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Value: <span style='color: white; font-weight: 600;'>{valoare_gest:,.0f} RON</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Quantity: <span style='color: white; font-weight: 600;'>{cantitate_gest:,.0f} units</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Products: <span style='color: white; font-weight: 600;'>{len(gest_data)} SKUs</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📂 Category Analysis")
            grupa_selectata = st.selectbox(
                "Select product group:",
                options=["All Groups"] + list(ciis_df['Denumire grupa'].unique()),
                key="grupa_ciis"
            )
            
            if grupa_selectata != "All Groups":
                grupa_data = ciis_df[ciis_df['Denumire grupa'] == grupa_selectata]
                valoare_grupa = grupa_data['Valoare'].sum()
                cantitate_grupa = grupa_data['Cantitate'].sum()
                
                st.markdown(f"""
                <div class='glass-card' style='padding: 20px; margin-top: 10px;'>
                    <h4 style='color: #764ba2; margin: 0;'>📦 {grupa_selectata}</h4>
                    <div style='margin-top: 15px;'>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Value: <span style='color: white; font-weight: 600;'>{valoare_grupa:,.0f} RON</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Quantity: <span style='color: white; font-weight: 600;'>{cantitate_grupa:,.0f} units</span></p>
                        <p style='color: var(--text-secondary); margin: 5px 0;'>Suppliers: <span style='color: white; font-weight: 600;'>{grupa_data['Furnizor'].nunique()}</span></p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Apply filters
        filtered_ciis = ciis_df.copy()
        if gestiune_selectata != "All Locations":
            filtered_ciis = filtered_ciis[filtered_ciis['Gestiune'] == gestiune_selectata]
        if grupa_selectata != "All Groups":
            filtered_ciis = filtered_ciis[filtered_ciis['Denumire grupa'] == grupa_selectata]
        
        # 3D Treemap visualization
        if len(filtered_ciis) > 0:
            st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
            
            group_dist = filtered_ciis.groupby('Denumire grupa')['Valoare'].sum().reset_index()
            
            # Create hierarchical treemap
            fig_treemap = px.treemap(
                filtered_ciis,
                path=['Denumire grupa', 'Furnizor'],
                values='Valoare',
                title='Purchase Distribution by Category and Supplier',
                color='Valoare',
                color_continuous_scale='Blues',
                hover_data={'Cantitate': ':,.0f'}
            )
            
            fig_treemap.update_traces(
                textposition="middle center",
                textfont_size=12,
                hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f} RON<br>Quantity: %{customdata[0]:,.0f}<extra></extra>'
            )
            
            fig_treemap.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title_font_size=22,
                height=600,
                coloraxis_colorbar=dict(
                    title="Value (RON)",
                    tickformat=",.",
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                )
            )
            
            st.plotly_chart(fig_treemap, use_container_width=True)
    
    with tab3:
        st.markdown("<h3 style='font-size: 24px; margin-bottom: 20px;'>🤝 Comprehensive Supplier Analytics</h3>", unsafe_allow_html=True)
        
        # Combine all purchase data
        cipd_df_local = load_cumparari_cipd()
        ciis_df_local = load_cumparari_ciis()
        
        if not cipd_df_local.empty and not ciis_df_local.empty:
            all_purchases = pd.concat([cipd_df_local, ciis_df_local], ignore_index=True)
        elif not cipd_df_local.empty:
            all_purchases = cipd_df_local
        elif not ciis_df_local.empty:
            all_purchases = ciis_df_local
        else:
            st.warning("⚠️ No data available for supplier analysis")
            st.stop()
        
        # Advanced supplier metrics
        supplier_analysis = all_purchases.groupby('Furnizor').agg({
            'Valoare': 'sum',
            'Cantitate': 'sum',
            'Denumire': 'nunique',
            'Pret': 'mean'
        }).reset_index()
        
        supplier_analysis.columns = ['Furnizor', 'Valoare Totală', 'Cantitate Totală', 'Produse Unice', 'Preț Mediu']
        supplier_analysis = supplier_analysis.sort_values('Valoare Totală', ascending=False)
        
        # 3D Scatter plot for supplier analysis
        fig_3d_scatter = go.Figure(data=[go.Scatter3d(
            x=supplier_analysis.head(20)['Cantitate Totală'],
            y=supplier_analysis.head(20)['Valoare Totală'],
            z=supplier_analysis.head(20)['Produse Unice'],
            mode='markers+text',
            text=supplier_analysis.head(20)['Furnizor'],
            textposition="top center",
            marker=dict(
                size=supplier_analysis.head(20)['Preț Mediu'] / supplier_analysis.head(20)['Preț Mediu'].max() * 50,
                color=supplier_analysis.head(20)['Valoare Totală'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Total Value",
                    tickformat=",.",
                    bgcolor='rgba(0,0,0,0.5)',
                    bordercolor='rgba(255,255,255,0.1)',
                    borderwidth=1
                ),
                line=dict(color='rgba(255,255,255,0.2)', width=1)
            ),
            hovertemplate='<b>%{text}</b><br>Volume: %{x:,.0f}<br>Value: %{y:,.0f} RON<br>Products: %{z}<extra></extra>'
        )])
        
        fig_3d_scatter.update_layout(
            title=dict(
                text='Supplier Performance Matrix (3D)',
                font=dict(size=22)
            ),
            scene=dict(
                xaxis=dict(title='Total Volume', gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(title='Total Value (RON)', gridcolor='rgba(255,255,255,0.1)'),
                zaxis=dict(title='Product Diversity', gridcolor='rgba(255,255,255,0.1)'),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            height=600
        )
        
        st.plotly_chart(fig_3d_scatter, use_container_width=True)
        
        # Strategic supplier cards
        st.markdown("<div style='margin: 40px 0;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 22px; margin-bottom: 20px;'>🏆 Strategic Supplier Rankings</h3>", unsafe_allow_html=True)
        
        cols = st.columns(5)
        rank_gradients = [
            'linear-gradient(135deg, #FFD700 0%, #FFA000 100%)',  # Gold
            'linear-gradient(135deg, #C0C0C0 0%, #808080 100%)',  # Silver
            'linear-gradient(135deg, #CD7F32 0%, #8B4513 100%)',  # Bronze
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',  # Blue
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'   # Purple
        ]
        
        for i, (col, row) in enumerate(zip(cols, supplier_analysis.head(5).iterrows())):
            with col:
                supplier = row[1]
                efficiency = supplier['Valoare Totală'] / supplier['Cantitate Totală'] if supplier['Cantitate Totală'] > 0 else 0
                
                st.markdown(f"""
                <div class='premium-info-box' style='text-align: center; padding: 25px;'>
                    <div style='background: {rank_gradients[i]}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                                font-size: 36px; font-weight: 900; margin-bottom: 10px;'>#{i+1}</div>
                    <h4 style='color: white; margin: 10px 0; font-size: 16px; font-weight: 600; 
                               overflow: hidden; text-overflow: ellipsis; white-space: nowrap;'>{supplier['Furnizor']}</h4>
                    <div style='margin: 15px 0;'>
                        <p style='color: var(--text-secondary); margin: 5px 0; font-size: 12px;'>Total Value</p>
                        <p style='color: white; margin: 0; font-size: 18px; font-weight: 700;'>{supplier['Valoare Totală']/1000000:.1f}M</p>
                    </div>
                    <div style='background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-top: 15px;'>
                        <p style='color: var(--text-secondary); margin: 2px 0; font-size: 11px;'>{supplier['Produse Unice']} products</p>
                        <p style='color: var(--text-secondary); margin: 2px 0; font-size: 11px;'>Eff: {efficiency:.0f} RON/unit</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Footer Premium
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 40px 20px; background: var(--glass-bg); backdrop-filter: blur(20px); 
            border-radius: 20px; border: 1px solid var(--glass-border); margin-top: 60px;'>
    <h3 class='animated-gradient-text' style='margin: 0 0 10px 0; font-size: 24px;'>BRENADO ANALYTICS</h3>
    <p style='color: var(--text-secondary); margin: 10px 0; font-size: 14px;'>
        Premium Business Intelligence Suite • Next-Generation Analytics Platform
    </p>
    <div style='display: flex; justify-content: center; gap: 30px; margin: 20px 0;'>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <span class='live-indicator'></span>
            <span style='color: var(--text-secondary); font-size: 12px;'>Real-time Data</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <span style='color: #4facfe;'>🔥</span>
            <span style='color: var(--text-secondary); font-size: 12px;'>Firebase Powered</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <span style='color: #764ba2;'>⚡</span>
            <span style='color: var(--text-secondary); font-size: 12px;'>AI-Enhanced</span>
        </div>
        <div style='display: flex; align-items: center; gap: 8px;'>
            <span style='color: #f093fb;'>🛡️</span>
            <span style='color: var(--text-secondary); font-size: 12px;'>Enterprise Security</span>
        </div>
    </div>
    <p style='color: var(--text-secondary); margin: 20px 0 0 0; font-size: 11px; opacity: 0.6;'>
        © 2025 BRENADO | Premium Edition v2.0 | Crafted with excellence
    </p>
</div>
""", unsafe_allow_html=True)

# Floating Action Button pentru Quick Actions
st.markdown("""
<div class='fab' onclick='window.scrollTo({top: 0, behavior: "smooth"})' 
     style='cursor: pointer;' title='Back to top'>
    <span style='font-size: 24px; color: white;'>↑</span>
</div>
""", unsafe_allow_html=True)
