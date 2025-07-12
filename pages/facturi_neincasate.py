"""
Pagina Facturi Neîncasate pentru aplicația Brenado For House
"""

import streamlit as st
from utils.data_loaders import load_neincasate

# Titlu pagină
st.markdown("### 📥 Facturi Neîncasate")

# Încărcare date
neincasate_df = load_neincasate()

# Calculare metrici principali
total_general = neincasate_df['Total'].sum() if 'Total' in neincasate_df.columns else 0
total_sold = neincasate_df['Sold'].sum() if 'Sold' in neincasate_df.columns else 0
total_achitat = neincasate_df['Achitat'].sum() if 'Achitat' in neincasate_df.columns else 0

# Metrici principale
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total", f"{total_general:,.0f} RON")
with col2:
    st.metric("Sold", f"{total_sold:,.0f} RON")
with col3:
    st.metric("Achitat", f"{total_achitat:,.0f} RON")

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
    # Filtru agent
    if 'Agent' in neincasate_df.columns:
        agent_filter = st.multiselect(
            "Filtrează după agent:",
            options=neincasate_df['Agent'].unique(),
            default=[],
            key="agent_filter"
        )

# Aplicare filtre
filtered_df = neincasate_df.copy()

# Filtru client
if 'Client' in neincasate_df.columns and client_filter:
    filtered_df = filtered_df[filtered_df['Client'].isin(client_filter)]

# Filtru agent
if 'Agent' in neincasate_df.columns and agent_filter:
    filtered_df = filtered_df[filtered_df['Agent'].isin(agent_filter)]

# Afișare tabel cu datele filtrate
st.dataframe(filtered_df, use_container_width=True)

# Metrici pentru datele filtrate (sub tabel)
if not filtered_df.empty and (client_filter or agent_filter):
    st.markdown("#### 📊 Statistici Date Filtrate")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_filtrat = filtered_df['Total'].sum() if 'Total' in filtered_df.columns else 0
        st.metric("Total Filtrat", f"{total_filtrat:,.0f} RON")
    with col2:
        sold_filtrat = filtered_df['Sold'].sum() if 'Sold' in filtered_df.columns else 0
        st.metric("Sold Filtrat", f"{sold_filtrat:,.0f} RON")
    with col3:
        achitat_filtrat = filtered_df['Achitat'].sum() if 'Achitat' in filtered_df.columns else 0
        st.metric("Achitat Filtrat", f"{achitat_filtrat:,.0f} RON")
