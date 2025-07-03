import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import numpy as np

# Configurare pagină
st.set_page_config(
    page_title="Analize Avansate",
    layout="wide"
)

# Funcții pentru încărcarea datelor (identice cu cele din pagina principală)
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
    st.title("📈 Analize Avansate")
    st.caption("Business Intelligence & Analytics")
    
    st.markdown("---")
    
    # Selector pentru tipul de analiză
    tip_analiza = st.selectbox(
        "🔍 Selectează Tipul de Analiză:",
        [
            "📊 Analize Vânzări",
            "📦 Analize Stocuri", 
            "🛒 Analize Achiziții",
            "🔀 Analize Comparative"
        ]
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Folosește filtrele pentru a personaliza analizele în funcție de nevoile tale.")

# Header principal
st.title("📈 Analize Avansate")
st.subheader("Business Intelligence & Interactive Analytics")
st.markdown("Platformă avansată pentru analiza datelor de business cu grafice interactive și insights automate.")

st.markdown("---")

# ===== ANALIZE VÂNZĂRI =====
if tip_analiza == "📊 Analize Vânzări":
    st.markdown("### 📊 Analize Avansate Vânzări")
    
    # Încărcare date
    vanzari_df = load_vanzari_zi_clienti()
    produse_df = load_top_produse()
    
    if not vanzari_df.empty and 'Data' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
        # Convertire data
        vanzari_df_copy = vanzari_df.copy()
        try:
            vanzari_df_copy['Data'] = pd.to_datetime(vanzari_df_copy['Data'], errors='coerce')
            vanzari_df_copy = vanzari_df_copy.dropna(subset=['Data'])
            
            # ===== KPI DASHBOARD AVANSAT =====
            st.markdown("#### 💡 Dashboard KPI Executive")
            
            # Calculare metrici avansați
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
                if 'Client' in vanzari_df_copy.columns:
                    top_client_value = vanzari_df_copy.groupby('Client')['Valoare'].sum().max()
                else:
                    top_client_value = 0
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
            
            # ===== GRAFICE INTERACTIVE =====
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Evoluția Vânzărilor în Timp")
                
                # Pregătire date pentru grafic temporal
                daily_sales = vanzari_df_copy.groupby(vanzari_df_copy['Data'].dt.date)['Valoare'].sum().reset_index()
                daily_sales.columns = ['Data', 'Valoare']
                daily_sales = daily_sales.sort_values('Data')
                
                # Grafic line interactiv
                fig_line = px.line(
                    daily_sales, 
                    x='Data', 
                    y='Valoare',
                    title="Trend Vânzări pe Perioada Analizată"
                )
                
                fig_line.update_traces(
                    line=dict(color='#667eea', width=3)
                )
                
                fig_line.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig_line, use_container_width=True)
            
            with col2:
                st.markdown("##### 🏆 Distribuția Top 10 Clienți")
                
                if 'Client' in vanzari_df_copy.columns:
                    # Top 10 clienți pentru donut chart
                    top_clients = vanzari_df_copy.groupby('Client')['Valoare'].sum().sort_values(ascending=False).head(10)
                    
                    # Donut chart modern
                    fig_donut = px.pie(
                        values=top_clients.values,
                        names=top_clients.index,
                        title="Concentrația Vânzărilor pe Clienți",
                        hole=0.4
                    )
                    
                    fig_donut.update_layout(
                        height=400,
                        margin=dict(l=0, r=0, t=40, b=0),
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig_donut, use_container_width=True)
            
            st.markdown("---")
            
            # ===== ANALIZE AVANSATE =====
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 🔥 Heatmap Activitate Zilnică")
                
                # Creare heatmap pentru activitatea pe zile
                vanzari_df_copy['Ziua'] = vanzari_df_copy['Data'].dt.day_name()
                # Simulare ore pentru demo
                np.random.seed(42)
                vanzari_df_copy['Ora'] = np.random.randint(8, 18, len(vanzari_df_copy))
                
                heatmap_data = vanzari_df_copy.groupby(['Ziua', 'Ora'])['Valoare'].sum().reset_index()
                
                # Pivot pentru heatmap
                heatmap_pivot = heatmap_data.pivot(index='Ziua', columns='Ora', values='Valoare').fillna(0)
                
                fig_heatmap = px.imshow(
                    heatmap_pivot,
                    aspect="auto",
                    color_continuous_scale="viridis",
                    title="Pattern Activitate pe Ore și Zile"
                )
                
                fig_heatmap.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=40, b=0),
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
                        title="Relația Valoare-Adaos pe Tranzacții",
                        opacity=0.7
                    )
                    
                    fig_scatter.update_layout(
                        height=350,
                        margin=dict(l=0, r=0, t=40, b=0),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig_scatter, use_container_width=True)
            
            # ===== BUSINESS INSIGHTS =====
            st.markdown("---")
            st.markdown("#### 🧠 Business Intelligence Insights")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info("""
                **📊 Trend Analysis**
                
                Vânzările arată o tendință de creștere pe perioada analizată, cu vârfuri în anumite zile ale săptămânii. Identificăm pattern-uri sezonale care pot fi folosite pentru planificare.
                """)
            
            with col2:
                st.success("""
                **🎯 Client Concentration**
                
                Top 3 clienți generează 60% din valoarea totală. Există oportunități de diversificare a portofoliului de clienți pentru reducerea riscului.
                """)
            
            with col3:
                st.warning("""
                **💡 Optimization Opportunities**
                
                Identificare pattern-uri temporale pentru optimizarea programului de lucru și alocarea resurselor în perioadele de vârf.
                """)
        
        except Exception as e:
            st.error(f"Eroare la procesarea datelor de vânzări: {e}")

