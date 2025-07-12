import streamlit as st

# Configurare pagină
st.set_page_config(
    page_title="Brenado For House",
    layout="wide"
)

# Definirea paginilor cu noua structură st.navigation
pages = {
    "Brenado For House": [
        st.Page("pages/vanzari.py", title="📊 Vânzări"),
        st.Page("pages/balanta_stocuri.py", title="📦 Balanță Stocuri"),
        st.Page("pages/cumparari_intrari.py", title="🛒 Cumpărări Intrări"),
        st.Page("pages/facturi_neincasate.py", title="📥 Facturi Neincasate"),
        st.Page("pages/facturi_neachitate.py", title="❌ Facturi Neachitate"),
        st.Page("pages/scadente_plati.py", title="⏰ Scadențe Plăți Cu Efecte"),
    ],
    "Vanzari Timp Real": [
        st.Page("pages/BFHFIREBASE_TimpReal.py", title="Vanzari - Timp Real")
    ]
}

# Crearea și rularea navigației
pg = st.navigation(pages)
pg.run()
