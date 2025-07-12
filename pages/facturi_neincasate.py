"""
Pagina Facturi Neîncasate pentru aplicația Brenado For House
"""

import streamlit as st
from utils.data_loaders import load_neincasate

# Titlu pagină
st.markdown("### 📥 Facturi Neîncasate")

# Încărcare date
neincasate_df = load_neincasate()

# Afișare tabel cu datele
st.dataframe(neincasate_df, use_container_width=True)
