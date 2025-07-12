"""
Pagina Facturi Neachitate pentru aplicația Brenado For House
"""

import streamlit as st
from utils.data_loaders import load_neachitate

# Titlu pagină
st.markdown("### ❌ Facturi Neachitate")

# Încărcare date
neachitate_df = load_neachitate()

# Afișare tabel cu datele
st.dataframe(neachitate_df, use_container_width=True)
