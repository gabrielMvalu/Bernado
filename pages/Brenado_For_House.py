import streamlit as st
import pandas as pd

# Configurare pagină
st.set_page_config(
    page_title="Brenado For House",
    layout="wide"
)

# Funcții pentru încărcarea datelor - ORIGINALE
@st.cache_data
def load_vanzari_zi_clienti():
    """Încarcă datele din Excel - Situația zi și clienți"""
    try:
        df = pd.read_excel("data/svzc.xlsx")
        return df
    except:
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
        return pd.DataFrame({
            'Denumire gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ZileVechime': [10]
        })

@st.cache_data
def load_cumparari_cipd():
    """Încarcă datele din Excel - Cumparari CIPD"""
    try:
        df = pd.read_excel("data/CIPD.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Cantitate': [100],
            'Valoare': [5000],
            'Furnizor': ['Demo Furnizor']
        })

@st.cache_data
def load_cumparari_ciis():
    """Încarcă datele din Excel - Cumparari CIIS"""
    try:
        df = pd.read_excel("data/CIIS.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Cantitate': [100],
            'Valoare': [5000],
            'Furnizor': ['Demo Furnizor']
        })

# NOUĂ - Funcții pentru încărcarea datelor de facturi
@st.cache_data
def load_neachitate():
    """Încarcă datele din Excel - Facturi Neachitate"""
    try:
        # Încerc mai multe căi posibile pentru fișier
        possible_paths = ["Neachitate.xlsx", "data/Neachitate.xlsx", "./Neachitate.xlsx"]
        df = None
        
        for path in possible_paths:
            try:
                df = pd.read_excel(path)
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            raise FileNotFoundError("Nu s-a găsit fișierul")
        
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Furnizor'].notna() & ~df['Furnizor'].str.contains('Total  ', na=False) & df['Numar'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        return df
    except:
        return pd.DataFrame({
            'Furnizor': ['Furnizor Demo 1', 'Furnizor Demo 2'],
            'Numar': ['F001', 'F002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [5000, 3000],
            'Sold': [5000, 1500],
            'Zile Intarziere': [5, 0],
            'Valuta': ['EUR', 'EUR'],
            'Serie': ['Demo1', 'Demo2'],
            'PL': ['PL 01', 'PL 02']
        })

@st.cache_data
def load_neincasate():
    """Încarcă datele din Excel - Facturi Neincasate"""
    try:
        # Încerc mai multe căi posibile pentru fișier
        possible_paths = ["Neincasate.xlsx", "data/Neincasate.xlsx", "./Neincasate.xlsx"]
        df = None
        
        for path in possible_paths:
            try:
                df = pd.read_excel(path)
                break
            except FileNotFoundError:
                continue
        
        if df is None:
            raise FileNotFoundError("Nu s-a găsit fișierul")
        
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Client'].notna() & ~df['Client'].str.contains('Total  ', na=False) & df['NumarDoc'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        return df
    except:
        return pd.DataFrame({
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'NumarDoc': ['V001', 'V002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [8000, 6000],
            'Sold': [8000, 3000],
            'Zile Intarziere': [10, 0],
            'Valuta': ['LEI', 'LEI'],
            'Serie': ['Demo1', 'Demo2'],
            'Agent': ['Agent Demo', 'Agent Demo']
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
    ["Situație Intrări Ieșiri", "Balanță Stocuri", "Cumparari Intrari", "Plăți Facturi"]
)

st.markdown("---")

# ===== SITUAȚIE INTRĂRI IEȘIRI ===== [ORIGINAL - NESCHIMBAT]
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

# ===== BALANȚĂ STOCURI ===== [ORIGINAL - NESCHIMBAT]
elif category == "Balanță Stocuri":
    st.markdown("### 📦 Balanță Stocuri")
    
    # Tabs pentru subcategoriile Balanță Stocuri
    tab1, tab2 = st.tabs(["📅 În Dată", "📊 Perioadă"])
    
    with tab1:
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
            st.metric("Stoc Total", f"{total_stoc:,.0f} buc")
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
        
        # Aplicare filtre
        filtered_balanta = balanta_df.copy()
        if 'DenumireGest' in balanta_df.columns and gestiune_filter:
            filtered_balanta = filtered_balanta[filtered_balanta['DenumireGest'].isin(gestiune_filter)]
        
        # Tabel cu date
        st.dataframe(filtered_balanta, use_container_width=True)
    
    with tab2:
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
        st.dataframe(perioada_df, use_container_width=True)

# ===== CUMPARARI INTRARI ===== [ORIGINAL - NESCHIMBAT]
elif category == "Cumparari Intrari":
    st.markdown("### 🛒 Cumparari Intrari")
    
    # Tabs pentru subcategoriile Cumparari Intrari
    tab1, tab2 = st.tabs(["📋 Cumpărări Intrări Grupări pe Data", "📊 Cumpărări Intrări în Stoc"])
    
    with tab1:
        st.markdown("#### 📋 Cumpărări Intrări Grupări pe Data")
        
        # Încărcare date
        cipd_df = load_cumparari_cipd()
        
        # Calculare metrici
        total_cantitate = cipd_df['Cantitate'].sum() if 'Cantitate' in cipd_df.columns else 0
        total_valoare = cipd_df['Valoare'].sum() if 'Valoare' in cipd_df.columns else 0
        numar_produse = len(cipd_df)
        furnizori_unici = cipd_df['Furnizor'].nunique() if 'Furnizor' in cipd_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Cantitate Totală", f"{total_cantitate:,.0f} buc")
        with col2:
            st.metric("Valoare Totală", f"{total_valoare:,.0f} RON")
        with col3:
            st.metric("Produse", f"{numar_produse:,}")
        with col4:
            st.metric("Furnizori", f"{furnizori_unici}")
        
        st.markdown("---")
        st.dataframe(cipd_df, use_container_width=True)
    
    with tab2:
        st.markdown("#### 📊 Cumpărări Intrări în Stoc")
        
        # Încărcare date
        ciis_df = load_cumparari_ciis()
        
        # Calculare metrici generale
        total_cantitate = ciis_df['Cantitate'].sum() if 'Cantitate' in ciis_df.columns else 0
        total_valoare = ciis_df['Valoare'].sum() if 'Valoare' in ciis_df.columns else 0
        numar_produse = len(ciis_df)
        furnizori_unici = ciis_df['Furnizor'].nunique() if 'Furnizor' in ciis_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Cantitate Totală", f"{total_cantitate:,.0f} buc")
        with col2:
            st.metric("Valoare Totală", f"{total_valoare:,.0f} RON")
        with col3:
            st.metric("Produse", f"{numar_produse:,}")
        with col4:
            st.metric("Furnizori", f"{furnizori_unici}")
        
        st.markdown("---")
        
        # Selecții pentru filtrare cu afișare valori
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Selectare Gestiune")
            if 'Gestiune' in ciis_df.columns:
                gestiune_selectata = st.selectbox(
                    "Alege gestiunea:",
                    options=["Toate"] + list(ciis_df['Gestiune'].unique()),
                    key="gestiune_select"
                )
                
                # Calculare și afișare valoare pentru gestiunea selectată
                if gestiune_selectata != "Toate":
                    valoare_gestiune = ciis_df[ciis_df['Gestiune'] == gestiune_selectata]['Valoare'].sum()
                    st.success(f"💰 Valoare gestiune **{gestiune_selectata}**: **{valoare_gestiune:,.0f} RON**")
        
        with col2:
            st.subheader("📂 Selectare Grupă")
            if 'Denumire grupa' in ciis_df.columns:
                grupa_selectata = st.selectbox(
                    "Alege grupa:",
                    options=["Toate"] + list(ciis_df['Denumire grupa'].unique()),
                    key="grupa_select"
                )
                
                # Calculare și afișare valoare pentru grupa selectată
                if grupa_selectata != "Toate":
                    valoare_grupa = ciis_df[ciis_df['Denumire grupa'] == grupa_selectata]['Valoare'].sum()
                    st.success(f"💰 Valoare grupă **{grupa_selectata}**: **{valoare_grupa:,.0f} RON**")
        
        st.markdown("---")
        
        # Aplicare filtre pe tabel
        filtered_ciis = ciis_df.copy()
        
        # Filtrare după gestiune
        if 'Gestiune' in ciis_df.columns and gestiune_selectata != "Toate":
            filtered_ciis = filtered_ciis[filtered_ciis['Gestiune'] == gestiune_selectata]
        
        # Filtrare după grupă
        if 'Denumire grupa' in ciis_df.columns and grupa_selectata != "Toate":
            filtered_ciis = filtered_ciis[filtered_ciis['Denumire grupa'] == grupa_selectata]
        
        # Afișare tabel filtrat
        st.subheader(f"📋 Date Filtrate ({len(filtered_ciis)} înregistrări)")
        st.dataframe(filtered_ciis, use_container_width=True)
        
        # Statistici pentru datele filtrate
        if not filtered_ciis.empty:
            st.markdown("#### 📊 Statistici Date Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                cant_filtrata = filtered_ciis['Cantitate'].sum() if 'Cantitate' in filtered_ciis.columns else 0
                st.metric("Cantitate Filtrată", f"{cant_filtrata:,.0f} buc")
            with col2:
                val_filtrata = filtered_ciis['Valoare'].sum() if 'Valoare' in filtered_ciis.columns else 0
                st.metric("Valoare Filtrată", f"{val_filtrata:,.0f} RON")
            with col3:
                furnizori_filtrati = filtered_ciis['Furnizor'].nunique() if 'Furnizor' in filtered_ciis.columns else 0
                st.metric("Furnizori", f"{furnizori_filtrati}")
            with col4:
                pret_mediu = filtered_ciis['Pret'].mean() if 'Pret' in filtered_ciis.columns else 0
                st.metric("Preț Mediu", f"{pret_mediu:,.2f} RON")

# ===== PLĂȚI FACTURI ===== [NOU - ADĂUGAT]
elif category == "Plăți Facturi":
    st.markdown("### 💳 Plăți Facturi")
    
    # Tabs pentru subcategoriile Plăți Facturi
    tab1, tab2 = st.tabs(["❌ Neachitate", "📥 Neincasate"])
    
    with tab1:
        st.markdown("#### ❌ Facturi Neachitate")
        
        # Încărcare date
        neachitate_df = load_neachitate()
        
        # Calculare metrici
        total_neachitat = neachitate_df['Sold'].sum() if 'Sold' in neachitate_df.columns else 0
        numar_facturi = len(neachitate_df)
        furnizori_unici = neachitate_df['Furnizor'].nunique() if 'Furnizor' in neachitate_df.columns else 0
        facturi_restante = len(neachitate_df[neachitate_df['Zile Intarziere'] > 0]) if 'Zile Intarziere' in neachitate_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Neachitat", f"{total_neachitat:,.0f} RON")
        with col2:
            st.metric("Facturi Neachitate", f"{numar_facturi}")
        with col3:
            st.metric("Furnizori", f"{furnizori_unici}")
        with col4:
            st.metric("Facturi Restante", f"{facturi_restante}")
        
        st.markdown("---")
        
        # Selecții pentru filtrare cu afișare valori
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Selectare Furnizor")
            if 'Furnizor' in neachitate_df.columns:
                furnizor_selectat = st.selectbox(
                    "Alege furnizorul:",
                    options=["Toți"] + list(neachitate_df['Furnizor'].unique()),
                    key="furnizor_select"
                )
                
                # Calculare și afișare valoare pentru furnizorul selectat
                if furnizor_selectat != "Toți":
                    valoare_furnizor = neachitate_df[neachitate_df['Furnizor'] == furnizor_selectat]['Sold'].sum()
                    st.success(f"💰 Valoare furnizor **{furnizor_selectat}**: **{valoare_furnizor:,.0f} RON**")
        
        with col2:
            st.subheader("💱 Selectare Valută")
            if 'Valuta' in neachitate_df.columns:
                valuta_selectata = st.selectbox(
                    "Alege valuta:",
                    options=["Toate"] + list(neachitate_df['Valuta'].unique()),
                    key="valuta_select"
                )
                
                # Calculare și afișare valoare pentru valuta selectată
                if valuta_selectata != "Toate":
                    valoare_valuta = neachitate_df[neachitate_df['Valuta'] == valuta_selectata]['Sold'].sum()
                    st.success(f"💰 Total valută **{valuta_selectata}**: **{valoare_valuta:,.0f}**")
        
        # Filtrare pentru sume mari
        col3, col4 = st.columns(2)
        with col3:
            if 'Sold' in neachitate_df.columns:
                suma_minima = st.number_input(
                    "Suma minimă (RON):",
                    min_value=0,
                    value=0,
                    step=1000,
                    key="suma_min_neachitate"
                )
        
        with col4:
            # Filtru pentru facturile restante
            show_restante = st.checkbox("Doar facturile restante", key="restante_neachitate")
        
        st.markdown("---")
        
        # Aplicare filtre pe tabel
        filtered_neachitate = neachitate_df.copy()
        
        # Filtrare după furnizor
        if 'Furnizor' in neachitate_df.columns and furnizor_selectat != "Toți":
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Furnizor'] == furnizor_selectat]
        
        # Filtrare după valută
        if 'Valuta' in neachitate_df.columns and valuta_selectata != "Toate":
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Valuta'] == valuta_selectata]
        
        # Filtrare după sumă minimă
        if 'Sold' in neachitate_df.columns and suma_minima > 0:
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Sold'] >= suma_minima]
        
        # Filtrare după restante
        if show_restante and 'Zile Intarziere' in neachitate_df.columns:
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Zile Intarziere'] > 0]
        
        # Afișare tabel filtrat
        st.subheader(f"📋 Date Filtrate ({len(filtered_neachitate)} înregistrări)")
        st.dataframe(filtered_neachitate, use_container_width=True)
        
        # Statistici pentru datele filtrate
        if not filtered_neachitate.empty:
            st.markdown("#### 📊 Statistici Date Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_filtrat = filtered_neachitate['Sold'].sum() if 'Sold' in filtered_neachitate.columns else 0
                st.metric("Total Filtrat", f"{total_filtrat:,.0f} RON")
            with col2:
                suma_totala = filtered_neachitate['Total'].sum() if 'Total' in filtered_neachitate.columns else 0
                st.metric("Suma Totală", f"{suma_totala:,.0f} RON")
            with col3:
                furnizori_filtrati = filtered_neachitate['Furnizor'].nunique() if 'Furnizor' in filtered_neachitate.columns else 0
                st.metric("Furnizori", f"{furnizori_filtrati}")
            with col4:
                zile_medie = filtered_neachitate['Zile Intarziere'].mean() if 'Zile Intarziere' in filtered_neachitate.columns else 0
                st.metric("Întârziere Medie", f"{zile_medie:.0f} zile")
    
    with tab2:
        st.markdown("#### 📥 Facturi Neincasate")
        
        # Încărcare date
        neincasate_df = load_neincasate()
        
        # Calculare metrici
        total_neincasat = neincasate_df['Sold'].sum() if 'Sold' in neincasate_df.columns else 0
        numar_facturi = len(neincasate_df)
        clienti_unici = neincasate_df['Client'].nunique() if 'Client' in neincasate_df.columns else 0
        facturi_restante = len(neincasate_df[neincasate_df['Zile Intarziere'] > 0]) if 'Zile Intarziere' in neincasate_df.columns else 0
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Neincasat", f"{total_neincasat:,.0f} RON")
        with col2:
            st.metric("Facturi Neincasate", f"{numar_facturi}")
        with col3:
            st.metric("Clienți", f"{clienti_unici}")
        with col4:
            st.metric("Facturi Restante", f"{facturi_restante}")
        
        st.markdown("---")
        
        # Selecții pentru filtrare cu afișare valori
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Selectare Client")
            if 'Client' in neincasate_df.columns:
                client_selectat = st.selectbox(
                    "Alege clientul:",
                    options=["Toți"] + list(neincasate_df['Client'].unique()),
                    key="client_select"
                )
                
                # Calculare și afișare valoare pentru clientul selectat
                if client_selectat != "Toți":
                    valoare_client = neincasate_df[neincasate_df['Client'] == client_selectat]['Sold'].sum()
                    st.success(f"💰 Valoare client **{client_selectat}**: **{valoare_client:,.0f} RON**")
        
        with col2:
            st.subheader("🎯 Selectare Agent")
            if 'Agent' in neincasate_df.columns:
                agent_selectat = st.selectbox(
                    "Alege agentul:",
                    options=["Toți"] + list(neincasate_df['Agent'].unique()),
                    key="agent_select"
                )
                
                # Calculare și afișare valoare pentru agentul selectat
                if agent_selectat != "Toți":
                    valoare_agent = neincasate_df[neincasate_df['Agent'] == agent_selectat]['Sold'].sum()
                    st.success(f"💰 Total agent **{agent_selectat}**: **{valoare_agent:,.0f} RON**")
        
        # Filtrare pentru sume mari
        col3, col4 = st.columns(2)
        with col3:
            if 'Sold' in neincasate_df.columns:
                suma_minima = st.number_input(
                    "Suma minimă (RON):",
                    min_value=0,
                    value=0,
                    step=1000,
                    key="suma_min_neincasate"
                )
        
        with col4:
            # Filtru pentru facturile restante
            show_restante = st.checkbox("Doar facturile restante", key="restante_neincasate")
        
        st.markdown("---")
        
        # Aplicare filtre pe tabel
        filtered_neincasate = neincasate_df.copy()
        
        # Filtrare după client
        if 'Client' in neincasate_df.columns and client_selectat != "Toți":
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Client'] == client_selectat]
        
        # Filtrare după agent
        if 'Agent' in neincasate_df.columns and agent_selectat != "Toți":
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Agent'] == agent_selectat]
        
        # Filtrare după sumă minimă
        if 'Sold' in neincasate_df.columns and suma_minima > 0:
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Sold'] >= suma_minima]
        
        # Filtrare după restante
        if show_restante and 'Zile Intarziere' in neincasate_df.columns:
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Zile Intarziere'] > 0]
        
        # Afișare tabel filtrat
        st.subheader(f"📋 Date Filtrate ({len(filtered_neincasate)} înregistrări)")
        st.dataframe(filtered_neincasate, use_container_width=True)
        
        # Statistici pentru datele filtrate
        if not filtered_neincasate.empty:
            st.markdown("#### 📊 Statistici Date Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_filtrat = filtered_neincasate['Sold'].sum() if 'Sold' in filtered_neincasate.columns else 0
                st.metric("Total Filtrat", f"{total_filtrat:,.0f} RON")
            with col2:
                suma_totala = filtered_neincasate['Total'].sum() if 'Total' in filtered_neincasate.columns else 0
                st.metric("Suma Totală", f"{suma_totala:,.0f} RON")
            with col3:
                clienti_filtrati = filtered_neincasate['Client'].nunique() if 'Client' in filtered_neincasate.columns else 0
                st.metric("Clienți", f"{clienti_filtrati}")
            with col4:
                zile_medie = filtered_neincasate['Zile Intarziere'].mean() if 'Zile Intarziere' in filtered_neincasate.columns else 0
                st.metric("Întârziere Medie", f"{zile_medie:.0f} zile")
