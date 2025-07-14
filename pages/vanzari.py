"""
Pagina Vânzări pentru aplicația Brenado For House
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_loaders import load_vanzari

# ===== FUNCȚII HELPER =====

def render_main_metrics(df):
    """Randează metricii principali"""
    if df.empty:
        st.warning("⚠️ Nu sunt date disponibile")
        return
    
    st.subheader("📊 Metrici Principali")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_vanzari = df['Valoare'].sum() if 'Valoare' in df.columns else 0
        st.metric("💰 Vânzări Totale", f"{total_vanzari:,.0f} RON")
    
    with col2:
        clienti_unici = df['Client'].nunique() if 'Client' in df.columns else 0
        st.metric("👥 Clienți Unici", f"{clienti_unici}")
    
    with col3:
        total_records = len(df)
        st.metric("📋 Tranzacții", f"{total_records:,}")
    
    with col4:
        gestiuni = df['DenumireGestiune'].nunique() if 'DenumireGestiune' in df.columns else 0
        st.metric("🏢 Gestiuni", f"{gestiuni}")

def render_charts(df):
    """Randează graficele de analiză"""
    if df.empty:
        return
    
    st.subheader("📈 Analize Vizuale")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vânzări pe Zi**")
        if 'Data' in df.columns and 'Valoare' in df.columns:
            daily_sales = df.groupby(df['Data'].dt.date)['Valoare'].sum().reset_index()
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
        if 'Client' in df.columns and 'Valoare' in df.columns:
            top_clienti = df.groupby('Client')['Valoare'].sum().nlargest(10).reset_index()
            
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

def apply_filters(df, gestiune_filter, agent_filter, date_range, search_produs):
    """Aplică toate filtrele pe DataFrame"""
    filtered_df = df.copy()
    
    # Filtru gestiune
    if 'DenumireGestiune' in df.columns and gestiune_filter != 'Toate':
        filtered_df = filtered_df[filtered_df['DenumireGestiune'] == gestiune_filter]
    
    # Filtru agent
    if 'Agent' in df.columns and agent_filter != 'Toți':
        filtered_df = filtered_df[filtered_df['Agent'] == agent_filter]
    
    # Filtru dată (interval)
    if 'Data' in df.columns and date_range:
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[
                (filtered_df['Data'].dt.date >= start_date) & 
                (filtered_df['Data'].dt.date <= end_date)
            ]
        else:
            selected_date_obj = date_range
            filtered_df = filtered_df[filtered_df['Data'].dt.date == selected_date_obj]
    
    # Filtru produs (fuzzy search)
    if 'Denumire' in df.columns and search_produs:
        filtered_df = filtered_df[
            filtered_df['Denumire'].str.contains(search_produs, case=False, na=False)
        ]
    
    return filtered_df

def render_filter_statistics(filtered_df):
    """Randează statisticile pentru datele filtrate"""
    if filtered_df.empty:
        return
    
    st.markdown("#### 📊 Statistici Date Filtrate")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_valoare = filtered_df['Valoare'].sum() if 'Valoare' in filtered_df.columns else 0
        st.metric("Total Valoare", f"{total_valoare:,.0f} RON")
    
    with col2:
        total_adaos = filtered_df['Adaos'].sum() if 'Adaos' in filtered_df.columns else 0
        st.metric("Total Adaos", f"{total_adaos:,.0f} RON")
    
    with col3:
        total_cantitate = filtered_df['Cantitate'].sum() if 'Cantitate' in filtered_df.columns else 0
        st.metric("Total Cantitate", f"{total_cantitate:,.0f}")
    
    with col4:
        nr_inregistrari = len(filtered_df)
        st.metric("Înregistrări", f"{nr_inregistrari:,}")

def render_data_tables(df):
    """Randează tabelele cu date și filtrele"""
    if df.empty:
        return
    
    st.subheader("📋 Date Detaliate")
    
    # Filtre - 4 coloane
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'DenumireGestiune' in df.columns:
            gestiuni = ['Toate'] + list(df['DenumireGestiune'].unique())
            selected_gestiune = st.selectbox("Gestiune:", gestiuni)
    
    with col2:
        if 'Agent' in df.columns:
            agenti = ['Toți'] + list(df['Agent'].unique())
            selected_agent = st.selectbox("Agent:", agenti)
    
    with col3:
        if 'Data' in df.columns:
            # Convertește la datetime dacă nu e deja
            df['Data'] = pd.to_datetime(df['Data'])
            
            # Obține min și max din date
            min_date = df['Data'].min().date()
            max_date = df['Data'].max().date()
            today = datetime.now().date()
            
            # Verifică dacă ziua curentă e în dataset, altfel folosește ultima dată
            if today > max_date:
                default_date = max_date
            elif today < min_date:
                default_date = min_date
            else:
                default_date = today
            
            # Range picker cu default pe ziua curentă (sau ultima disponibilă)
            date_range = st.date_input(
                "📅 Interval date:",
                value=(default_date, default_date),
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY",
                help="Selectează o zi sau trage pentru interval"
            )
    
    with col4:
        if 'Denumire' in df.columns:
            search_produs = st.text_input(
                "🔍 Caută produs:", 
                placeholder="Tastează oricare parte din nume...",
                help="Ex: 'cablu', 'samsung', '200', etc."
            )
    
    # Aplicare filtre
    filtered_df = apply_filters(df, selected_gestiune, selected_agent, date_range, search_produs)
    
    # Afișare numărul de rezultate găsite
    if not filtered_df.empty:
        st.info(f"🔍 Găsite: **{len(filtered_df):,}** înregistrări din {len(df):,} totale")
    else:
        st.warning("⚠️ Nu s-au găsit înregistrări cu filtrele selectate")
        return
    
    # Selectare coloane importante pentru afișare
    display_columns = [
        'Data', 'Client', 'Denumire', 'Cantitate', 'Valoare', 
        'Adaos', 'Agent', 'DenumireGestiune', 'Cod', 'UM'
    ]
    
    # Afișează doar coloanele disponibile
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    
    if available_columns:
        # Sortare după dată (cele mai recente primul)
        if 'Data' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('Data', ascending=False)
        
        st.dataframe(
            filtered_df[available_columns], 
            use_container_width=True,
            height=400
        )
        
        # Statistici pentru datele filtrate
        render_filter_statistics(filtered_df)
    else:
        st.warning("Nu există coloane disponibile pentru afișare")



# ===== FUNCȚIA PRINCIPALĂ =====

def main():
    """Funcția principală a paginii"""
    
    # Header
    st.title("📊 Vânzări")
    st.markdown("*Date din fișierul Excel VS.xlsx*")
    st.markdown("---")
    
    # Încărcare date
    with st.spinner("📡 Se încarcă datele din Excel..."):
        df = load_vanzari()
    
    # Sidebar
    render_sidebar(df)
    
    # Metrici principale
    render_main_metrics(df)
    
    st.markdown("---")
    
    # Grafice
    render_charts(df)
    
    st.markdown("---")
    
    # Tabele detaliate
    render_data_tables(df)
    
    # Footer
    st.markdown("---")
    st.markdown("*Dashboard generat automat din datele Excel • Brenado For House ERP*")


if __name__ == "__main__":
    main()
else:
    main()
