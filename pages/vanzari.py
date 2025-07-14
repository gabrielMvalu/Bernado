"""
Pagina Vânzări pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_loaders import load_vanzari

# Titlu pagină
st.markdown("### 📊 Vânzări")

# Încărcare date
vanzari_df = load_vanzari()

# Calculare metrici principali
total_vanzari = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
clienti_unici = vanzari_df['Client'].nunique() if 'Client' in vanzari_df.columns else 0
total_records = len(vanzari_df)
gestiuni = vanzari_df['DenumireGestiune'].nunique() if 'DenumireGestiune' in vanzari_df.columns else 0

# Metrici principale
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Vânzări Totale", f"{total_vanzari:,.0f} RON")
with col2:
    st.metric("👥 Clienți Unici", f"{clienti_unici}")
with col3:
    st.metric("📋 Tranzacții", f"{total_records:,}")
with col4:
    st.metric("🏢 Gestiuni", f"{gestiuni}")

st.markdown("---")

# Grafice
st.subheader("📈 Analize Vizuale")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Vânzări pe Zi**")
    if 'Data' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
        daily_sales = vanzari_df.groupby(vanzari_df['Data'].dt.date)['Valoare'].sum().reset_index()
        daily_sales.columns = ['Data', 'Valoare']
        
        if not daily_sales.empty:
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
            st.info("Nu există date pentru perioada selectată")
    else:
        st.info("Date insuficiente pentru grafic")

with col2:
    st.markdown("**Top 10 Clienți**")
    if 'Client' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
        top_clienti = vanzari_df.groupby('Client')['Valoare'].sum().nlargest(10).reset_index()
        
        if not top_clienti.empty:
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
            st.info("Nu există date pentru grafic")
    else:
        st.info("Date insuficiente pentru grafic")

st.markdown("---")

# Date detaliate cu filtre
st.subheader("📋 Date Detaliate")

# Filtre
col1, col2, col3, col4 = st.columns(4)

with col1:
    if 'DenumireGestiune' in vanzari_df.columns:
        gestiuni_list = ['Toate'] + list(vanzari_df['DenumireGestiune'].unique())
        selected_gestiune = st.selectbox("Gestiune:", gestiuni_list)

with col2:
    if 'Agent' in vanzari_df.columns:
        agenti_list = ['Toți'] + list(vanzari_df['Agent'].unique())
        selected_agent = st.selectbox("Agent:", agenti_list)

with col3:
    if 'Data' in vanzari_df.columns:
        vanzari_df['Data'] = pd.to_datetime(vanzari_df['Data'])
        min_date = vanzari_df['Data'].min().date()
        max_date = vanzari_df['Data'].max().date()
        today = datetime.now().date()
        
        if today > max_date:
            default_date = max_date
        elif today < min_date:
            default_date = min_date
        else:
            default_date = today
        
        date_range = st.date_input(
            "📅 Interval date:",
            value=(default_date, default_date),
            min_value=min_date,
            max_value=max_date,
            format="DD/MM/YYYY"
        )

with col4:
    # Filtru produs
    if 'Denumire' in vanzari_df.columns:
        produs_filter = st.multiselect(
            "Filtrează după produs:",
            options=vanzari_df['Denumire'].unique(),
            default=[],
            key="produs_filter"
        )

# Aplicare filtre
filtered_df = vanzari_df.copy()

# Filtru gestiune
if 'DenumireGestiune' in vanzari_df.columns and selected_gestiune != 'Toate':
    filtered_df = filtered_df[filtered_df['DenumireGestiune'] == selected_gestiune]

# Filtru agent
if 'Agent' in vanzari_df.columns and selected_agent != 'Toți':
    filtered_df = filtered_df[filtered_df['Agent'] == selected_agent]

# Filtru dată
if 'Data' in vanzari_df.columns and date_range:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Data'].dt.date >= start_date) & 
            (filtered_df['Data'].dt.date <= end_date)
        ]
    else:
        selected_date_obj = date_range
        filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date_obj]

# Filtru produs
if 'Denumire' in vanzari_df.columns and produs_filter:
    filtered_df = filtered_df[filtered_df['Denumire'].isin(produs_filter)]

# Afișare rezultate
if not filtered_df.empty:
    # Sortare după dată
    if 'Data' in filtered_df.columns:
        filtered_df = filtered_df.sort_values('Data', ascending=False)
    
    # Afișare DataFrame complet
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Afișez întotdeauna statisticile când sunt aplicate filtre
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
        st.metric("Înregistrări", f"{len(filtered_df):,}")

else:
    st.warning("Nu s-au găsit înregistrări cu filtrele selectate")