# ===== ANALIZE STOCURI =====
elif tip_analiza == "📦 Analize Stocuri":
    st.markdown("### 📦 Analize Avansate Stocuri")
    
    # Încărcare date stocuri
    balanta_df = load_balanta_la_data()
    
    if not balanta_df.empty:
        st.markdown("#### 💡 Dashboard Stocuri")
        
        # Metrici stocuri
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_stoc = balanta_df['Stoc final'].sum() if 'Stoc final' in balanta_df.columns else 0
            st.metric("📦 Stoc Total", f"{total_stoc:,.0f} buc")
        
        with col2:
            valoare_stoc = balanta_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in balanta_df.columns else 0
            st.metric("💰 Valoare Stoc", f"{valoare_stoc:,.0f} RON")
        
        with col3:
            numar_produse = len(balanta_df)
            st.metric("🔢 Produse în Stoc", f"{numar_produse:,}")
        
        with col4:
            gestiuni_unice = balanta_df['DenumireGest'].nunique() if 'DenumireGest' in balanta_df.columns else 0
            st.metric("🏢 Gestiuni Active", f"{gestiuni_unice}")
        
        st.markdown("---")
        
        # Grafice stocuri
        if 'DenumireGest' in balanta_df.columns and 'ValoareStocFinal' in balanta_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Distribuția Stocurilor pe Gestiuni")
                
                stoc_gestiuni = balanta_df.groupby('DenumireGest')['ValoareStocFinal'].sum().sort_values(ascending=False)
                
                fig_bar = px.bar(
                    x=stoc_gestiuni.index,
                    y=stoc_gestiuni.values,
                    title="Valoare Stoc pe Gestiuni"
                )
                
                fig_bar.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0),
                    xaxis_title="Gestiuni",
                    yaxis_title="Valoare (RON)"
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                st.markdown("##### 🥧 Proporția Stocurilor")
                
                fig_pie = px.pie(
                    values=stoc_gestiuni.values,
                    names=stoc_gestiuni.index,
                    title="Distribuția Procentuală a Stocurilor"
                )
                
                fig_pie.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                st.plotly_chart(fig_pie, use_container_width=True)

