import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configurare pagină cu tema dark modern
st.set_page_config(
    page_title="Brenado For House",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS pentru design modern
st.markdown("""
<style>
    /* Dark theme modern */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Metric cards styling */
    div[data-testid="metric-container"] {
        background-color: #1e2329;
        border: 1px solid #2d3339;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Headers styling */
    h1 {
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #e0e0e0;
        font-weight: 600;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #1e2329;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #a0a0a0;
        font-size: 16px;
        font-weight: 500;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3d4551;
        color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background-color: #1e2329;
        border-radius: 8px;
        border: 1px solid #2d3339;
    }
    
    /* Success alerts */
    .stSuccess {
        background-color: rgba(0, 255, 0, 0.1);
        border-left: 4px solid #00ff00;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #1e2329 0%, #2d3339 100%);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid #3d4551;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Modern button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3d4551 0%, #4d5561 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #4d5561 0%, #5d6571 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Funcții pentru încărcarea datelor (păstrate identice)
@st.cache_data
def load_vanzari_zi_clienti():
    """Încarcă datele din Excel - Vânzări"""
    try:
        df = pd.read_excel("data/svzc.xlsx")
        # Conversie dată din format Excel numeric
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime('1900-01-01') + pd.to_timedelta(df['Data'] - 2, unit='D')
        return df
    except:
        # Date demo mai realiste
        dates = pd.date_range(start='2025-05-01', end='2025-05-30', freq='D')
        clients = [f'Client {i}' for i in range(1, 51)]
        data = []
        for date in dates:
            for _ in range(np.random.randint(5, 25)):
                client = np.random.choice(clients)
                valoare = np.random.randint(500, 10000)
                data.append({
                    'Data': date,
                    'Client': client,
                    'Pret Contabil': valoare * 0.1,
                    'Valoare': valoare,
                    'Adaos': valoare * 0.15,
                    'Cost': valoare * 0.85
                })
        return pd.DataFrame(data)

@st.cache_data
def load_top_produse():
    """Încarcă datele din Excel - Top produse"""
    try:
        df = pd.read_excel("data/svtp.xlsx")
        return df
    except:
        produse = [f'Produs {i}' for i in range(1, 101)]
        data = []
        for produs in produse:
            cantitate = np.random.randint(10, 500)
            valoare = np.random.randint(1000, 50000)
            data.append({
                'Denumire': produs,
                'Cantitate': cantitate,
                'Valoare': valoare,
                'Adaos': valoare * 0.15
            })
        return pd.DataFrame(data)

@st.cache_data
def load_balanta_la_data():
    """Încarcă datele din Excel - Balanță la dată"""
    try:
        df = pd.read_excel("data/LaData.xlsx")
        return df
    except:
        gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța', 'Showroom Cluj']
        produse = [f'Produs {i}' for i in range(1, 201)]
        data = []
        for gest in gestiuni:
            for _ in range(50):
                produs = np.random.choice(produse)
                stoc = np.random.randint(10, 500)
                data.append({
                    'DenumireGest': gest,
                    'Denumire': produs,
                    'Stoc final': stoc,
                    'ValoareStocFinal': stoc * np.random.randint(50, 500)
                })
        return pd.DataFrame(data)

@st.cache_data
def load_balanta_perioada():
    """Încarcă datele din Excel - Balanță pe perioadă"""
    try:
        df = pd.read_excel("data/Perioada.xlsx")
        return df
    except:
        gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța', 'Showroom Cluj']
        produse = [f'Produs {i}' for i in range(1, 201)]
        data = []
        for gest in gestiuni:
            for _ in range(50):
                produs = np.random.choice(produse)
                stoc = np.random.randint(10, 500)
                data.append({
                    'Denumire gestiune': gest,
                    'Denumire': produs,
                    'Stoc final': stoc,
                    'Valoare intrare': stoc * np.random.randint(50, 500),
                    'ZileVechime': np.random.randint(1, 180)
                })
        return pd.DataFrame(data)

@st.cache_data
def load_cumparari_cipd():
    """Încarcă datele din Excel - Cumparari CIPD"""
    try:
        df = pd.read_excel("data/CIPD.xlsx")
        return df
    except:
        gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța']
        furnizori = [f'Furnizor {i}' for i in range(1, 21)]
        produse = [f'Produs {i}' for i in range(1, 101)]
        data = []
        for _ in range(200):
            cantitate = np.random.randint(10, 200)
            pret = np.random.randint(50, 500)
            data.append({
                'Gestiune': np.random.choice(gestiuni),
                'Denumire': np.random.choice(produse),
                'Cantitate': cantitate,
                'Pret': pret,
                'Valoare': cantitate * pret,
                'Furnizor': np.random.choice(furnizori)
            })
        return pd.DataFrame(data)

@st.cache_data
def load_cumparari_ciis():
    """Încarcă datele din Excel - Cumparari CIIS"""
    try:
        df = pd.read_excel("data/CIIS.xlsx")
        return df
    except:
        gestiuni = ['Depozit Central', 'Showroom București', 'Depozit Constanța']
        furnizori = [f'Furnizor {i}' for i in range(1, 21)]
        produse = [f'Produs {i}' for i in range(1, 101)]
        grupe = ['Materiale Construcții', 'Instalații Sanitare', 'Instalații Electrice', 'Finisaje', 'Unelte']
        data = []
        for _ in range(300):
            cantitate = np.random.randint(10, 200)
            pret = np.random.randint(50, 500)
            data.append({
                'Gestiune': np.random.choice(gestiuni),
                'Denumire': np.random.choice(produse),
                'Denumire grupa': np.random.choice(grupe),
                'Cantitate': cantitate,
                'Pret': pret,
                'Valoare': cantitate * pret,
                'Furnizor': np.random.choice(furnizori)
            })
        return pd.DataFrame(data)

# Sidebar modern cu gradient
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #ffffff; margin-bottom: 5px;'>🏠 BRENADO</h1>
        <h3 style='color: #888; margin-top: 0; font-weight: 300;'>For House</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📊 Dashboard Analytics")
    st.markdown("Segmentul rezidențial premium")
    
    # Quick stats în sidebar
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    vanzari_df = load_vanzari_zi_clienti()
    st.metric("Total Vânzări Mai", f"{vanzari_df['Valoare'].sum()/1000000:.1f}M RON")
    st.metric("Clienți Activi", f"{vanzari_df['Client'].nunique()}")

# Header principal cu gradient
st.markdown("""
<div style='background: linear-gradient(135deg, #1e2329 0%, #2d3339 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 30px;'>
    <h1 style='margin: 0; color: #ffffff;'>Brenado For House Dashboard</h1>
    <p style='margin: 10px 0 0 0; color: #888; font-size: 18px;'>
        Business Intelligence pentru segmentul rezidențial • Mai 2025
    </p>
</div>
""", unsafe_allow_html=True)

# Selectare categorie cu cards moderne
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Vânzări", use_container_width=True, key="btn1"):
        st.session_state.category = "Vânzări"
with col2:
    if st.button("📦 Balanță Stocuri", use_container_width=True, key="btn2"):
        st.session_state.category = "Balanță Stocuri"
with col3:
    if st.button("🛒 Cumpărări Intrări", use_container_width=True, key="btn3"):
        st.session_state.category = "Cumparari Intrari"

# Initialize session state
if 'category' not in st.session_state:
    st.session_state.category = "Vânzări"

category = st.session_state.category

st.markdown("---")

# ===== Vânzări =====
if category == "Vânzări":
    st.markdown("## 📊 Vânzări")
    
    # Încărcare date
    vanzari_df = load_vanzari_zi_clienti()
    produse_df = load_top_produse()

    # Calculare metrici cu trend indicators
    total_valoare = vanzari_df['Valoare'].sum()
    numar_clienti = vanzari_df['Client'].nunique()
    numar_produse = len(produse_df)
    valoare_medie = vanzari_df['Valoare'].mean()
    
    # KPI Cards cu gradient și iconuri
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #888; margin: 0;'>Vânzări Totale</h4>
            <h2 style='color: #4CAF50; margin: 5px 0;'>{:,.0f} RON</h2>
            <p style='color: #888; margin: 0; font-size: 14px;'>↑ +12.5% vs luna trecută</p>
        </div>
        """.format(total_valoare), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #888; margin: 0;'>Clienți Unici</h4>
            <h2 style='color: #2196F3; margin: 5px 0;'>{}</h2>
            <p style='color: #888; margin: 0; font-size: 14px;'>↑ +8 clienți noi</p>
        </div>
        """.format(numar_clienti), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #888; margin: 0;'>Produse Active</h4>
            <h2 style='color: #FF9800; margin: 5px 0;'>{}</h2>
            <p style='color: #888; margin: 0; font-size: 14px;'>Din 800+ SKU total</p>
        </div>
        """.format(numar_produse), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='info-box'>
            <h4 style='color: #888; margin: 0;'>Valoare Medie</h4>
            <h2 style='color: #9C27B0; margin: 5px 0;'>{:,.0f} RON</h2>
            <p style='color: #888; margin: 0; font-size: 14px;'>Per tranzacție</p>
        </div>
        """.format(valoare_medie), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs pentru diferite secțiuni
    tab1, tab2, tab3 = st.tabs(["📊 Analiză Vânzări", "🏆 Top Produse", "📈 Insights"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📈 Evoluție Vânzări Zilnice")
            
            # Grafic linie cu design modern
            daily_sales = vanzari_df.groupby('Data')['Valoare'].sum().reset_index()
            
            fig_line = px.line(daily_sales, x='Data', y='Valoare', 
                              title='Trend Vânzări Mai 2025',
                              labels={'Valoare': 'Valoare (RON)', 'Data': 'Data'})
            
            fig_line.update_traces(line_color='#4CAF50', line_width=3)
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title_font_size=20,
                hovermode='x unified',
                showlegend=False,
                xaxis=dict(gridcolor='#2d3339'),
                yaxis=dict(gridcolor='#2d3339')
            )
            
            # Adaugă trend line
            z = np.polyfit(range(len(daily_sales)), daily_sales['Valoare'], 1)
            p = np.poly1d(z)
            fig_line.add_trace(go.Scatter(
                x=daily_sales['Data'],
                y=p(range(len(daily_sales))),
                mode='lines',
                name='Trend',
                line=dict(color='#FF9800', width=2, dash='dash')
            ))
            
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Top 5 Clienți")
            
            # Donut chart pentru top clienți
            top_clients = vanzari_df.groupby('Client')['Valoare'].sum().nlargest(5).reset_index()
            
            fig_donut = px.pie(top_clients, values='Valoare', names='Client', 
                              hole=0.6, title='Distribuție Top Clienți')
            
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            fig_donut.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                showlegend=False,
                title_font_size=16
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # Tabel interactiv cu filtrare
        st.markdown("### 📋 Detalii Tranzacții")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            client_filter = st.multiselect(
                "🔍 Filtrează după client:",
                options=vanzari_df['Client'].unique(),
                default=[]
            )
        with col2:
            date_range = st.date_input(
                "📅 Perioada:",
                value=(vanzari_df['Data'].min(), vanzari_df['Data'].max()),
                min_value=vanzari_df['Data'].min(),
                max_value=vanzari_df['Data'].max()
            )
        
        # Aplicare filtre
        filtered_df = vanzari_df.copy()
        if client_filter:
            filtered_df = filtered_df[filtered_df['Client'].isin(client_filter)]
        if len(date_range) == 2:
            filtered_df = filtered_df[(filtered_df['Data'] >= pd.to_datetime(date_range[0])) & 
                                    (filtered_df['Data'] <= pd.to_datetime(date_range[1]))]
        
        # Afișare metrici pentru datele filtrate
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Filtrat", f"{filtered_df['Valoare'].sum():,.0f} RON")
        with col2:
            st.metric("Tranzacții", len(filtered_df))
        with col3:
            st.metric("Valoare Medie", f"{filtered_df['Valoare'].mean():,.0f} RON")
        with col4:
            st.metric("Adaos Total", f"{filtered_df['Adaos'].sum():,.0f} RON")
        
        # Tabel stilizat
        st.dataframe(
            filtered_df.style.format({
                'Pret Contabil': '{:,.0f} RON',
                'Valoare': '{:,.0f} RON',
                'Adaos': '{:,.0f} RON',
                'Cost': '{:,.0f} RON'
            }).background_gradient(subset=['Valoare'], cmap='Greens'),
            use_container_width=True,
            height=400
        )

    with tab2:
        st.subheader("🏆 Analiza Top Produse")
        
        col1, col2 = st.columns([3, 1])
        
        with col2:
            show_option = st.selectbox(
                "📊 Afișează:",
                ["Top 10", "Top 20", "Top 50", "Top 100"],
                key="show_products"
            )
            
            chart_type = st.radio(
                "📈 Tip grafic:",
                ["Bar Chart", "Treemap", "Sunburst"],
                key="chart_type"
            )
        
        with col1:
            # Procesare date
            n_products = int(show_option.split()[1])
            top_produse = produse_df.nlargest(n_products, 'Valoare')
            
            if chart_type == "Bar Chart":
                # Bar chart horizontal
                fig_bar = px.bar(top_produse.head(20), y='Denumire', x='Valoare',
                                orientation='h', title=f'{show_option} Produse după Valoare',
                                color='Valoare', color_continuous_scale='Viridis')
                
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    title_font_size=20,
                    showlegend=False,
                    xaxis=dict(gridcolor='#2d3339'),
                    yaxis=dict(gridcolor='#2d3339', autorange="reversed")
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
                
            elif chart_type == "Treemap":
                # Treemap pentru vizualizare ierarhică
                fig_tree = px.treemap(top_produse, path=['Denumire'], values='Valoare',
                                    title=f'{show_option} Produse - Treemap',
                                    color='Adaos', color_continuous_scale='RdYlGn')
                
                fig_tree.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    title_font_size=20
                )
                
                st.plotly_chart(fig_tree, use_container_width=True)
                
            else:  # Sunburst
                # Sunburst chart
                fig_sun = px.sunburst(top_produse.head(30), path=['Denumire'], values='Valoare',
                                    title=f'{show_option} Produse - Sunburst',
                                    color='Valoare', color_continuous_scale='Plasma')
                
                fig_sun.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ffffff',
                    title_font_size=20
                )
                
                st.plotly_chart(fig_sun, use_container_width=True)
        
        # Statistici produse în cards
        st.markdown("### 📊 Statistici Produse")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            best_product = produse_df.loc[produse_df['Valoare'].idxmax()]
            st.info(f"**🥇 Top Produs**\n\n{best_product['Denumire']}\n\n{best_product['Valoare']:,.0f} RON")
        
        with col2:
            st.info(f"**📦 Cantitate Totală**\n\n{produse_df['Cantitate'].sum():,.0f} buc\n\nDin toate produsele")
        
        with col3:
            st.info(f"**💰 Valoare Totală**\n\n{produse_df['Valoare'].sum():,.0f} RON\n\nTotal merchandise")
        
        with col4:
            avg_margin = (produse_df['Adaos'].sum() / produse_df['Valoare'].sum() * 100)
            st.info(f"**📈 Marjă Medie**\n\n{avg_margin:.1f}%\n\nProfit margin")

    with tab3:
        st.subheader("💡 Business Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Analiza pe zile ale săptămânii
            vanzari_df['DayOfWeek'] = vanzari_df['Data'].dt.day_name()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            daily_pattern = vanzari_df.groupby('DayOfWeek')['Valoare'].agg(['sum', 'count', 'mean']).reset_index()
            daily_pattern['DayOfWeek'] = pd.Categorical(daily_pattern['DayOfWeek'], categories=day_order, ordered=True)
            daily_pattern = daily_pattern.sort_values('DayOfWeek')
            
            fig_pattern = go.Figure()
            fig_pattern.add_trace(go.Bar(
                x=daily_pattern['DayOfWeek'],
                y=daily_pattern['sum'],
                name='Vânzări Totale',
                marker_color='#4CAF50',
                yaxis='y'
            ))
            
            fig_pattern.add_trace(go.Scatter(
                x=daily_pattern['DayOfWeek'],
                y=daily_pattern['count'],
                name='Nr. Tranzacții',
                line=dict(color='#FF9800', width=3),
                yaxis='y2'
            ))
            
            fig_pattern.update_layout(
                title='Pattern Săptămânal Vânzări',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                yaxis=dict(title='Valoare (RON)', gridcolor='#2d3339'),
                yaxis2=dict(title='Nr. Tranzacții', overlaying='y', side='right', gridcolor='#2d3339'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_pattern, use_container_width=True)
        
        with col2:
            # Distribuția valorilor tranzacțiilor
            fig_dist = px.histogram(vanzari_df, x='Valoare', nbins=30,
                                  title='Distribuția Valorilor Tranzacțiilor',
                                  labels={'count': 'Frecvență', 'Valoare': 'Valoare Tranzacție (RON)'})
            
            fig_dist.update_traces(marker_color='#2196F3')
            fig_dist.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                xaxis=dict(gridcolor='#2d3339'),
                yaxis=dict(gridcolor='#2d3339')
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Insights automate
        st.markdown("### 🎯 Insights Automate")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            best_day = daily_pattern.loc[daily_pattern['sum'].idxmax()]
            st.success(f"""
            **📈 Cea mai bună zi**
            
            **{best_day['DayOfWeek']}** generează cele mai mari vânzări:
            - Valoare: **{best_day['sum']:,.0f} RON**
            - Tranzacții: **{best_day['count']:.0f}**
            - Medie/tranzacție: **{best_day['mean']:,.0f} RON**
            """)
        
        with col2:
            top_20_percent = int(len(vanzari_df) * 0.2)
            top_20_value = vanzari_df.nlargest(top_20_percent, 'Valoare')['Valoare'].sum()
            percentage = (top_20_value / vanzari_df['Valoare'].sum()) * 100
            
            st.info(f"""
            **🎯 Principiul Pareto**
            
            Top **20%** din tranzacții generează **{percentage:.1f}%** din vânzări
            - Valoare top 20%: **{top_20_value:,.0f} RON**
            - Focus pe clienții premium
            """)
        
        with col3:
            growth_rate = ((daily_sales['Valoare'].iloc[-7:].mean() / daily_sales['Valoare'].iloc[:7].mean()) - 1) * 100
            
            if growth_rate > 0:
                st.success(f"""
                **📊 Trend Pozitiv**
                
                Creștere de **+{growth_rate:.1f}%** în ultima săptămână vs prima
                - Momentum pozitiv
                - Recomandare: Menține strategia actuală
                """)
            else:
                st.warning(f"""
                **📉 Atenție Trend**
                
                Scădere de **{growth_rate:.1f}%** în ultima săptămână
                - Necesită analiză detaliată
                - Verifică factorii externi
                """)

# ===== BALANȚĂ STOCURI =====
elif category == "Balanță Stocuri":
    st.markdown("## 📦 Balanță Stocuri")
    
    # Tabs pentru subcategorii
    tab1, tab2 = st.tabs(["📅 Stoc Curent", "📊 Analiza pe Perioadă"])
    
    with tab1:
        st.markdown("### 📅 Situația Curentă a Stocurilor")
        
        # Încărcare date
        balanta_df = load_balanta_la_data()
        
        # KPI Cards moderne
        col1, col2, col3, col4 = st.columns(4)
        
        total_stoc = balanta_df['Stoc final'].sum()
        valoare_stoc = balanta_df['ValoareStocFinal'].sum()
        numar_produse = len(balanta_df)
        gestiuni_unice = balanta_df['DenumireGest'].nunique()
        
        with col1:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Stoc Total</h4>
                <h2 style='color: #4CAF50; margin: 5px 0;'>{total_stoc:,.0f} buc</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>În toate gestiunile</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Valoare Stoc</h4>
                <h2 style='color: #2196F3; margin: 5px 0;'>{valoare_stoc/1000000:.1f}M RON</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Capital imobilizat</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>SKU Active</h4>
                <h2 style='color: #FF9800; margin: 5px 0;'>{numar_produse:,}</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Produse diferite</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Gestiuni</h4>
                <h2 style='color: #9C27B0; margin: 5px 0;'>{gestiuni_unice}</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Locații active</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Vizualizări stocuri
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Grafic distribuție stocuri pe gestiuni
            stock_by_location = balanta_df.groupby('DenumireGest')['ValoareStocFinal'].sum().reset_index()
            
            fig_locations = px.bar(stock_by_location, x='DenumireGest', y='ValoareStocFinal',
                                 title='Distribuția Valorii Stocurilor pe Gestiuni',
                                 labels={'ValoareStocFinal': 'Valoare Stoc (RON)', 'DenumireGest': 'Gestiune'},
                                 color='ValoareStocFinal', color_continuous_scale='Viridis')
            
            fig_locations.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title_font_size=20,
                showlegend=False,
                xaxis=dict(gridcolor='#2d3339'),
                yaxis=dict(gridcolor='#2d3339')
            )
            
            st.plotly_chart(fig_locations, use_container_width=True)
        
        with col2:
            # Pie chart pentru proporții
            fig_pie = px.pie(stock_by_location, values='ValoareStocFinal', names='DenumireGest',
                           title='Proporții Stocuri')
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                showlegend=False,
                title_font_size=16
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Analiza ABC a stocurilor
        st.markdown("### 📊 Analiza ABC Stocuri")
        
        # Calculare ABC
        produse_abc = balanta_df.groupby('Denumire')['ValoareStocFinal'].sum().reset_index()
        produse_abc = produse_abc.sort_values('ValoareStocFinal', ascending=False)
        produse_abc['Cumulative'] = produse_abc['ValoareStocFinal'].cumsum()
        produse_abc['Percentage'] = produse_abc['Cumulative'] / produse_abc['ValoareStocFinal'].sum() * 100
        
        produse_abc['Category'] = pd.cut(produse_abc['Percentage'], 
                                        bins=[0, 80, 95, 100], 
                                        labels=['A', 'B', 'C'])
        
        # Vizualizare ABC
        fig_abc = go.Figure()
        
        colors = {'A': '#4CAF50', 'B': '#FF9800', 'C': '#f44336'}
        
        for category in ['A', 'B', 'C']:
            data = produse_abc[produse_abc['Category'] == category]
            fig_abc.add_trace(go.Bar(
                x=range(len(data)),
                y=data['ValoareStocFinal'],
                name=f'Categoria {category}',
                marker_color=colors[category]
            ))
        
        fig_abc.update_layout(
            title='Analiza ABC - Distribuția Valorii Stocurilor',
            barmode='stack',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            xaxis=dict(title='Produse (sortate după valoare)', gridcolor='#2d3339'),
            yaxis=dict(title='Valoare Stoc (RON)', gridcolor='#2d3339')
        )
        
        st.plotly_chart(fig_abc, use_container_width=True)
        
        # Statistici ABC
        col1, col2, col3 = st.columns(3)
        
        for col, cat in zip([col1, col2, col3], ['A', 'B', 'C']):
            cat_data = produse_abc[produse_abc['Category'] == cat]
            with col:
                color = colors[cat]
                st.markdown(f"""
                <div style='background-color: {color}20; border-left: 4px solid {color}; padding: 15px; border-radius: 8px;'>
                    <h4 style='color: {color}; margin: 0;'>Categoria {cat}</h4>
                    <p style='color: #888; margin: 5px 0;'>{len(cat_data)} produse ({len(cat_data)/len(produse_abc)*100:.1f}%)</p>
                    <p style='color: #fff; margin: 0; font-size: 18px; font-weight: bold;'>
                        {cat_data['ValoareStocFinal'].sum()/1000000:.1f}M RON
                    </p>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Analiza Stocurilor pe Perioadă")
        
        # Încărcare date perioadă
        perioada_df = load_balanta_perioada()
        
        # Analiza vechimii stocurilor
        st.markdown("#### 🕐 Analiza Vechimii Stocurilor")
        
        # Categorii vechime
        perioada_df['Categorie Vechime'] = pd.cut(perioada_df['ZileVechime'], 
                                                  bins=[0, 30, 60, 90, 180, 365, float('inf')],
                                                  labels=['< 30 zile', '30-60 zile', '60-90 zile', 
                                                         '90-180 zile', '180-365 zile', '> 365 zile'])
        
        vechime_stats = perioada_df.groupby('Categorie Vechime').agg({
            'Valoare intrare': 'sum',
            'Stoc final': 'sum'
        }).reset_index()
        
        # Grafic vechime
        fig_vechime = go.Figure()
        
        fig_vechime.add_trace(go.Bar(
            x=vechime_stats['Categorie Vechime'],
            y=vechime_stats['Valoare intrare'],
            name='Valoare Stoc',
            marker_color='#2196F3'
        ))
        
        fig_vechime.add_trace(go.Scatter(
            x=vechime_stats['Categorie Vechime'],
            y=vechime_stats['Stoc final'],
            name='Cantitate',
            yaxis='y2',
            line=dict(color='#FF9800', width=3)
        ))
        
        fig_vechime.update_layout(
            title='Distribuția Stocurilor după Vechime',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            yaxis=dict(title='Valoare (RON)', gridcolor='#2d3339'),
            yaxis2=dict(title='Cantitate (buc)', overlaying='y', side='right', gridcolor='#2d3339'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_vechime, use_container_width=True)
        
        # Alertă stocuri vechi
        old_stock = perioada_df[perioada_df['ZileVechime'] > 180]
        if len(old_stock) > 0:
            old_value = old_stock['Valoare intrare'].sum()
            st.warning(f"""
            ⚠️ **Atenție Stocuri Învechite**
            
            Există **{len(old_stock)} produse** cu vechime peste 180 zile, reprezentând **{old_value/1000000:.1f}M RON**.
            Acestea necesită acțiuni urgente de lichidare.
            """)
        
        # Top produse cu rotație lentă
        st.markdown("#### 🐌 Top Produse cu Rotație Lentă")
        
        slow_movers = perioada_df.nlargest(10, 'ZileVechime')[['Denumire', 'Stoc final', 'Valoare intrare', 'ZileVechime']]
        
        # Stilizare tabel
        st.dataframe(
            slow_movers.style.format({
                'Valoare intrare': '{:,.0f} RON',
                'Stoc final': '{:,.0f} buc',
                'ZileVechime': '{:.0f} zile'
            }).background_gradient(subset=['ZileVechime'], cmap='Reds'),
            use_container_width=True
        )

# ===== CUMPARARI INTRARI =====
elif category == "Cumparari Intrari":
    st.markdown("## 🛒 Cumpărări Intrări")
    
    # Tabs pentru subcategorii
    tab1, tab2, tab3 = st.tabs(["📋 Cumpărări pe Dată", "📊 Cumpărări în Stoc", "📈 Analiza Furnizori"])
    
    with tab1:
        st.markdown("### 📋 Cumpărări Intrări Grupări pe Dată")
        
        # Încărcare date
        cipd_df = load_cumparari_cipd()
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        total_cantitate = cipd_df['Cantitate'].sum()
        total_valoare = cipd_df['Valoare'].sum()
        numar_produse = len(cipd_df)
        furnizori_unici = cipd_df['Furnizor'].nunique()
        
        with col1:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Cantitate Totală</h4>
                <h2 style='color: #4CAF50; margin: 5px 0;'>{total_cantitate:,.0f} buc</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Unități achiziționate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Valoare Achiziții</h4>
                <h2 style='color: #2196F3; margin: 5px 0;'>{total_valoare/1000000:.1f}M RON</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Total investit</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Produse</h4>
                <h2 style='color: #FF9800; margin: 5px 0;'>{numar_produse:,}</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>SKU achiziționate</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='info-box'>
                <h4 style='color: #888; margin: 0;'>Furnizori</h4>
                <h2 style='color: #9C27B0; margin: 5px 0;'>{furnizori_unici}</h2>
                <p style='color: #888; margin: 0; font-size: 14px;'>Parteneri activi</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top furnizori
        top_suppliers = cipd_df.groupby('Furnizor')['Valoare'].sum().nlargest(10).reset_index()
        
        fig_suppliers = px.bar(top_suppliers, x='Valoare', y='Furnizor', orientation='h',
                              title='Top 10 Furnizori după Valoare',
                              labels={'Valoare': 'Valoare Totală (RON)', 'Furnizor': 'Furnizor'},
                              color='Valoare', color_continuous_scale='Viridis')
        
        fig_suppliers.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=20,
            showlegend=False,
            xaxis=dict(gridcolor='#2d3339'),
            yaxis=dict(gridcolor='#2d3339', autorange="reversed")
        )
        
        st.plotly_chart(fig_suppliers, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Cumpărări Intrări în Stoc")
        
        # Încărcare date
        ciis_df = load_cumparari_ciis()
        
        # Selecții interactive cu preview valori
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 Analiză pe Gestiune")
            gestiune_selectata = st.selectbox(
                "Selectează gestiunea:",
                options=["Toate"] + list(ciis_df['Gestiune'].unique()),
                key="gest_ciis"
            )
            
            if gestiune_selectata != "Toate":
                gest_data = ciis_df[ciis_df['Gestiune'] == gestiune_selectata]
                valoare_gest = gest_data['Valoare'].sum()
                cantitate_gest = gest_data['Cantitate'].sum()
                
                st.success(f"""
                💰 **Gestiune: {gestiune_selectata}**
                - Valoare: **{valoare_gest:,.0f} RON**
                - Cantitate: **{cantitate_gest:,.0f} buc**
                - Produse: **{len(gest_data)} SKU**
                """)
        
        with col2:
            st.markdown("#### 📂 Analiză pe Grupă")
            grupa_selectata = st.selectbox(
                "Selectează grupa:",
                options=["Toate"] + list(ciis_df['Denumire grupa'].unique()),
                key="grupa_ciis"
            )
            
            if grupa_selectata != "Toate":
                grupa_data = ciis_df[ciis_df['Denumire grupa'] == grupa_selectata]
                valoare_grupa = grupa_data['Valoare'].sum()
                cantitate_grupa = grupa_data['Cantitate'].sum()
                
                st.info(f"""
                📦 **Grupă: {grupa_selectata}**
                - Valoare: **{valoare_grupa:,.0f} RON**
                - Cantitate: **{cantitate_grupa:,.0f} buc**
                - Furnizori: **{grupa_data['Furnizor'].nunique()}**
                """)
        
        # Aplicare filtre
        filtered_ciis = ciis_df.copy()
        if gestiune_selectata != "Toate":
            filtered_ciis = filtered_ciis[filtered_ciis['Gestiune'] == gestiune_selectata]
        if grupa_selectata != "Toate":
            filtered_ciis = filtered_ciis[filtered_ciis['Denumire grupa'] == grupa_selectata]
        
        # Vizualizare date filtrate
        if len(filtered_ciis) > 0:
            # Grafic distribuție pe grupe
            group_dist = filtered_ciis.groupby('Denumire grupa')['Valoare'].sum().reset_index()
            
            fig_groups = px.treemap(group_dist, path=['Denumire grupa'], values='Valoare',
                                  title='Distribuția Achizițiilor pe Grupe',
                                  color='Valoare', color_continuous_scale='Blues')
            
            fig_groups.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                title_font_size=20
            )
            
            st.plotly_chart(fig_groups, use_container_width=True)
    
    with tab3:
        st.markdown("### 📈 Analiza Detaliată Furnizori")
        
        # Combinare date pentru analiză completă
        all_purchases = pd.concat([cipd_df, ciis_df], ignore_index=True)
        
        # Analiza performanței furnizorilor
        supplier_analysis = all_purchases.groupby('Furnizor').agg({
            'Valoare': 'sum',
            'Cantitate': 'sum',
            'Denumire': 'nunique',
            'Pret': 'mean'
        }).reset_index()
        
        supplier_analysis.columns = ['Furnizor', 'Valoare Totală', 'Cantitate Totală', 'Produse Unice', 'Preț Mediu']
        supplier_analysis = supplier_analysis.sort_values('Valoare Totală', ascending=False)
        
        # Scatter plot pentru analiza furnizorilor
        fig_scatter = px.scatter(supplier_analysis.head(20), 
                               x='Cantitate Totală', 
                               y='Valoare Totală',
                               size='Produse Unice',
                               color='Preț Mediu',
                               hover_data=['Furnizor'],
                               title='Analiza Furnizorilor: Volum vs Valoare',
                               labels={'Cantitate Totală': 'Volum Total (buc)',
                                      'Valoare Totală': 'Valoare Totală (RON)',
                                      'Produse Unice': 'Nr. Produse',
                                      'Preț Mediu': 'Preț Mediu'},
                               color_continuous_scale='Viridis')
        
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#ffffff',
            title_font_size=20,
            xaxis=dict(gridcolor='#2d3339'),
            yaxis=dict(gridcolor='#2d3339')
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Top 5 furnizori strategici
        st.markdown("#### 🏆 Furnizori Strategici")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        for i, (col, row) in enumerate(zip([col1, col2, col3, col4, col5], supplier_analysis.head(5).iterrows())):
            with col:
                supplier = row[1]
                rank_color = ['#FFD700', '#C0C0C0', '#CD7F32', '#4CAF50', '#2196F3'][i]
                st.markdown(f"""
                <div style='background-color: {rank_color}20; border-radius: 10px; padding: 15px; text-align: center; border: 2px solid {rank_color};'>
                    <h4 style='color: {rank_color}; margin: 0;'>#{i+1}</h4>
                    <p style='color: #fff; margin: 5px 0; font-weight: bold;'>{supplier['Furnizor']}</p>
                    <p style='color: #888; margin: 0; font-size: 14px;'>{supplier['Valoare Totală']/1000000:.1f}M RON</p>
                    <p style='color: #888; margin: 0; font-size: 12px;'>{supplier['Produse Unice']} produse</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>© 2025 BRENADO Analytics | Business Intelligence Dashboard | Powered by Streamlit</p>
</div>
""", unsafe_allow_html=True)
