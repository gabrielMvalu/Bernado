"""
Pagina Facturi Neîncasate pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.data_loaders import load_neincasate

# Titlu pagină
st.markdown("### 📥 Facturi Neîncasate")

# Încărcare date
neincasate_df = load_neincasate()

# Calculare metrici globali
total_sold = neincasate_df['Sold'].sum() if 'Sold' in neincasate_df.columns else 0

# Calculare Scadenta Azi
scadenta_azi = 0
if 'DataScadenta' in neincasate_df.columns:
    # Convertire DataScadenta la datetime și filtrare pentru ziua curentă
    neincasate_df['DataScadenta'] = pd.to_datetime(neincasate_df['DataScadenta'])
    data_curenta = datetime.now().date()
    
    # Filtrare facturi scadente azi
    facturi_azi = neincasate_df[neincasate_df['DataScadenta'].dt.date == data_curenta]
    scadenta_azi = facturi_azi['Sold'].sum() if not facturi_azi.empty and 'Sold' in facturi_azi.columns else 0

# Metrici principale (globali)
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sold", f"{total_sold:,.0f} RON")
with col2:
    st.metric("Scadenta Azi", f"{scadenta_azi:,.0f} RON")

st.markdown("---")

# Filtre
col1, col2 = st.columns(2)

with col1:
    # Filtru client
    if 'Client' in neincasate_df.columns:
        client_filter = st.multiselect(
            "Filtrează după client:",
            options=neincasate_df['Client'].unique(),
            default=[],
            key="client_filter"
        )

with col2:
    # Filtru scadențe depășite
    scadenta_filter = st.selectbox(
        "Filtrează facturi cu scadența depășită:",
        options=["Toate", "Săptămâna Curentă", "Luna Curentă"],
        index=0,
        key="scadenta_filter"
    )

# Aplicare filtre
filtered_df = neincasate_df.copy()

# Filtru client
if 'Client' in neincasate_df.columns and client_filter:
    filtered_df = filtered_df[filtered_df['Client'].isin(client_filter)]

# Filtru scadențe depășite
if 'DataScadenta' in neincasate_df.columns and scadenta_filter != "Toate":
    data_curenta = datetime.now().date()
    
    if scadenta_filter == "Săptămâna Curentă":
        # Începutul săptămânii curente (luni)
        start_week = data_curenta - timedelta(days=data_curenta.weekday())
        filtered_df = filtered_df[
            (filtered_df['DataScadenta'].dt.date < data_curenta) & 
            (filtered_df['DataScadenta'].dt.date >= start_week)
        ]
    
    elif scadenta_filter == "Luna Curentă":
        # Începutul lunii curente
        start_month = data_curenta.replace(day=1)
        filtered_df = filtered_df[
            (filtered_df['DataScadenta'].dt.date < data_curenta) & 
            (filtered_df['DataScadenta'].dt.date >= start_month)
        ]

# Afișare tabel cu datele filtrate
st.dataframe(filtered_df, use_container_width=True)

# Metrici pentru datele filtrate (sub tabel)
if not filtered_df.empty:
    st.markdown("#### 📊 Statistici Date Filtrate")
    total_sold_filtrat = filtered_df['Sold'].sum() if 'Sold' in filtered_df.columns else 0
    st.metric("Total Sold Filtrat", f"{total_sold_filtrat:,.0f} RON")
