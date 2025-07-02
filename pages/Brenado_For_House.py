import streamlit as st
import pandas as pd

# Configurare pagină
st.set_page_config(
    page_title="Brenado For House",
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

@st.cache_data
def load_balanta_la_data():
    """Încarcă datele din Excel - Balanță la dată"""
    try:
        df = pd.read_excel("data/LaData.xlsx")
        return df
    except:
        # Date demo dacă nu găsește fișierul
        return pd.DataFrame({
            'DenumireGest': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ValoareStocFinal': [5000]
        })

@st.cache_data
def load_balanta_perioada():
    """Încarcă datele din Excel - Balanță pe perioadă"""
    try:
        df = pd.read_excel("data/Perioada.xlsx")
        return df
    except:
        # Date demo dacă nu găsește fișierul
        return pd.DataFrame({
            'Denumire gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ZileVechime': [10]
        })

# Sidebar
with st.sidebar:
    st.title("🏠 Brenado For House")
    st.caption("Segmentul rezidențial")

# Header
st.title("Brenado For House")
st.subheader("Dashboard pentru segmentul rezidențial")

st.markdown("---")

# Selectare categorie principală
st.subheader("📂 Selectează Categoria")
category = st.selectbox(
    "Alege tipul de raport:",
    ["Situație Intrări Ieșiri", "Balanță Stocuri"]
)

st.markdown("---")

# ===== SITUAȚIE INTRĂRI IEȘIRI =====
if category == "Situație Intrări Ieșiri":
    st.markdown("### 📊 Situație Intrări Ieșiri")
    
    # Încărcare date
    vanzari_df = load_vanzari_zi_clienti()
    produse_df = load_top_produse()

    # Calculare metrici
    total_valoare = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
    numar_clienti = vanzari_df['Client'].nunique() if 'Client' in vanzari_df.columns else 0
    numar_produse = len(produse_df)
    valoare_medie = vanzari_df['Valoare'].mean() if 'Valoare' in vanzari_df.columns else 0

    # Metrici principale
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
        
        # Opțiuni de filtrare
        col1, col2 = st.columns(2)
        with col1:
            show_option = st.selectbox(
                "Afișează:",
                ["Top 10", "Top 20", "Top 50", "Top 100", "Toate produsele"]
            )
        
        # Sortare și afișare top produse
        if 'Valoare' in produse_df.columns:
            top_produse = produse_df.sort_values('Valoare', ascending=False)
            
            # Aplicare filtrare bazată pe selecție
            if show_option == "Top 10":
                top_produse = top_produse.head(10)
            elif show_option == "Top 20":
                top_produse = top_produse.head(20)
            elif show_option == "Top 50":
                top_produse = top_produse.head(50)
            elif show_option == "Top 100":
                top_produse = top_produse.head(100)
            # Pentru "Toate produsele" nu facem nimic (rămân toate)
            
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

# ===== BALANȚĂ STOCURI =====
elif category == "Balanță Stocuri":
    st.markdown("### 📦 Balanță Stocuri")
    
    # Subcategorie pentru Balanță Stocuri
    subcategory = st.selectbox(
        "Selectează tipul de balanță:",
        ["În Dată", "Perioadă"]
    )
    
    # ===== ÎN DATĂ =====
    if subcategory == "În Dată":
        st.markdown("#### 📅 Balanță Stocuri la Dată")
        
        # Încărcare date
        balanta_df = load_balanta_la_data()
        
        # Calculare metrici
        total_stoc = balanta_df['Stoc final'].sum() if 'Stoc final' in balanta_df.columns else 0
        valoare_stoc = balanta_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in balanta_df.columns else 0
        numar_produse = len(balanta_df)
        gestiuni_unice = balanta_df['DenumireGest'].nunique() if 'DenumireGest' in balanta_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Stoc Total", f"{total_stoc:,.0f} buc/kg")
        with col2:
            st.metric("Valoare Stoc", f"{valoare_stoc:,.0f} RON")
        with col3:
            st.metric("Produse în Stoc", f"{numar_produse:,}")
        with col4:
            st.metric("Gestiuni", f"{gestiuni_unice}")
        
        st.markdown("---")
        
        # Filtrare date
        col1, col2 = st.columns(2)
        with col1:
            if 'DenumireGest' in balanta_df.columns:
                gestiune_filter = st.multiselect(
                    "Filtrează după gestiune:",
                    options=balanta_df['DenumireGest'].unique(),
                    default=[]
                )
        with col2:
            if 'Grupa' in balanta_df.columns:
                grupa_filter = st.multiselect(
                    "Filtrează după grupă:",
                    options=balanta_df['Grupa'].unique(),
                    default=[]
                )
        
        # Aplicare filtre
        filtered_balanta = balanta_df.copy()
        if 'DenumireGest' in balanta_df.columns and gestiune_filter:
            filtered_balanta = filtered_balanta[filtered_balanta['DenumireGest'].isin(gestiune_filter)]
        if 'Grupa' in balanta_df.columns and grupa_filter:
            filtered_balanta = filtered_balanta[filtered_balanta['Grupa'].isin(grupa_filter)]
        
        # Tabel cu date
        st.dataframe(filtered_balanta, use_container_width=True)
        
        # Statistici filtrate
        if not filtered_balanta.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_filtrat = filtered_balanta['Stoc final'].sum() if 'Stoc final' in filtered_balanta.columns else 0
                st.metric("Stoc Filtrat", f"{total_filtrat:,.0f} buc")
            with col2:
                valoare_filtrata = filtered_balanta['ValoareStocFinal'].sum() if 'ValoareStocFinal' in filtered_balanta.columns else 0
                st.metric("Valoare Filtrată", f"{valoare_filtrata:,.0f} RON")
            with col3:
                st.metric("Înregistrări", len(filtered_balanta))
            with col4:
                pret_mediu = filtered_balanta['Pret'].mean() if 'Pret' in filtered_balanta.columns else 0
                st.metric("Preț Mediu", f"{pret_mediu:,.2f} RON")
    
    # ===== PERIOADĂ =====
    elif subcategory == "Perioadă":
        st.markdown("#### 📊 Balanță Stocuri pe Perioadă")
        
        # Încărcare date
        perioada_df = load_balanta_perioada()
        
        # Calculare metrici
        total_stoc = perioada_df['Stoc final'].sum() if 'Stoc final' in perioada_df.columns else 0
        valoare_intrare = perioada_df['Valoare intrare'].sum() if 'Valoare intrare' in perioada_df.columns else 0
        numar_produse = len(perioada_df)
        vechime_medie = perioada_df['ZileVechime'].mean() if 'ZileVechime' in perioada_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Stoc Total", f"{total_stoc:,.0f} buc")
        with col2:
            st.metric("Valoare Intrare", f"{valoare_intrare:,.0f} RON")
        with col3:
            st.metric("Produse", f"{numar_produse:,}")
        with col4:
            st.metric("Vechime Medie", f"{vechime_medie:.0f} zile")
        
        st.markdown("---")
        
        # Tabs pentru analiza pe perioade
        tab1, tab2 = st.tabs(["📋 Lista Stocuri", "⏰ Analiză Vechime"])
        
        with tab1:
            st.subheader("📋 Lista Completă Stocuri")
            
            # Filtrare
            col1, col2 = st.columns(2)
            with col1:
                if 'Denumire gestiune' in perioada_df.columns:
                    gestiune_filter = st.multiselect(
                        "Filtrează după gestiune:",
                        options=perioada_df['Denumire gestiune'].unique(),
                        default=[]
                    )
            
            # Aplicare filtru
            filtered_perioada = perioada_df.copy()
            if 'Denumire gestiune' in perioada_df.columns and gestiune_filter:
                filtered_perioada = filtered_perioada[filtered_perioada['Denumire gestiune'].isin(gestiune_filter)]
            
            # Tabel cu date
            st.dataframe(filtered_perioada, use_container_width=True)
        
        with tab2:
            st.subheader("⏰ Analiză Vechime Stocuri")
            
            # Calculare statistici vechime
            if 'ZileVechime' in perioada_df.columns:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    sub_0 = perioada_df['sub 0 zile'].sum() if 'sub 0 zile' in perioada_df.columns else 0
                    st.metric("Sub 0 zile", f"{sub_0:,.0f} RON")
                with col2:
                    intre_1_7 = perioada_df['intre 1 si 7 zile'].sum() if 'intre 1 si 7 zile' in perioada_df.columns else 0
                    st.metric("1-7 zile", f"{intre_1_7:,.0f} RON")
                with col3:
                    intre_8_14 = perioada_df['intre 8 si 14 zile'].sum() if 'intre 8 si 14 zile' in perioada_df.columns else 0
                    st.metric("8-14 zile", f"{intre_8_14:,.0f} RON")
                with col4:
                    peste_15 = perioada_df['peste 15 zile'].sum() if 'peste 15 zile' in perioada_df.columns else 0
                    st.metric("15+ zile", f"{peste_15:,.0f} RON")
                
                st.markdown("---")
                st.info("📊 Analiza vezi cum se distribuie stocurile pe categorii de vechime")
