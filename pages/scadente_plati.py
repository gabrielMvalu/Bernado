"""
Pagina Scadențe Plăți Cu Efecte pentru aplicația Brenado For House
"""

import streamlit as st
from utils.data_loaders import load_scadente_plati

# Titlu pagină
st.markdown("### ⏰ Scadențe Plăți Cu Efecte")

# Încărcare date
scadente_df = load_scadente_plati()

# Calculare metrici principali
suma_totala = scadente_df['Suma'].sum() if 'Suma' in scadente_df.columns else 0

# Metrici principali
st.metric("Suma", f"{suma_totala:,.0f} RON")

st.markdown("---")

# Filtre
col1, col2 = st.columns(2)

with col1:
    # Filtru data scadenta
    if 'DataScadenta' in scadente_df.columns:
        data_scadenta_filter = st.multiselect(
            "Filtrează după data scadența:",
            options=scadente_df['DataScadenta'].unique(),
            default=[],
            key="data_scadenta_filter"
        )

with col2:
    # Filtru tert
    if 'Tert' in scadente_df.columns:
        tert_filter = st.multiselect(
            "Filtrează după terț:",
            options=scadente_df['Tert'].unique(),
            default=[],
            key="tert_filter"
        )

# Aplicare filtre
filtered_df = scadente_df.copy()

# Filtru data scadenta
if 'Data Scadenta' in scadente_df.columns and data_scadenta_filter:
    filtered_df = filtered_df[filtered_df['DataScadenta'].isin(data_scadenta_filter)]

# Filtru tert
if 'Tert' in scadente_df.columns and tert_filter:
    filtered_df = filtered_df[filtered_df['Tert'].isin(tert_filter)]

# Afișare tabel cu datele filtrate
st.dataframe(filtered_df, use_container_width=True)

# Metrici pentru datele filtrate (sub tabel)
if not filtered_df.empty and (data_scadenta_filter or tert_filter):
    st.markdown("#### 📊 Statistici Date Filtrate")
    suma_filtrata = filtered_df['Suma'].sum() if 'Suma' in filtered_df.columns else 0
    st.metric("Suma Filtrată", f"{suma_filtrata:,.0f} RON")
