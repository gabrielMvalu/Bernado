import streamlit as st
import pandas as pd

# Configurare pagină
st.set_page_config(
    page_title="Brenado For House",
    layout="wide"
)

# Funcții pentru încărcarea datelor
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

@st.cache_data
def load_neachitate():
    """Încarcă datele din Excel - Facturi Neachitate"""
    try:
        df = pd.read_excel("Neachitate.xlsx")
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Furnizor'].notna() & ~df['Furnizor'].str.contains('Total  ', na=False) & df['Numar'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        # Redenumesc coloanele pentru consistență
        df = df.rename(columns={
            'Numar': 'Nr Factura',
            'Data': 'Data Factura',
            'DataScadenta': 'Data Scadenta',
            'Total': 'Suma',
            'Sold': 'Rest de Plata'
        })
        
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea datelor neachitate: {e}")
        return pd.DataFrame({
            'Furnizor': ['Furnizor Demo 1', 'Furnizor Demo 2'],
            'Nr Factura': ['F001', 'F002'],
            'Data Factura': ['2024-01-01', '2024-01-02'],
            'Data Scadenta': ['2024-01-31', '2024-02-01'],
            'Suma': [5000, 3000],
            'Rest de Plata': [5000, 1500],
            'Zile Intarziere': [5, 0]
        })