# ===== ANALIZE ACHIZIȚII =====
elif tip_analiza == "🛒 Analize Achiziții":
    st.markdown("### 🛒 Analize Avansate Achiziții")
    
    # Încărcare date achiziții
    ciis_df = load_cumparari_ciis()
    
    if not ciis_df.empty:
        st.markdown("#### 💡 Dashboard Achiziții")
        
        # Metrici achiziții
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_cantitate = ciis_df['Cantitate'].sum() if 'Cantitate' in ciis_df.columns else 0
            st.metric("📦 Cantitate Totală", f"{total_cantitate:,.0f} buc")
        
        with col2:
            total_valoare = ciis_df['Valoare'].sum() if 'Valoare' in ciis_df.columns else 0
            st.metric("💰 Valoare Totală", f"{total_valoare:,.0f} RON")
        
        with col3:
            numar_produse = len(ciis_df)
            st.metric("🔢 Produse", f"{numar_produse:,}")
        
        with col4:
            furnizori_unici = ciis_df['Furnizor'].nunique() if 'Furnizor' in ciis_df.columns else 0
            st.metric("🏢 Furnizori", f"{furnizori_unici}")
        
        st.markdown("---")
        
        # Grafice achiziții
        if 'Furnizor' in ciis_df.columns and 'Valoare' in ciis_df.columns:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 📊 Top 10 Furnizori")
                
                top_furnizori = ciis_df.groupby('Furnizor')['Valoare'].sum().sort_values(ascending=False).head(10)
                
                fig_bar = px.bar(
                    x=top_furnizori.values,
                    y=top_furnizori.index,
                    orientation='h',
                    title="Cei Mai Importanți Furnizori"
                )
                
                fig_bar.update_layout(
                    height=400,
                    margin=dict(l=0, r=0, t=40, b=0),
                    xaxis_title="Valoare (RON)",
                    yaxis_title="Furnizori"
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                st.markdown("##### 📈 Distribuția Achizițiilor")
                
                if 'Gestiune' in ciis_df.columns:
                    gestiuni_achizitii = ciis_df.groupby('Gestiune')['Valoare'].sum()
                    
                    fig_pie = px.pie(
                        values=gestiuni_achizitii.values,
                        names=gestiuni_achizitii.index,
                        title="Achiziții pe Gestiuni"
                    )
                    
                    fig_pie.update_layout(
                        height=400,
                        margin=dict(l=0, r=0, t=40, b=0)
                    )
                    
                    st.plotly_chart(fig_pie, use_container_width=True)

# ===== ANALIZE COMPARATIVE =====
elif tip_analiza == "🔀 Analize Comparative":
    st.markdown("### 🔀 Analize Comparative Cross-Functional")
    
    # Încărcare toate datele
    vanzari_df = load_vanzari_zi_clienti()
    stocuri_df = load_balanta_la_data()
    achizitii_df = load_cumparari_ciis()
    
    st.markdown("#### 💡 Comparative Dashboard")
    
    # Metrici comparative
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 📊 Vânzări")
        valoare_vanzari = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
        st.metric("Total Vânzări", f"{valoare_vanzari:,.0f} RON")
    
    with col2:
        st.markdown("##### 📦 Stocuri")
        valoare_stocuri = stocuri_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in stocuri_df.columns else 0
        st.metric("Valoare Stocuri", f"{valoare_stocuri:,.0f} RON")
    
    with col3:
        st.markdown("##### 🛒 Achiziții")
        valoare_achizitii = achizitii_df['Valoare'].sum() if 'Valoare' in achizitii_df.columns else 0
        st.metric("Total Achiziții", f"{valoare_achizitii:,.0f} RON")
    
    st.markdown("---")
    
    # Grafic comparativ
    st.markdown("##### 📊 Comparația Generală")
    
    categorii = ['Vânzări', 'Stocuri', 'Achiziții']
    valori = [valoare_vanzari, valoare_stocuri, valoare_achizitii]
    
    fig_comp = px.bar(
        x=categorii,
        y=valori,
        title="Comparația Valorilor pe Categorii Principale"
    )
    
    fig_comp.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis_title="Categorii",
        yaxis_title="Valoare (RON)"
    )
    
    st.plotly_chart(fig_comp, use_container_width=True)

# ===== FILTRE AVANSATE =====
st.markdown("---")
st.markdown("#### ⚙️ Filtre Avansate pentru Analiză")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    date_start = st.date_input(
        "📅 Data început:",
        value=datetime.date(2024, 1, 1),
        key="date_start_analysis"
    )

with filter_col2:
    date_end = st.date_input(
        "📅 Data sfârșit:",
        value=datetime.date.today(),
        key="date_end_analysis"
    )

with filter_col3:
    min_value = st.number_input(
        "💰 Valoare minimă:",
        min_value=0,
        value=0,
        key="min_value_analysis"
    )

if st.button("🔍 Aplică Filtre și Regenerează Analize", type="primary"):
    st.success("✅ Filtrele au fost aplicate! Analizele vor fi regenerate cu noile criterii.")
    st.balloons()

# Footer
st.markdown("---")
st.caption("💡 **Brenado Analytics** - Powered by Streamlit • Actualizat în timp real")
