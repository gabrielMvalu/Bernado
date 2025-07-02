import streamlit as st
import pandas as pd

# Configurare pagină
st.set_page_config(
    page_title="BrenadoForHouse",
    page_icon="🏠",
    layout="wide"
)

# Funcție pentru încărcarea datelor
@st.cache_data
def load_vanzari_zi_clienti():
    """Încarcă datele din Excel - Situația zi și clienți"""
    try:
        df = pd.read_excel("data/svzc.xlsx")
        return df
    except:
        # Date demo dacă nu găsește fișierul
        return pd.DataFrame({
            'Data': ['2024-01-01', '2024-01-02'],
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'Pret Contabil': [100, 200],
            'Valoare': [1000, 2000],
            'Adaos': [50, 100],
            'Cost': [950, 1900]
        })

@st.cache_data
def load_top_produse():
    """Încarcă datele din Excel - Top produse"""
    try:
        df = pd.read_excel("data/svtp.xlsx")
        return df
    except:
        # Date demo dacă nu găsește fișierul
        return pd.DataFrame({
            'Denumire': ['Produs Demo 1', 'Produs Demo 2'],
            'Cantitate': [100, 200],
            'Valoare': [5000, 8000],
            'Adaos': [500, 800]
        })

# Sidebar
with st.sidebar:
    st.title("🏠 BrenadoForHouse")
    st.caption("Segmentul rezidențial")

# Header
st.title("🏠 BrenadoForHouse")
st.subheader("Dashboard pentru segmentul rezidențial")

st.markdown("---")

# Selectare locație
st.subheader("📍 Selectează Locația")
location = st.selectbox(
    "Alege depozitul/showroom:",
    ["Showroom Galicea", "Depozit Grele Galicea", "Magazin Galicea"]
)

st.markdown(f"### 📊 Date pentru: **{location}**")

# Încărcare date
vanzari_df = load_vanzari_zi_clienti()
produse_df = load_top_produse()

# Calculare metrici
total_valoare = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
numar_clienti = vanzari_df['Client'].nunique() if 'Client' in vanzari_df.columns else 0
numar_produse = len(produse_df)
valoare_medie = vanzari_df['Valoare'].mean() if 'Valoare' in vanzari_df.columns else 0

# Metrici pentru locația selectată
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Vânzări Totale", f"{total_valoare:,.0f} RON")
with col2:
    st.metric("Clienți Unici", f"{numar_clienti}")
with col3:
    st.metric("Produse Active", f"{numar_produse}")
with col4:
    st.metric("Valoare Medie", f"{valoare_medie:,.0f} RON")

st.markdown("---")

# Tabs pentru diferite secțiuni
tab1, tab2 = st.tabs(["📊 Situația Zi și Clienți", "🏆 Top Produse"])

with tab1:
    st.subheader("📊 Situația Vânzărilor pe Zi și Clienți")
    
    # Filtrare date
    col1, col2 = st.columns(2)
    with col1:
        if 'Client' in vanzari_df.columns:
            client_filter = st.multiselect(
                "Filtrează după client:",
                options=vanzari_df['Client'].unique(),
                default=[]
            )
    
    # Afișare date filtrate
    if 'Client' in vanzari_df.columns and client_filter:
        filtered_df = vanzari_df[vanzari_df['Client'].isin(client_filter)]
    else:
        filtered_df = vanzari_df
    
    # Tabel cu date
    st.dataframe(filtered_df, use_container_width=True)
    
    # Statistici rapide
    if not filtered_df.empty:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            total_pret_contabil = filtered_df['Pret Contabil'].sum() if 'Pret Contabil' in filtered_df.columns else 0
            st.metric("Total Preț Contabil", f"{total_pret_contabil:,.0f} RON")
        with col2:
            total_valoare = filtered_df['Valoare'].sum() if 'Valoare' in filtered_df.columns else 0
            st.metric("Total Valoare", f"{total_valoare:,.0f} RON")
        with col3:
            total_adaos = filtered_df['Adaos'].sum() if 'Adaos' in filtered_df.columns else 0
            st.metric("Total Adaos", f"{total_adaos:,.0f} RON")
        with col4:
            total_cost = filtered_df['Cost'].sum() if 'Cost' in filtered_df.columns else 0
            st.metric("Total Cost", f"{total_cost:,.0f} RON")
        with col5:
            st.metric("Înregistrări", len(filtered_df))

with tab2:
    st.subheader("🏆 Top Produse după Valoare")
    
    # Sortare și afișare top produse
    if 'Valoare' in produse_df.columns:
        top_produse = produse_df.sort_values('Valoare', ascending=False).head(20)
        
        # Tabel top produse
        st.dataframe(top_produse, use_container_width=True)
        
        # Statistici produse
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Top Produs Valoare", f"{produse_df['Valoare'].max():,.0f} RON")
        with col2:
            st.metric("Cantitate Totală", f"{produse_df['Cantitate'].sum():,.0f}")
        with col3:
            st.metric("Valoare Totală", f"{produse_df['Valoare'].sum():,.0f} RON")
        with col4:
            st.metric("Adaos Total", f"{produse_df['Adaos'].sum():,.0f} RON")
    else:
        st.error("Nu s-au putut încărca datele produselor")