@st.cache_data
def load_neincasate():
    """Încarcă datele din Excel - Facturi Neincasate"""
    try:
        df = pd.read_excel("Neincasate.xlsx")
        # Filtrez doar facturile reale (nu totalurile)
        df = df[df['Client'].notna() & ~df['Client'].str.contains('Total  ', na=False) & df['NumarDoc'].notna()]
        
        # Calculez zilele de întârziere
        df['Data'] = pd.to_datetime(df['Data'])
        df['DataScadenta'] = pd.to_datetime(df['DataScadenta'])
        today = pd.Timestamp.now()
        df['Zile Intarziere'] = (today - df['DataScadenta']).dt.days
        df['Zile Intarziere'] = df['Zile Intarziere'].apply(lambda x: max(0, x))
        
        # Redenumesc coloanele pentru consistență
        df = df.rename(columns={
            'NumarDoc': 'Nr Factura',
            'Data': 'Data Factura',
            'DataScadenta': 'Data Scadenta',
            'Total': 'Suma',
            'Sold': 'Rest de Incasat'
        })
        
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea datelor neincasate: {e}")
        return pd.DataFrame({
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'Nr Factura': ['V001', 'V002'],
            'Data Factura': ['2024-01-01', '2024-01-02'],
            'Data Scadenta': ['2024-01-31', '2024-02-01'],
            'Suma': [8000, 6000],
            'Rest de Incasat': [8000, 3000],
            'Zile Intarziere': [10, 0]
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

# ===== CUMPARARI INTRARI =====
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

# ===== PLĂȚI FACTURI =====
elif category == "Plăți Facturi":
    st.markdown("### 💳 Plăți Facturi")
    
    # Tabs pentru subcategoriile Plăți Facturi
    tab1, tab2 = st.tabs(["❌ Neachitate", "📥 Neincasate"])
    
    with tab1:
        st.markdown("#### ❌ Facturi Neachitate")
        
        # Încărcare date
        neachitate_df = load_neachitate()
        
        # Calculare metrici
        total_neachitat = neachitate_df['Rest de Plata'].sum() if 'Rest de Plata' in neachitate_df.columns else 0
        numar_facturi = len(neachitate_df)
        furnizori_unici = neachitate_df['Furnizor'].nunique() if 'Furnizor' in neachitate_df.columns else 0
        
        # Calculare facturi restante (cu întârziere)
        facturi_restante = 0
        if 'Zile Intarziere' in neachitate_df.columns:
            facturi_restante = len(neachitate_df[neachitate_df['Zile Intarziere'] > 0])
        
        # Determinare valută principală
        valuta_principala = "EUR"
        if 'Valuta' in neachitate_df.columns and len(neachitate_df) > 0:
            valuta_principala = neachitate_df['Valuta'].iloc[0]
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Neachitat", f"{total_neachitat:,.2f} {valuta_principala}", delta=None, delta_color="inverse")
        with col2:
            st.metric("Facturi Neachitate", f"{numar_facturi:,}")
        with col3:
            st.metric("Furnizori", f"{furnizori_unici}")
        with col4:
            st.metric("Facturi Restante", f"{facturi_restante}", delta=None, delta_color="inverse")
        
        st.markdown("---")
        
        # Filtrare date
        col1, col2 = st.columns(2)
        with col1:
            if 'Furnizor' in neachitate_df.columns:
                furnizor_filter = st.multiselect(
                    "Filtrează după furnizor:",
                    options=sorted(neachitate_df['Furnizor'].unique()),
                    default=[],
                    key="furnizor_neachitate"
                )
        
        with col2:
            # Filtru pentru facturile restante
            show_restante = st.checkbox("Afișează doar facturile restante", key="restante_neachitate")
        
        # Adaug filtrare după valută
        col3, col4 = st.columns(2)
        with col3:
            if 'Valuta' in neachitate_df.columns:
                valute_disponibile = neachitate_df['Valuta'].unique()
                valuta_filter = st.selectbox(
                    "Filtrează după valută:",
                    options=["Toate"] + list(valute_disponibile),
                    key="valuta_neachitate"
                )
        
        with col4:
            # Afișez totaluri pe valute
            if 'Valuta' in neachitate_df.columns and 'Rest de Plata' in neachitate_df.columns:
                st.markdown("**💰 Totaluri pe valute:**")
                for valuta in neachitate_df['Valuta'].unique():
                    total_valuta = neachitate_df[neachitate_df['Valuta'] == valuta]['Rest de Plata'].sum()
                    st.write(f"• {valuta}: {total_valuta:,.2f}")
        
        # Aplicare filtre
        filtered_neachitate = neachitate_df.copy()
        
        if 'Furnizor' in neachitate_df.columns and furnizor_filter:
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Furnizor'].isin(furnizor_filter)]
        
        if show_restante and 'Zile Intarziere' in neachitate_df.columns:
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Zile Intarziere'] > 0]
        
        if valuta_filter != "Toate" and 'Valuta' in neachitate_df.columns:
            filtered_neachitate = filtered_neachitate[filtered_neachitate['Valuta'] == valuta_filter]
        
        # Sortare după data scadenței
        if 'Data Scadenta' in filtered_neachitate.columns:
            filtered_neachitate = filtered_neachitate.sort_values('Data Scadenta')
        
        # Afișare tabel
        st.subheader(f"📋 Facturi Neachitate ({len(filtered_neachitate)} înregistrări)")
        
        # Selectez coloanele pentru afișare
        columns_to_show = ['Furnizor', 'Nr Factura', 'Serie', 'Data Factura', 'Data Scadenta', 
                          'Valuta', 'Suma', 'Rest de Plata', 'Zile Intarziere', 'PL']
        available_columns = [col for col in columns_to_show if col in filtered_neachitate.columns]
        
        # Formatez datele pentru afișare
        display_df = filtered_neachitate[available_columns].copy()
        
        # Formatez valorile monetare și datele
        if 'Suma' in display_df.columns:
            display_df['Suma'] = display_df['Suma'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "0")
        if 'Rest de Plata' in display_df.columns:
            display_df['Rest de Plata'] = display_df['Rest de Plata'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "0")
        if 'Data Factura' in display_df.columns:
            display_df['Data Factura'] = display_df['Data Factura'].dt.strftime('%d.%m.%Y')
        if 'Data Scadenta' in display_df.columns:
            display_df['Data Scadenta'] = display_df['Data Scadenta'].dt.strftime('%d.%m.%Y')
        
        # Stylez tabelul pentru a evidenția facturile restante
        def highlight_restante(row):
            try:
                zile = float(row['Zile Intarziere']) if 'Zile Intarziere' in row and pd.notna(row['Zile Intarziere']) else 0
                if zile > 30:
                    return ['background-color: #ffebee'] * len(row)  # Roșu deschis pentru întârziere mare
                elif zile > 0:
                    return ['background-color: #fff3e0'] * len(row)  # Portocaliu deschis pentru întârziere mică
                else:
                    return [''] * len(row)
            except:
                return [''] * len(row)
        
        if 'Zile Intarziere' in display_df.columns:
            styled_df = display_df.style.apply(highlight_restante, axis=1)
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(display_df, use_container_width=True)
        
        # Legendă pentru culori
        if 'Zile Intarziere' in filtered_neachitate.columns:
            st.markdown("""
            **Legendă culori:**
            - 🟡 Galben: Întârziere 1-30 zile
            - 🔴 Roșu: Întârziere peste 30 zile
            """)
        
        # Buton pentru export
        if st.button("📥 Exportă datele filtrate", key="export_neachitate"):
            csv = filtered_neachitate.to_csv(index=False)
            st.download_button(
                label="Descarcă CSV",
                data=csv,
                file_name=f"facturi_neachitate_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="download_neachitate"
            )
        
        # Statistici pentru datele filtrate
        if not filtered_neachitate.empty:
            st.markdown("#### 📊 Statistici Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_filtrat = filtered_neachitate['Rest de Plata'].sum() if 'Rest de Plata' in filtered_neachitate.columns else 0
                valuta = filtered_neachitate['Valuta'].iloc[0] if 'Valuta' in filtered_neachitate.columns and len(filtered_neachitate) > 0 else "RON"
                st.metric("Total Neachitat", f"{total_filtrat:,.2f} {valuta}")
            with col2:
                suma_totala = filtered_neachitate['Suma'].sum() if 'Suma' in filtered_neachitate.columns else 0
                st.metric("Suma Totală Facturi", f"{suma_totala:,.2f} {valuta}")
            with col3:
                valoare_medie_filtrat = filtered_neachitate['Rest de Plata'].mean() if 'Rest de Plata' in filtered_neachitate.columns else 0
                st.metric("Rest Mediu", f"{valoare_medie_filtrat:,.2f} {valuta}")
            with col4:
                zile_medie = filtered_neachitate['Zile Intarziere'].mean() if 'Zile Intarziere' in filtered_neachitate.columns else 0
                st.metric("Întârziere Medie", f"{zile_medie:.0f} zile")
    
    with tab2:
        st.markdown("#### 📥 Facturi Neincasate")
        
        # Încărcare date
        neincasate_df = load_neincasate()
        
        # Calculare metrici
        total_neincasat = neincasate_df['Rest de Incasat'].sum() if 'Rest de Incasat' in neincasate_df.columns else 0
        numar_facturi = len(neincasate_df)
        clienti_unici = neincasate_df['Client'].nunique() if 'Client' in neincasate_df.columns else 0
        
        # Calculare facturi restante (cu întârziere)
        facturi_restante = 0
        if 'Zile Intarziere' in neincasate_df.columns:
            facturi_restante = len(neincasate_df[neincasate_df['Zile Intarziere'] > 0])
        
        # Determinare valută principală
        valuta_principala = "LEI"
        if 'Valuta' in neincasate_df.columns and len(neincasate_df) > 0:
            valuta_principala = neincasate_df['Valuta'].iloc[0]
        
        # Metrici principale
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Neincasat", f"{total_neincasat:,.2f} {valuta_principala}", delta=None, delta_color="inverse")
        with col2:
            st.metric("Facturi Neincasate", f"{numar_facturi:,}")
        with col3:
            st.metric("Clienți", f"{clienti_unici}")
        with col4:
            st.metric("Facturi Restante", f"{facturi_restante}", delta=None, delta_color="inverse")
        
        st.markdown("---")
        
        # Filtrare date
        col1, col2 = st.columns(2)
        with col1:
            if 'Client' in neincasate_df.columns:
                client_filter = st.multiselect(
                    "Filtrează după client:",
                    options=sorted(neincasate_df['Client'].unique()),
                    default=[],
                    key="client_neincasate"
                )
        
        with col2:
            # Filtru pentru facturile restante
            show_restante = st.checkbox("Afișează doar facturile restante", key="restante_neincasate")
        
        # Adaug filtrare după valută și agent
        col3, col4 = st.columns(2)
        with col3:
            if 'Agent' in neincasate_df.columns:
                agenti_disponibili = neincasate_df['Agent'].unique()
                agent_filter = st.selectbox(
                    "Filtrează după agent:",
                    options=["Toți"] + list(agenti_disponibili),
                    key="agent_neincasate"
                )
        
        with col4:
            # Afișez totaluri pe valute
            if 'Valuta' in neincasate_df.columns and 'Rest de Incasat' in neincasate_df.columns:
                st.markdown("**💰 Totaluri pe valute:**")
                for valuta in neincasate_df['Valuta'].unique():
                    total_valuta = neincasate_df[neincasate_df['Valuta'] == valuta]['Rest de Incasat'].sum()
                    st.write(f"• {valuta}: {total_valuta:,.2f}")
        
        # Aplicare filtre
        filtered_neincasate = neincasate_df.copy()
        
        if 'Client' in neincasate_df.columns and client_filter:
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Client'].isin(client_filter)]
        
        if show_restante and 'Zile Intarziere' in neincasate_df.columns:
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Zile Intarziere'] > 0]
        
        if agent_filter != "Toți" and 'Agent' in neincasate_df.columns:
            filtered_neincasate = filtered_neincasate[filtered_neincasate['Agent'] == agent_filter]
        
        # Sortare după data scadenței
        if 'Data Scadenta' in filtered_neincasate.columns:
            filtered_neincasate = filtered_neincasate.sort_values('Data Scadenta')
        
        # Afișare tabel
        st.subheader(f"📋 Facturi Neincasate ({len(filtered_neincasate)} înregistrări)")
        
        # Selectez coloanele pentru afișare
        columns_to_show = ['Client', 'Nr Factura', 'Serie', 'Data Factura', 'Data Scadenta', 
                          'Valuta', 'Suma', 'Rest de Incasat', 'Zile Intarziere', 'Agent']
        available_columns = [col for col in columns_to_show if col in filtered_neincasate.columns]
        
        # Formatez datele pentru afișare
        display_df = filtered_neincasate[available_columns].copy()
        
        # Formatez valorile monetare și datele
        if 'Suma' in display_df.columns:
            display_df['Suma'] = display_df['Suma'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "0")
        if 'Rest de Incasat' in display_df.columns:
            display_df['Rest de Incasat'] = display_df['Rest de Incasat'].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "0")
        if 'Data Factura' in display_df.columns:
            display_df['Data Factura'] = display_df['Data Factura'].dt.strftime('%d.%m.%Y')
        if 'Data Scadenta' in display_df.columns:
            display_df['Data Scadenta'] = display_df['Data Scadenta'].dt.strftime('%d.%m.%Y')
        
        # Stylez tabelul pentru a evidenția facturile restante
        def highlight_restante(row):
            try:
                zile = float(row['Zile Intarziere']) if 'Zile Intarziere' in row and pd.notna(row['Zile Intarziere']) else 0
                if zile > 30:
                    return ['background-color: #ffebee'] * len(row)  # Roșu deschis pentru întârziere mare
                elif zile > 0:
                    return ['background-color: #fff3e0'] * len(row)  # Portocaliu deschis pentru întârziere mică
                else:
                    return [''] * len(row)
            except:
                return [''] * len(row)
        
        if 'Zile Intarziere' in display_df.columns:
            styled_df = display_df.style.apply(highlight_restante, axis=1)
            st.dataframe(styled_df, use_container_width=True)
        else:
            st.dataframe(display_df, use_container_width=True)
        
        # Legendă pentru culori
        if 'Zile Intarziere' in filtered_neincasate.columns:
            st.markdown("""
            **Legendă culori:**
            - 🟡 Galben: Întârziere 1-30 zile
            - 🔴 Roșu: Întârziere peste 30 zile
            """)
        
        # Buton pentru export
        if st.button("📥 Exportă datele filtrate", key="export_neincasate"):
            csv = filtered_neincasate.to_csv(index=False)
            st.download_button(
                label="Descarcă CSV",
                data=csv,
                file_name=f"facturi_neincasate_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                key="download_neincasate"
            )
        
        # Statistici pentru datele filtrate
        if not filtered_neincasate.empty:
            st.markdown("#### 📊 Statistici Filtrate")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_filtrat = filtered_neincasate['Rest de Incasat'].sum() if 'Rest de Incasat' in filtered_neincasate.columns else 0
                valuta = filtered_neincasate['Valuta'].iloc[0] if 'Valuta' in filtered_neincasate.columns and len(filtered_neincasate) > 0 else "RON"
                st.metric("Total Neincasat", f"{total_filtrat:,.2f} {valuta}")
            with col2:
                suma_totala = filtered_neincasate['Suma'].sum() if 'Suma' in filtered_neincasate.columns else 0
                st.metric("Suma Totală Facturi", f"{suma_totala:,.2f} {valuta}")
            with col3:
                valoare_medie_filtrat = filtered_neincasate['Rest de Incasat'].mean() if 'Rest de Incasat' in filtered_neincasate.columns else 0
                st.metric("Rest Mediu", f"{valoare_medie_filtrat:,.2f} {valuta}")
            with col4:
                zile_medie = filtered_neincasate['Zile Intarziere'].mean() if 'Zile Intarziere' in filtered_neincasate.columns else 0
                st.metric("Întârziere Medie", f"{zile_medie:.0f} zile")
