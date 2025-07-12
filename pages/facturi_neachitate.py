"""
Pagina Facturi Neachitate pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_loaders import load_neachitate

# Titlu pagină
st.markdown("### ❌ Facturi Neachitate")

# Încărcare date
neachitate_df = load_neachitate()

# Calculare metrici
total_sold = neachitate_df['Sold'].sum() if 'Sold' in neachitate_df.columns else 0

# Calculare Scadenta Azi
scadenta_azi = 0
if 'DataScadenta' in neachitate_df.columns:
    # Convertire DataScadenta la datetime și filtrare pentru ziua curentă
    neachitate_df['DataScadenta'] = pd.to_datetime(neachitate_df['DataScadenta'])
    data_curenta = datetime.now().date()
    
    # Filtrare facturi scadente azi
    facturi_azi = neachitate_df[neachitate_df['DataScadenta'].dt.date == data_curenta]
    scadenta_azi = facturi_azi['Sold'].sum() if not facturi_azi.empty and 'Sold' in facturi_azi.columns else 0

# Metrici principale
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sold", f"{total_sold:,.0f} RON")
with col2:
    st.metric("Scadenta Azi", f"{scadenta_azi:,.0f} RON")

st.markdown("---")

# Afișare tabel cu datele
st.dataframe(neachitate_df, use_container_width=True)
