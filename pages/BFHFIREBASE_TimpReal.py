"""
Brenado For House - Dashboard Firebase în Timp Real
Autor: Castemill SRL
Data: Iulie 2025
"""

import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# ===== CONFIGURARE PAGINĂ =====
st.set_page_config(
    page_title="Brenado For House ",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== FUNCȚII FIREBASE =====

@st.cache_resource
def init_firebase():
    """Inițializează Firebase pentru Streamlit Cloud"""
    try:
        # Verifică dacă Firebase e deja inițializat
        if firebase_admin._apps:
            return firestore.client()
        
        # Pentru LOCAL (development) - folosește fișierul JSON
        # Decomentează dacă rulezi local:
        # cred = credentials.Certificate("path/to/firebase_key.json")
        # firebase_admin.initialize_app(cred)
        
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

@st.cache_data(ttl=3600)  # Cache 1h
def load_vanzari_from_firebase():
    """Încarcă datele de vânzări din Firebase"""
    try:
        db = init_firebase()
        if not db:
            return pd.DataFrame()
        
        # Citește din colecția vanzari_current_month
        docs = db.collection('vanzari_current_month').stream()
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            data.append(doc_data)
        
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        
        # Convertește Data la datetime
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'])
        
        return df
        
    except Exception as e:
        st.error(f"❌ Eroare încărcare date: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_summary_from_firebase():
    """Încarcă sumarizarea din Firebase"""
    try:
        db = init_firebase()
        if not db:
            return {}
        
        # Citește sumarizarea pentru luna curentă
        month_doc = datetime.now().strftime('%Y-%m')
        doc = db.collection('monthly_summaries').document(month_doc).get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return {}
            
    except Exception as e:
        st.error(f"❌ Eroare încărcare sumarizare: {e}")
        return {}

@st.cache_data(ttl=300)
def get_last_sync_info():
    """Returnează informații despre ultimul upload"""
    try:
        db = init_firebase()
        if db is None:
            return None
            
        doc = db.collection('sync_info').document('last_upload').get()
        if doc.exists:
            data = doc.to_dict()
            if 'upload_date' in data and data['upload_date']:
                if hasattr(data['upload_date'], 'strftime'):
                    data['upload_date'] = data['upload_date'].strftime('%d/%m/%Y %H:%M')
                else:
                    data['upload_date'] = str(data['upload_date'])[:16]
            return data
        return None
    except Exception as e:
        st.error(f"Eroare citire sync info: {e}")
        return None

# ===== FUNCȚII DASHBOARD =====

def render_header():
    """Randare header-ul aplicației"""
    st.title("Brenado For House ")
    st.markdown("*Conectat Firebase - date live din ERP B-org*")
    st.markdown("---")

def render_connection_status():
    """Afișează statusul conexiunii"""
    last_sync = get_last_sync_info()
    
    if last_sync:
        upload_date = last_sync.get('upload_date', 'N/A')
        records_count = last_sync.get('records_count', 0)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"🟢 Conectat la Firebase")
        with col2:
            st.info(f"📊 Ultima actualizare: {upload_date}")
        with col3:
            st.info(f"📈 {records_count} înregistrări")
    else:
        st.warning("🟡 Nu s-au găsit informații de sincronizare")

def render_main_metrics(df, summary=None):
    """metricile principale"""
    if df.empty:
        st.warning("⚠️ Nu sunt date disponibile în Firebase")
        return
    
    st.subheader("📊 Metrici Principale")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vanzari = df['Valoare'].sum() if 'Valoare' in df.columns else 0
        st.metric("💰 Vânzări Totale", f"{total_vanzari:,.0f} RON")
    
    with col2:
        clienti_unici = df['Client'].nunique() if 'Client' in df.columns else 0
        st.metric("👥 Clienți Unici", f"{clienti_unici}")
    
    with col3:
        total_records = len(df)
        st.metric("📋 Tranzacții", f"{total_records:,}")
    
    with col4:
        gestiuni = df['DenumireGestiune'].nunique() if 'DenumireGestiune' in df.columns else 0
        st.metric("🏢 Gestiuni", f"{gestiuni}")



def render_charts(df):
    """graficele"""
    if df.empty:
        return
    
    st.subheader("📈 Analize Vizuale")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vânzări pe Zi**")
        if 'Data' in df.columns and 'Valoare' in df.columns:
            daily_sales = df.groupby(df['Data'].dt.date)['Valoare'].sum().reset_index()
            daily_sales.columns = ['Data', 'Valoare']
            
            fig = px.line(
                daily_sales, 
                x='Data', 
                y='Valoare',
                title="Evoluția Vânzărilor",
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date insuficiente pentru grafic")
    
    with col2:
        st.markdown("**Top 10 Clienți**")
        if 'Client' in df.columns and 'Valoare' in df.columns:
            top_clienti = df.groupby('Client')['Valoare'].sum().nlargest(10).reset_index()
            
            fig = px.bar(
                top_clienti, 
                x='Valoare', 
                y='Client',
                orientation='h',
                title="Clienți după Valoare",
                color='Valoare',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Date insuficiente pentru grafic")





def render_data_tables(df):
    """Randează tabelele cu date"""
    if df.empty:
        return
    
    st.subheader("📋 Date Detaliate")
    
    # Filtre - 4 coloane
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'DenumireGestiune' in df.columns:
            gestiuni = ['Toate'] + list(df['DenumireGestiune'].unique())
            selected_gestiune = st.selectbox("Gestiune:", gestiuni)
    
    with col2:
        if 'Agent' in df.columns:
            agenti = ['Toți'] + list(df['Agent'].unique())
            selected_agent = st.selectbox("Agent:", agenti)
    
    with col3:
        if 'Data' in df.columns:
            # Convertește la datetime dacă nu e deja
            df['Data'] = pd.to_datetime(df['Data'])
            # Obține datele unice și sortează
            date_list = sorted(df['Data'].dt.date.unique())
            date_options = ['Toate zilele'] + [str(date) for date in date_list]
            selected_date = st.selectbox("Data:", date_options)
    
    with col4:
        if 'Denumire' in df.columns:
            # Limitează la primele 50 de produse pentru performanță
            denumiri = ['Toate produsele'] + list(df['Denumire'].unique())[:50]
            selected_denumire = st.selectbox("Produs:", denumiri)
    
    # Aplicare filtre
    filtered_df = df.copy()
    
    # Filtru gestiune
    if 'DenumireGestiune' in df.columns and selected_gestiune != 'Toate':
        filtered_df = filtered_df[filtered_df['DenumireGestiune'] == selected_gestiune]
    
    # Filtru agent
    if 'Agent' in df.columns and selected_agent != 'Toți':
        filtered_df = filtered_df[filtered_df['Agent'] == selected_agent]
    
    # Filtru dată
    if 'Data' in df.columns and selected_date != 'Toate zilele':
        selected_date_obj = pd.to_datetime(selected_date).date()
        filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date_obj]
    
    # Filtru denumire produs
    if 'Denumire' in df.columns and selected_denumire != 'Toate produsele':
        filtered_df = filtered_df[filtered_df['Denumire'] == selected_denumire]
    
    # Selectare coloane importante pentru afișare
    display_columns = [
        'Data', 'Client', 'Denumire', 'Cantitate', 'Valoare', 
        'Adaos', 'Agent', 'DenumireGestiune', 'Cod', 'UM'
    ]
    
    # Afișează doar coloanele disponibile
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    if available_columns:
        # Sortare după dată (cele mai recente primul)
        if 'Data' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('Data', ascending=False)
        
        st.dataframe(
            filtered_df[available_columns], 
            use_container_width=True,
            height=400
        )
        
        # Statistici pentru datele filtrate
        if not filtered_df.empty:
            st.markdown("#### 📊 Statistici Date Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_valoare = filtered_df['Valoare'].sum() if 'Valoare' in filtered_df.columns else 0
                st.metric("Total Valoare", f"{total_valoare:,.0f} RON")
            
            with col2:
                total_adaos = filtered_df['Adaos'].sum() if 'Adaos' in filtered_df.columns else 0
                st.metric("Total Adaos", f"{total_adaos:,.0f} RON")
            
            with col3:
                total_cantitate = filtered_df['Cantitate'].sum() if 'Cantitate' in filtered_df.columns else 0
                st.metric("Total Cantitate", f"{total_cantitate:,.0f}")
            
            with col4:
                nr_inregistrari = len(filtered_df)
                st.metric("Înregistrări", f"{nr_inregistrari:,}")
    else:
        st.warning("Nu există coloane disponibile pentru afișare")

def render_sidebar():
    """sidebar-ul cu controale"""
    with st.sidebar:

        # Informații sistem
        st.subheader("ℹ️ Informații Sistem")
        st.info(f"🕒 Ultimul refresh: {datetime.now().strftime('%H:%M:%S')}")
        
  
        
        # Status Firebase
        st.subheader("🔥 Status Firebase")
        try:
            db = init_firebase()
            if db:
                st.success("✅ Conectat")
            else:
                st.error("❌ Deconectat")
        except:
            st.error("❌ Eroare conexiune")

# ===== FUNCȚIA PRINCIPALĂ =====

def main():
    """Funcția principală a aplicației"""
    
    # Header
    render_header()
    
    # Sidebar
    render_sidebar()
    
    # Status conexiune
    render_connection_status()
    
    st.markdown("---")
    
    # Încărcare date
    with st.spinner("📡 Se încarcă datele din Firebase..."):
        df = load_vanzari_from_firebase()
        summary = load_summary_from_firebase()
    
    # Metrici principale
    render_main_metrics(df, summary)
    
    st.markdown("---")
    
    # Grafice
    render_charts(df)
    
    st.markdown("---")
    
    # Tabele detaliate
    render_data_tables(df)
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard generat automat din datele Firebase • Brenado For House ERP*")

# ===== RULARE APLICAȚIE =====

if __name__ == "__main__":
    main()
