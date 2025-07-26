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
    
    # Încărcare date YTD
    @st.cache_data
    def load_ytd_data():
        """Încarcă datele YTD din Excel"""
        try:
            df = pd.read_excel("data/YTD.xlsx")
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'])
            return df
        except Exception as e:
            st.error(f"Nu s-au putut încărca datele YTD: {e}")
            # Date demo pentru testare
            dates_2024 = pd.date_range(start='2024-06-01', end='2024-12-31', freq='D')
            dates_2025 = pd.date_range(start='2025-01-01', end='2025-07-26', freq='D')
            
            demo_data = []
            for i, date in enumerate(dates_2024):
                demo_data.append({'Data': date, 'Valoare': 800 + i*30 + np.random.randint(-100, 100)})
            for i, date in enumerate(dates_2025):
                demo_data.append({'Data': date, 'Valoare': 1000 + i*40 + np.random.randint(-100, 100)})
                
            return pd.DataFrame(demo_data)
    
    ytd_df = load_ytd_data()
    
    if not ytd_df.empty and 'Data' in ytd_df.columns and 'Valoare' in ytd_df.columns:
        # Grupare vânzări pe zi
        daily_sales_ytd = ytd_df.groupby(ytd_df['Data'].dt.date)['Valoare'].sum().reset_index()
        daily_sales_ytd.columns = ['Data', 'Valoare']
        daily_sales_ytd['Data'] = pd.to_datetime(daily_sales_ytd['Data'])
        
        # Obținem luna și anul curent
        today = datetime.now()
        current_month = today.month
        current_year = today.year
        previous_year = current_year - 1
        
        # Verificăm dacă avem date pentru anul trecut în aceeași lună
        current_month_data = daily_sales_ytd[
            (daily_sales_ytd['Data'].dt.year == current_year) & 
            (daily_sales_ytd['Data'].dt.month == current_month)
        ]
        
        previous_month_data = daily_sales_ytd[
            (daily_sales_ytd['Data'].dt.year == previous_year) & 
            (daily_sales_ytd['Data'].dt.month == current_month)
        ]
        
        # CHECKBOX pentru comparația cu aceeași lună din anul trecut
        has_previous_month_data = len(previous_month_data) > 0
        
        if has_previous_month_data:
            show_monthly_comparison = st.checkbox(
                f"📊 Compară {calendar.month_name[current_month]} {current_year} cu {calendar.month_name[current_month]} {previous_year}", 
                value=False
            )
        else:
            show_monthly_comparison = False
            st.info(f"Comparația va fi disponibilă când vor exista date pentru {calendar.month_name[current_month]} {previous_year}")
        
        # PERIOD SELECTOR
        col1, col2 = st.columns([3, 1])
        with col2:
            period_options = ["Toate", "YTD", "3 Luni", "1 Lună"]
            if show_monthly_comparison:
                period_options.append("Doar comparația lunară")
            selected_period = st.selectbox("📅 Perioada:", period_options, index=0)
        
        # Filtrarea datelor bazat pe perioada selectată
        if selected_period == "1 Lună":
            start_date = today - timedelta(days=30)
            filtered_data = daily_sales_ytd[daily_sales_ytd['Data'] >= start_date]
        elif selected_period == "3 Luni":
            start_date = today - timedelta(days=90)
            filtered_data = daily_sales_ytd[daily_sales_ytd['Data'] >= start_date]
        elif selected_period == "YTD":
            start_date = datetime(current_year, 1, 1)
            filtered_data = daily_sales_ytd[daily_sales_ytd['Data'] >= start_date]
        elif selected_period == "Doar comparația lunară" and show_monthly_comparison:
            # Afișăm doar luna curentă și luna din anul trecut
            filtered_data = pd.concat([current_month_data, previous_month_data])
        else:  # "Toate"
            filtered_data = daily_sales_ytd
        
        # CREAREA GRAFICULUI
        if show_monthly_comparison and has_previous_month_data and selected_period != "Doar comparația lunară":
            # Grafic cu comparația lunară inclusă în perioada selectată
            fig = go.Figure()
            
            # Adăugăm toate datele filtrate ca linie principală
            fig.add_trace(go.Scatter(
                x=filtered_data['Data'],
                y=filtered_data['Valoare'],
                mode='lines+markers',
                name=f'Vânzări {current_year}',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=4)
            ))
            
            # Adăugăm luna din anul trecut (ajustată pentru suprapunere)
            if len(previous_month_data) > 0:
                previous_adjusted = previous_month_data.copy()
                previous_adjusted['Data_Adjusted'] = previous_adjusted['Data'].apply(
                    lambda x: x.replace(year=current_year)
                )
                
                fig.add_trace(go.Scatter(
                    x=previous_adjusted['Data_Adjusted'],
                    y=previous_adjusted['Valoare'],
                    mode='lines+markers',
                    name=f'{calendar.month_name[current_month]} {previous_year}',
                    line=dict(color='#ff7f0e', width=3, dash='dash'),
                    marker=dict(size=5),
                    opacity=0.8
                ))
            
            title = f'📈 Vânzări - {selected_period} (cu comparația {calendar.month_name[current_month]})'
            
        elif show_monthly_comparison and selected_period == "Doar comparația lunară":
            # Grafic doar cu comparația lunară
            fig = go.Figure()
            
            # Luna curentă
            fig.add_trace(go.Scatter(
                x=current_month_data['Data'],
                y=current_month_data['Valoare'],
                mode='lines+markers',
                name=f'{calendar.month_name[current_month]} {current_year}',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=6)
            ))
            
            # Luna din anul trecut (ajustată)
            previous_adjusted = previous_month_data.copy()
            previous_adjusted['Data_Adjusted'] = previous_adjusted['Data'].apply(
                lambda x: x.replace(year=current_year)
            )
            
            fig.add_trace(go.Scatter(
                x=previous_adjusted['Data_Adjusted'],
                y=previous_adjusted['Valoare'],
                mode='lines+markers',
                name=f'{calendar.month_name[current_month]} {previous_year}',
                line=dict(color='#ff7f0e', width=3, dash='dash'),
                marker=dict(size=6),
                opacity=0.8
            ))
            
            title = f'📈 Comparație: {calendar.month_name[current_month]} {current_year} vs {calendar.month_name[current_month]} {previous_year}'
            
        else:
            # Grafic normal fără comparație
            fig = px.line(
                filtered_data, 
                x='Data', 
                y='Valoare',
                title=f'📈 Evoluția Vânzărilor - {selected_period}',
                markers=True
            )
            fig.update_traces(line=dict(width=2), marker=dict(size=4))
        
        # Layout grafic
        fig.update_layout(
            height=600,
            xaxis_title="Data",
            yaxis_title="Valoare Vânzări (RON)",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Range selector doar pentru graficele care nu sunt "Doar comparația lunară"
        if selected_period != "Doar comparația lunară":
            fig.update_xaxes(
                rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1 Lună", step="month", stepmode="backward"),
                        dict(count=3, label="3 Luni", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(step="all", label="Toate")
                    ])
                )
            )
        
        # Afișare grafic
        st.plotly_chart(fig, use_container_width=True)
        
        # STATISTICI
        st.markdown("---")
        st.subheader("📈 Statistici")
        
        if show_monthly_comparison and len(previous_month_data) > 0:
            # Statistici cu comparație
            col1, col2, col3, col4 = st.columns(4)
            
            current_total = current_month_data['Valoare'].sum() if len(current_month_data) > 0 else 0
            previous_total = previous_month_data['Valoare'].sum()
            
            with col1:
                st.metric(
                    f"💰 Total {calendar.month_name[current_month]} {current_year}", 
                    f"{current_total:,.0f} RON",
                    delta=f"{current_total - previous_total:,.0f} RON" if current_total > 0 else None
                )
            
            with col2:
                if len(current_month_data) > 0:
                    current_avg = current_month_data['Valoare'].mean()
                    previous_avg = previous_month_data['Valoare'].mean()
                    st.metric(
                        "📊 Media zilnică", 
                        f"{current_avg:,.0f} RON",
                        delta=f"{current_avg - previous_avg:,.0f} RON"
                    )
                else:
                    st.metric("📊 Media zilnică", "0 RON")
            
            with col3:
                if len(current_month_data) > 0:
                    best_day_current = current_month_data.loc[current_month_data['Valoare'].idxmax()]
                    st.metric("🏆 Cea mai bună zi (luna curentă)", f"{best_day_current['Valoare']:,.0f} RON")
                else:
                    st.metric("🏆 Cea mai bună zi", "0 RON")
            
            with col4:
                best_day_previous = previous_month_data.loc[previous_month_data['Valoare'].idxmax()]
                st.metric("🏆 Cea mai bună zi (anul trecut)", f"{best_day_previous['Valoare']:,.0f} RON")
                
        else:
            # Statistici normale
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total = filtered_data['Valoare'].sum()
                st.metric("💰 Total", f"{total:,.0f} RON")
            
            with col2:
                avg = filtered_data['Valoare'].mean()
                st.metric("📊 Media zilnică", f"{avg:,.0f} RON")
            
            with col3:
                if len(filtered_data) > 0:
                    best_day = filtered_data.loc[filtered_data['Valoare'].idxmax()]
                    st.metric("🏆 Cea mai bună zi", f"{best_day['Valoare']:,.0f} RON")
                else:
                    st.metric("🏆 Cea mai bună zi", "0 RON")
    
    else:
        st.error("❌ Fișierul YTD.xlsx nu există sau nu conține coloanele Data și Valoare")
        st.info("💡 Verifică că fișierul se află în folderul data/ și conține coloanele corecte")
