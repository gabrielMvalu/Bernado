"""
Pagina Vânzări pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.data_loaders import load_vanzari

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
            df = pd.read_excel("data/ytd.xlsx")
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'])
            return df
        except Exception as e:
            st.error(f"Nu s-au putut încărca datele YTD: {e}")
            # Date demo pentru YTD - extindem pentru a include și anul trecut
            dates_current = pd.date_range(start='2024-06-01', end='2024-07-26', freq='D')
            dates_previous = pd.date_range(start='2023-06-01', end='2023-07-26', freq='D')
            
            demo_data = []
            # Date pentru 2024
            for i, date in enumerate(dates_current):
                demo_data.append({'Data': date, 'Valoare': 1000 + i*50})
            # Date pentru 2023
            for i, date in enumerate(dates_previous):
                demo_data.append({'Data': date, 'Valoare': 800 + i*40})  # Valori ușor mai mici pentru 2023
                
            return pd.DataFrame(demo_data)
    
    ytd_df = load_ytd_data()
    
    if not ytd_df.empty and 'Data' in ytd_df.columns and 'Valoare' in ytd_df.columns:
        # Grupare vânzări pe zi și sumare
        daily_sales_ytd = ytd_df.groupby(ytd_df['Data'].dt.date)['Valoare'].sum().reset_index()
        daily_sales_ytd.columns = ['Data', 'Valoare']
        daily_sales_ytd['Data'] = pd.to_datetime(daily_sales_ytd['Data'])
        
        if not daily_sales_ytd.empty:
            # Separăm datele pe ani pentru comparație
            current_year = datetime.now().year  # 2025
            current_month = datetime.now().month
            
            # Verificăm ce ani avem disponibili în date
            available_years = sorted(daily_sales_ytd['Data'].dt.year.unique())
            
            # Logica de comparație adaptată la datele disponibile
            if len(available_years) >= 2:
                # Avem cel puțin 2 ani de date pentru comparație
                latest_year = max(available_years)
                previous_year = max([year for year in available_years if year < latest_year])
                
                # Datele pentru cel mai recent an
                current_year_data = daily_sales_ytd[daily_sales_ytd['Data'].dt.year == latest_year]
                
                # Datele pentru anul anterior disponibil
                previous_year_data = daily_sales_ytd[daily_sales_ytd['Data'].dt.year == previous_year]
                
                # Widget pentru selectarea tipului de grafic
                comparison_label = f"📊 Afișează comparația {latest_year} vs {previous_year} (pentru luna curentă)"
                show_comparison = st.checkbox(comparison_label, value=False)
                
                if show_comparison:
                    # Filtrăm pentru luna curentă
                    current_month_data = current_year_data[
                        current_year_data['Data'].dt.month == current_month
                    ]
                    previous_month_data = previous_year_data[
                        previous_year_data['Data'].dt.month == current_month
                    ]
                    
                    # Verificăm dacă avem date pentru ambele perioade
                    if current_month_data.empty and previous_month_data.empty:
                        st.warning(f"Nu există date pentru luna {current_month} în niciunul din anii {latest_year} sau {previous_year}")
                        show_comparison = False
                    elif current_month_data.empty:
                        st.warning(f"Nu există date pentru luna {current_month}/{latest_year}")
                        show_comparison = False
                    elif previous_month_data.empty:
                        st.warning(f"Nu există date pentru luna {current_month}/{previous_year}")
                        show_comparison = False
                
                if show_comparison and not current_month_data.empty and not previous_month_data.empty:
                    # Pentru afișarea comparativă, ajustăm datele anului anterior
                    previous_month_adjusted = previous_month_data.copy()
                    # Ajustăm anul pentru comparație vizuală side-by-side
                    previous_month_adjusted['Data_Adjusted'] = previous_month_adjusted['Data'].apply(
                        lambda x: x.replace(year=latest_year)
                    )
                    
                    # Creăm graficul cu comparație
                    fig = px.line(title=f'📈 Comparație Vânzări - {current_month}/{latest_year} vs {current_month}/{previous_year}')
                    
                    # Adăugăm linia pentru anul curent
                    fig.add_scatter(
                        x=current_month_data['Data'],
                        y=current_month_data['Valoare'],
                        mode='lines+markers',
                        name=f'{latest_year} (Anul Curent)',
                        line=dict(color='#1f77b4', width=3),
                        marker=dict(size=6)
                    )
                    
                    # Adăugăm linia pentru anul anterior (cu styling diferit)
                    fig.add_scatter(
                        x=previous_month_adjusted['Data_Adjusted'],
                        y=previous_month_adjusted['Valoare'],
                        mode='lines+markers',
                        name=f'{previous_year} (Anul Anterior)',
                        line=dict(color='#ff7f0e', width=2, dash='dash'),
                        marker=dict(size=4),
                        opacity=0.7
                    )
                    
                    # Configurare layout pentru comparație
                    fig.update_layout(
                        height=600,
                        xaxis_title="Data",
                        yaxis_title="Valoare Vânzări (RON)",
                        hovermode='x unified',
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.01
                        )
                    )
                    
                    # Formatare hover pentru comparație
                    fig.update_traces(
                        hovertemplate='<b>%{fullData.name}</b><br>%{x}<br>Valoare: %{y:,.0f} RON<extra></extra>'
                    )
                    
                else:
                    show_comparison = False
            else:
                # Nu avem suficiente date pentru comparație
                current_year_data = daily_sales_ytd
                show_comparison = False
                st.info("ℹ️ Comparația year-over-year nu este disponibilă (necesită date din cel puțin 2 ani)")
            
            if not show_comparison:
                # Graficul standard cu range slider și selectori
                fig = px.line(
                    daily_sales_ytd, 
                    x='Data', 
                    y='Valoare',
                    title='📈 Evoluția Vânzărilor Totale - Serie Temporală cu Selectori',
                    markers=True
                )
                
                # Configurare range slider și selectori
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
                
                # Styling pentru grafic standard
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    xaxis_title="Data",
                    yaxis_title="Valoare Vânzări (RON)",
                    hovermode='x unified'
                )
                
                # Formatare hover standard
                fig.update_traces(
                    hovertemplate='<b>%{x}</b><br>Valoare: %{y:,.0f} RON<extra></extra>'
                )
            
            # Afișare grafic
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistici rapide pentru perioada afișată
            if show_comparison and len(available_years) >= 2:
                # Statistici comparative
                latest_year = max(available_years)
                previous_year = max([year for year in available_years if year < latest_year])
                
                current_month_data = daily_sales_ytd[
                    (daily_sales_ytd['Data'].dt.year == latest_year) & 
                    (daily_sales_ytd['Data'].dt.month == current_month)
                ]
                previous_month_data = daily_sales_ytd[
                    (daily_sales_ytd['Data'].dt.year == previous_year) & 
                    (daily_sales_ytd['Data'].dt.month == current_month)
                ]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    current_total = current_month_data['Valoare'].sum() if not current_month_data.empty else 0
                    previous_total = previous_month_data['Valoare'].sum() if not previous_month_data.empty else 0
                    difference = current_total - previous_total
                    st.metric(
                        f"📊 Total {latest_year}", 
                        f"{current_total:,.0f} RON",
                        delta=f"{difference:,.0f} RON vs {previous_year}"
                    )
                
                with col2:
                    st.metric(f"📈 Total {previous_year}", f"{previous_total:,.0f} RON")
                
                with col3:
                    if previous_total > 0:
                        growth_rate = ((current_total - previous_total) / previous_total) * 100
                        st.metric("📈 Creștere YoY", f"{growth_rate:+.1f}%")
                    else:
                        st.metric("📈 Creștere YoY", "N/A")
            else:
                # Statistici standard
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_ytd = daily_sales_ytd['Valoare'].sum()
                    st.metric("📊 Total Perioada", f"{total_ytd:,.0f} RON")
                
                with col2:
                    avg_daily = daily_sales_ytd['Valoare'].mean()
                    st.metric("📈 Media Zilnică", f"{avg_daily:,.0f} RON")
                
                with col3:
                    if not daily_sales_ytd.empty:
                        max_day = daily_sales_ytd.loc[daily_sales_ytd['Valoare'].idxmax()]
                        st.metric("🏆 Cea Mai Bună Zi", f"{max_day['Valoare']:,.0f} RON")
            
            # Informații despre perioada datelor
            min_date = daily_sales_ytd['Data'].min().strftime('%d/%m/%Y')
            max_date = daily_sales_ytd['Data'].max().strftime('%d/%m/%Y')
            total_days = len(daily_sales_ytd)
            years_available = ", ".join(map(str, available_years))
            
            st.info(f"📅 **Perioada datelor:** {min_date} - {max_date} ({total_days} zile) | **Ani disponibili:** {years_available}")
            
        else:
            st.warning("Nu există date pentru a genera graficul temporal")
    else:
        st.error("Datele YTD nu conțin coloanele necesare (Data, Valoare) sau fișierul nu există")
