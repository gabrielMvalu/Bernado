"""
Pagina Vânzări pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_loaders import load_vanzari
import calendar
import plotly.graph_objects as go

# Titlu pagină
st.markdown("### 📊 Vânzări")

# Încărcare date
vanzari_df = load_vanzari()

# Calculare metrici principali
total_vanzari = vanzari_df['Valoare'].sum() if 'Valoare' in vanzari_df.columns else 0
clienti_unici = vanzari_df['Client'].nunique() if 'Client' in vanzari_df.columns else 0
total_records = len(vanzari_df)
gestiuni = vanzari_df['DenumireGestiune'].nunique() if 'DenumireGestiune' in vanzari_df.columns else 0

# Metrici principale
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Vânzări Totale", f"{total_vanzari:,.0f} RON")
with col2:
    st.metric("👥 Clienți Unici", f"{clienti_unici}")
with col3:
    st.metric("📋 Tranzacții", f"{total_records:,}")
with col4:
    st.metric("🏢 Gestiuni", f"{gestiuni}")

st.markdown("---")

# Grafice
st.subheader("📈 Analize Vizuale")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Vânzări pe Zi**")
    if 'Data' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
        daily_sales = vanzari_df.groupby(vanzari_df['Data'].dt.date)['Valoare'].sum().reset_index()
        daily_sales.columns = ['Data', 'Valoare']
        
        if not daily_sales.empty:
            fig = px.line(
                daily_sales, 
                x='Data', 
                y='Valoare',
                title="Evoluția Vânzărilor",
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există date pentru perioada selectată")
    else:
        st.info("Date insuficiente pentru grafic")

with col2:
    st.markdown("**Top 10 Clienți**")
    if 'Client' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
        top_clienti = vanzari_df.groupby('Client')['Valoare'].sum().nlargest(10).reset_index()
        
        if not top_clienti.empty:
            fig = px.bar(
                top_clienti, 
                x='Valoare', 
                y='Client',
                orientation='h',
                title="Clienți după Valoare",
                color='Valoare',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există date pentru grafic")
    else:
        st.info("Date insuficiente pentru grafic")

st.markdown("---")

# ===== TABS PENTRU DATE DETALIATE ȘI ANALIZE =====
tab1, tab2 = st.tabs(["📋 Date Detaliate", "📊 Analize Avansate"])

# ===== TAB 1: DATE DETALIATE (CODUL ACTUAL) =====
with tab1:
    # Date detaliate cu filtre
    st.subheader("📋 Date Detaliate")

    # Radio buttons pentru tipul de afișare
    view_type = st.radio(
        "Selectează tipul de afișare:",
        options=["Standard", "Zi și Clienți", "Top Produse"],
        horizontal=True,
        key="view_type_radio"
    )

    # Filtre - doar pentru Standard
    if view_type == "Standard":
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if 'DenumireGestiune' in vanzari_df.columns:
                gestiuni_list = ['Toate'] + list(vanzari_df['DenumireGestiune'].unique())
                selected_gestiune = st.selectbox("Gestiune:", gestiuni_list)

        with col2:
            if 'Agent' in vanzari_df.columns:
                agenti_list = ['Toți'] + list(vanzari_df['Agent'].unique())
                selected_agent = st.selectbox("Agent:", agenti_list)

        with col3:
            if 'Data' in vanzari_df.columns:
                vanzari_df['Data'] = pd.to_datetime(vanzari_df['Data'])
                min_date = vanzari_df['Data'].min().date()
                max_date = vanzari_df['Data'].max().date()
                today = datetime.now().date()
                
                if today > max_date:
                    default_date = max_date
                elif today < min_date:
                    default_date = min_date
                else:
                    default_date = today
                
                date_range = st.date_input(
                    "📅 Interval date:",
                    value=(default_date, default_date),
                    min_value=min_date,
                    max_value=max_date,
                    format="DD/MM/YYYY"
                )

        with col4:
            # Filtru produs
            if 'Denumire' in vanzari_df.columns:
                produs_filter = st.multiselect(
                    "Filtrează după produs:",
                    options=vanzari_df['Denumire'].unique(),
                    default=[],
                    key="produs_filter"
                )

        # Aplicare filtre pentru Standard
        filtered_df = vanzari_df.copy()

        # Filtru gestiune
        if 'DenumireGestiune' in vanzari_df.columns and selected_gestiune != 'Toate':
            filtered_df = filtered_df[filtered_df['DenumireGestiune'] == selected_gestiune]

        # Filtru agent
        if 'Agent' in vanzari_df.columns and selected_agent != 'Toți':
            filtered_df = filtered_df[filtered_df['Agent'] == selected_agent]

        # Filtru dată
        if 'Data' in vanzari_df.columns and date_range:
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df['Data'].dt.date >= start_date) & 
                    (filtered_df['Data'].dt.date <= end_date)
                ]
            else:
                selected_date_obj = date_range
                filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date_obj]

        # Filtru produs
        if 'Denumire' in vanzari_df.columns and produs_filter:
            filtered_df = filtered_df[filtered_df['Denumire'].isin(produs_filter)]

    else:
        # Pentru "Zi și Clienți" și "Top Produse" - doar filtru dată
        if 'Data' in vanzari_df.columns:
            vanzari_df['Data'] = pd.to_datetime(vanzari_df['Data'])
            min_date = vanzari_df['Data'].min().date()
            max_date = vanzari_df['Data'].max().date()
            today = datetime.now().date()
            
            if today > max_date:
                default_date = max_date
            elif today < min_date:
                default_date = min_date
            else:
                default_date = today
            
            date_range = st.date_input(
                "📅 Interval date:",
                value=(default_date, default_date),
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY",
                key=f"date_filter_{view_type}"
            )
        
        # Aplicare filtru dată pentru toate view-urile
        filtered_df = vanzari_df.copy()
        if 'Data' in vanzari_df.columns and date_range:
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                filtered_df = filtered_df[
                    (filtered_df['Data'].dt.date >= start_date) & 
                    (filtered_df['Data'].dt.date <= end_date)
                ]
            else:
                selected_date_obj = date_range
                filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date_obj]

    # Procesare date în funcție de tipul de view selectat
    if view_type == "Standard":
        # Afișare standard - toate coloanele
        display_df = filtered_df.copy()
        if 'Data' in display_df.columns:
            display_df = display_df.sort_values('Data', ascending=False)
        
    elif view_type == "Zi și Clienți":
        # Grupare pe Data și Client
        if all(col in filtered_df.columns for col in ['Data', 'Client', 'Valoare', 'Adaos']):
            display_df = filtered_df.groupby(['Data', 'Client']).agg({
                'Valoare': 'sum',
                'Adaos': 'sum'
            }).reset_index()
            display_df = display_df.sort_values('Data', ascending=False)
        else:
            st.warning("Coloanele necesare (Data, Client, Valoare, Adaos) nu sunt disponibile")
            display_df = pd.DataFrame()
            
    elif view_type == "Top Produse":
        # Afișare doar coloanele specificate
        required_columns = ['Denumire', 'Cantitate', 'Valoare', 'Adaos']
        available_columns = [col for col in required_columns if col in filtered_df.columns]
        
        if available_columns:
            display_df = filtered_df[available_columns].copy()
        else:
            st.warning("Coloanele necesare (Denumire, Cantitate, Valoare, Adaos) nu sunt disponibile")
            display_df = pd.DataFrame()

    # Afișare rezultate
    if not display_df.empty:
        # Configurare column_config în funcție de view type
        if view_type == "Standard" and 'Data' in display_df.columns:
            column_config = {
                "Data": st.column_config.DatetimeColumn(
                    "Data",
                    format="DD/MM/YYYY"
                )
            }
        elif view_type == "Zi și Clienți" and 'Data' in display_df.columns:
            column_config = {
                "Data": st.column_config.DatetimeColumn(
                    "Data",
                    format="DD/MM/YYYY"
                )
            }
        else:
            column_config = None
        
        # Afișare DataFrame
        st.dataframe(
            display_df, 
            use_container_width=True, 
            height=400,
            column_config=column_config
        )
        
        # Afișez statisticile
        st.markdown("#### 📊 Statistici")
        col1, col2 = st.columns(2)
        
        with col1:
            total_valoare = display_df['Valoare'].sum() if 'Valoare' in display_df.columns else 0
            st.metric("Total Valoare", f"{total_valoare:,.0f} RON")
        with col2:
            total_adaos = display_df['Adaos'].sum() if 'Adaos' in display_df.columns else 0
            st.metric("Total Adaos", f"{total_adaos:,.0f} RON")

    else:
        if view_type == "Standard":
            st.warning("Nu s-au găsit înregistrări cu filtrele selectate")
        else:
            st.warning("Nu sunt date disponibile pentru acest tip de afișare")



# ===== TAB 2: ANALIZE AVANSATE =====
with tab2:
    st.subheader("📊 Analize Avansate")
    
    import pandas as pd
    import streamlit as st
    import plotly.express as px
    import plotly.graph_objects as go
    from datetime import datetime

    # Încărcare date YTD
    @st.cache_data
    def load_ytd_data():
        try:
            df = pd.read_excel("data/YTD.xlsx")
            df['Data'] = pd.to_datetime(df['Data'])
            return df
        except Exception as e:
            st.warning(f"Fișierul nu a fost găsit sau are probleme. Se încarcă date demo: {e}")
            # Date demo
            dates_2024 = pd.date_range("2024-07-01", "2024-07-31")
            dates_2025 = pd.date_range("2025-07-01", "2025-07-26")
            data = pd.DataFrame({
                "Data": list(dates_2024) + list(dates_2025),
                "Valoare": [1000 + i*10 for i in range(len(dates_2024))] + [1200 + i*12 for i in range(len(dates_2025))]
            })
            return data

    df = load_ytd_data()
    
    if df.empty or 'Data' not in df.columns or 'Valoare' not in df.columns:
        st.error("Datele nu sunt valide sau lipsesc coloanele necesare.")
    else:
        df = df.sort_values("Data")
        df['An'] = df['Data'].dt.year
        df['Lună'] = df['Data'].dt.month

        # Perioade disponibile
        ani = df['An'].unique()
        azi = pd.Timestamp("today").normalize()
        luna_curenta = azi.month
        anul_curent = azi.year

        # Checkbox comparație
        show_comparison = st.checkbox("📊 Compară luna curentă cu anul trecut")

        # Filtrare lună curentă și, opțional, luna similară din anul trecut
        df_current = df[(df['An'] == anul_curent) & (df['Lună'] == luna_curenta)]
        df_previous = df[(df['An'] == anul_curent - 1) & (df['Lună'] == luna_curenta)]

        # Grafic
        fig = go.Figure()

        if show_comparison and not df_previous.empty:
            # Date ajustate pt. aliniere (doar ziua)
            df_previous['Data_Adjusted'] = df_previous['Data'].apply(lambda x: x.replace(year=anul_curent))
            fig.add_trace(go.Scatter(
                x=df_previous['Data_Adjusted'],
                y=df_previous['Valoare'],
                mode='lines+markers',
                name=f"{anul_curent - 1}",
                line=dict(dash='dash', color='orange'),
                opacity=0.6
            ))

        if not df_current.empty:
            fig.add_trace(go.Scatter(
                x=df_current['Data'],
                y=df_current['Valoare'],
                mode='lines+markers',
                name=f"{anul_curent}",
                line=dict(color='blue'),
            ))

        # Range Selector
        fig.update_layout(
            title="📈 Vânzări Zilnice",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1 Lună", step="month", stepmode="backward"),
                        dict(count=3, label="3 Luni", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(step="all", label="Toate")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            ),
            yaxis_title="Valoare Vânzări (RON)",
            hovermode="x unified",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistici (pe întreg setul de date, nu doar luna curentă)
        total = df['Valoare'].sum()
        medie = df['Valoare'].mean()
        best_row = df[df['Valoare'] == df['Valoare'].max()].iloc[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Vânzări", f"{total:,.0f} RON")
        with col2:
            st.metric("📉 Media Zilnică", f"{medie:,.0f} RON")
        with col3:
            st.metric("🏆 Cea mai bună zi", f"{best_row['Valoare']:,.0f} RON", best_row['Data'].strftime('%d %b %Y'))
