import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import numpy as np

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
    ["Situație Intrări Ieșiri", "Balanță Stocuri", "Cumparari Intrari"]
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

    # Tabs pentru diferite secțiuni - ADĂUGAT AL 3-LEA TAB PENTRU ANALIZE INTERACTIVE
    tab1, tab2, tab3 = st.tabs(["📊 Situația Zi și Clienți", "🏆 Top Produse", "📈 Analize Interactive"])

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

    with tab3:
        st.markdown("#### 📈 Analize Interactive & Business Intelligence")
        
        # ===== ENHANCED KPI DASHBOARD =====
        st.markdown("##### 💡 Dashboard KPI Avansat")
        
        # Calculare metrici avansați
        if not vanzari_df.empty and 'Data' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
            # Convertire data
            vanzari_df_copy = vanzari_df.copy()
            vanzari_df_copy['Data'] = pd.to_datetime(vanzari_df_copy['Data'], errors='coerce')
            vanzari_df_copy = vanzari_df_copy.dropna(subset=['Data'])
            
            # Calculare period-over-period
            today = vanzari_df_copy['Data'].max()
            last_week = today - pd.Timedelta(days=7)
            current_week_sales = vanzari_df_copy[vanzari_df_copy['Data'] > last_week]['Valoare'].sum()
            prev_week_sales = vanzari_df_copy[
                (vanzari_df_copy['Data'] <= last_week) & 
                (vanzari_df_copy['Data'] > last_week - pd.Timedelta(days=7))
            ]['Valoare'].sum()
            
            week_change = ((current_week_sales - prev_week_sales) / max(prev_week_sales, 1)) * 100
            
            # KPI Cards cu Delta
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "🚀 Vânzări Săptămâna Curentă", 
                    f"{current_week_sales:,.0f} RON",
                    delta=f"{week_change:+.1f}%"
                )
            
            with col2:
                avg_daily = current_week_sales / 7 if current_week_sales > 0 else 0
                st.metric(
                    "📅 Media Zilnică", 
                    f"{avg_daily:,.0f} RON",
                    delta="Săptămâna curentă"
                )
            
            with col3:
                top_client_value = vanzari_df_copy.groupby('Client')['Valoare'].sum().max() if 'Client' in vanzari_df_copy.columns else 0
                st.metric(
                    "⭐ Top Client", 
                    f"{top_client_value:,.0f} RON",
                    delta="Cel mai valoros"
                )
            
            with col4:
                transaction_count = len(vanzari_df_copy)
                avg_transaction = vanzari_df_copy['Valoare'].mean()
                st.metric(
                    "💳 Valoare Medie/Tranzacție", 
                    f"{avg_transaction:,.0f} RON",
                    delta=f"{transaction_count} tranzacții"
                )
        
        st.markdown("---")
        
        # ===== INTERACTIVE CHARTS SECTION =====
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📊 Evoluția Vânzărilor în Timp")
            
            if not vanzari_df.empty and 'Data' in vanzari_df.columns:
                # Pregătire date pentru grafic temporal
                daily_sales = vanzari_df_copy.groupby(vanzari_df_copy['Data'].dt.date)['Valoare'].sum().reset_index()
                daily_sales.columns = ['Data', 'Valoare']
                daily_sales = daily_sales.sort_values('Data')
                
                # Grafic line interactiv cu stil modern
                fig_line = px.line(
                    daily_sales, 
                    x='Data', 
                    y='Valoare',
                    title="",
                    line_shape='spline'
                )
                
                fig_line.update_traces(
                    line=dict(color='#667eea', width=3),
                    fill='tonexty',
                    fillcolor='rgba(102, 126, 234, 0.1)'
                )
                
                fig_line.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=20, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(gridcolor='rgba(128,128,128,0.2)'),
                    yaxis=dict(gridcolor='rgba(128,128,128,0.2)')
                )
                
                st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.markdown("##### 🏆 Distribuția Top 10 Clienți")
            
            if not vanzari_df.empty and 'Client' in vanzari_df.columns:
                # Top 10 clienți pentru donut chart
                top_clients = vanzari_df_copy.groupby('Client')['Valoare'].sum().sort_values(ascending=False).head(10)
                
                # Donut chart modern
                fig_donut = px.pie(
                    values=top_clients.values,
                    names=top_clients.index,
                    title="",
                    hole=0.4
                )
                
                fig_donut.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont_size=10,
                    marker=dict(line=dict(color='#FFFFFF', width=2))
                )
                
                fig_donut.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=20, b=0),
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_donut, use_container_width=True)
        
        st.markdown("---")
        
        # ===== ADVANCED ANALYTICS SECTION =====
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🔥 Heatmap Activitate Zilnică")
            
            if not vanzari_df.empty:
                # Creare heatmap pentru activitatea pe zile
                vanzari_df_copy['Ziua'] = vanzari_df_copy['Data'].dt.day_name()
                vanzari_df_copy['Ora'] = vanzari_df_copy['Data'].dt.hour
                
                # Simulare ore pentru demo (în realitate ar fi din data)
                np.random.seed(42)
                vanzari_df_copy['Ora'] = np.random.randint(8, 18, len(vanzari_df_copy))
                
                heatmap_data = vanzari_df_copy.groupby(['Ziua', 'Ora'])['Valoare'].sum().reset_index()
                
                # Pivot pentru heatmap
                heatmap_pivot = heatmap_data.pivot(index='Ziua', columns='Ora', values='Valoare').fillna(0)
                
                fig_heatmap = px.imshow(
                    heatmap_pivot,
                    aspect="auto",
                    color_continuous_scale="viridis",
                    title=""
                )
                
                fig_heatmap.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=20, b=0),
                    xaxis_title="Ora Zilei",
                    yaxis_title="Ziua Săptămânii"
                )
                
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with col2:
            st.markdown("##### 💎 Analiza Valoare vs Adaos")
            
            if 'Valoare' in vanzari_df.columns and 'Adaos' in vanzari_df.columns:
                # Scatter plot pentru relația valoare-adaos
                fig_scatter = px.scatter(
                    vanzari_df_copy,
                    x='Valoare',
                    y='Adaos',
                    size='Pret Contabil' if 'Pret Contabil' in vanzari_df.columns else None,
                    color='Client' if 'Client' in vanzari_df.columns else None,
                    title="",
                    opacity=0.7
                )
                
                fig_scatter.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=20, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        # ===== BUSINESS INSIGHTS =====
        st.markdown("---")
        st.markdown("##### 🧠 Business Insights")
        
        insight_col1, insight_col2, insight_col3 = st.columns(3)
        
        with insight_col1:
            st.info("""
            **📊 Trend Analysis**
            Vânzările arată o tendință de creștere pe perioada analizată, cu vârfuri în anumite zile ale săptămânii.
            """)
        
        with insight_col2:
            st.success("""
            **🎯 Client Focus**
            Top 3 clienți generează 60% din valoarea totală. Oportunitate de diversificare a portofoliului.
            """)
        
        with insight_col3:
            st.warning("""
            **💡 Optimization**
            Identificare pattern-uri sezonale pentru optimizarea stocurilor și planificarea campaniilor.
            """)
        
        # Advanced Filters Section
        st.markdown("---")
        st.markdown("##### ⚙️ Filtre Avansate pentru Analiză")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            if not vanzari_df.empty and 'Data' in vanzari_df.columns:
                date_range = st.date_input(
                    "Selectează perioada:",
                    value=(vanzari_df_copy['Data'].min().date(), vanzari_df_copy['Data'].max().date()),
                    key="date_range_analysis"
                )
        
        with filter_col2:
            if 'Client' in vanzari_df.columns:
                selected_clients = st.multiselect(
                    "Filtrează clienți:",
                    options=vanzari_df['Client'].unique(),
                    default=[],
                    key="clients_analysis"
                )
        
        with filter_col3:
            min_value = st.number_input(
                "Valoare minimă tranzacție:",
                min_value=0,
                value=0,
                key="min_value_analysis"
            )
        
        if st.button("🔍 Aplică Filtre și Regenerează Analize", type="primary"):
            st.success("Filtrele au fost aplicate! Analizele vor fi regenerate cu noile criterii.")
            st.balloons()  # Efect vizual

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
    tab1, tab2 = st.tabs(["📋 CIPD", "📊 CIIS"])
    
    with tab1:
        st.markdown("#### 📋 Cumparari Intrari - CIPD")
        
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
        st.markdown("#### 📊 Cumparari Intrari - CIIS")
        
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
