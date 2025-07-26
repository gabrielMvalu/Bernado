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

    # Filtre
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

    # Aplicare filtre
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

    # Afișare rezultate
    if not filtered_df.empty:
        # Sortare după dată
        if 'Data' in filtered_df.columns:
            filtered_df = filtered_df.sort_values('Data', ascending=False)
        
        # Afișare DataFrame complet
        st.dataframe(
            filtered_df, 
            use_container_width=True, 
            height=400,
            column_config={
                "Data": st.column_config.DatetimeColumn(
                    "Data",
                    format="DD/MM/YYYY"
                )
            }
        )
        
        # Afișez întotdeauna statisticile când sunt aplicate filtre
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
            st.metric("Înregistrări", f"{len(filtered_df):,}")

    else:
        st.warning("Nu s-au găsit înregistrări cu filtrele selectate")

# ===== TAB 2: ANALIZE AVANSATE =====
with tab2:
    st.subheader("📊 Analize Avansate")
    
    if vanzari_df.empty:
        st.warning("Nu sunt date disponibile pentru analize")
    else:
        # ===== SECȚIUNEA 1: PERFORMANȚA MAGAZINELOR =====
        st.markdown("### 🏪 Performanța Magazinelor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 1. Pie Chart - Distribuția vânzărilor pe gestiuni
            if 'DenumireGestiune' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
                gestiuni_valoare = vanzari_df.groupby('DenumireGestiune')['Valoare'].sum().reset_index()
                
                fig = px.pie(
                    gestiuni_valoare,
                    values='Valoare',
                    names='DenumireGestiune',
                    title="Distribuția Vânzărilor pe Gestiuni"
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 2. Bar Chart - Comparație gestiuni pe lună
            if all(col in vanzari_df.columns for col in ['DenumireGestiune', 'Data', 'Valoare']):
                vanzari_df_copy = vanzari_df.copy()
                vanzari_df_copy['Luna'] = vanzari_df_copy['Data'].dt.strftime('%Y-%m')
                gestiuni_luna = vanzari_df_copy.groupby(['DenumireGestiune', 'Luna'])['Valoare'].sum().reset_index()
                
                fig = px.bar(
                    gestiuni_luna,
                    x='Luna',
                    y='Valoare',
                    color='DenumireGestiune',
                    title="Comparație Gestiuni pe Lună",
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ===== SECȚIUNEA 2: ANALIZA PRODUSELOR =====
        st.markdown("### 🏷️ Analiza Produselor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 3. Treemap - Grupe de produse
            if 'Denumire grupa' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
                grupe_valoare = vanzari_df.groupby('Denumire grupa')['Valoare'].sum().reset_index()
                grupe_valoare = grupe_valoare.sort_values('Valoare', ascending=False)
                
                fig = px.treemap(
                    grupe_valoare,
                    values='Valoare',
                    names='Denumire grupa',
                    title="Distribuția Vânzărilor pe Grupe de Produse"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 4. Top 20 Produse
            if 'Denumire' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
                top_produse = vanzari_df.groupby('Denumire')['Valoare'].sum().nlargest(20).reset_index()
                
                fig = px.bar(
                    top_produse,
                    x='Valoare',
                    y='Denumire',
                    orientation='h',
                    title="Top 20 Produse după Vânzări"
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
        
        # 5. Scatter Plot - Preț vs Cantitate
        if all(col in vanzari_df.columns for col in ['Pret', 'Cantitate', 'Valoare']):
            # Creez o copie pentru a gestiona valorile negative
            scatter_df = vanzari_df.copy()
            # Adaug o coloană pentru a identifica retururile
            scatter_df['Tip_Tranzactie'] = scatter_df['Cantitate'].apply(lambda x: 'Retur' if x < 0 else 'Vânzare')
            # Folosesc valoarea absolută pentru size (plotly nu acceptă negative)
            scatter_df['Size_Abs'] = abs(scatter_df['Cantitate'])
            
            fig = px.scatter(
                scatter_df,
                x='Pret',
                y='Cantitate',
                size='Size_Abs',
                color='Tip_Tranzactie',
                title="Corelația Preț vs Cantitate (Vânzări vs Retururi)",
                hover_data=['Denumire'] if 'Denumire' in scatter_df.columns else None,
                color_discrete_map={'Vânzare': 'blue', 'Retur': 'red'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ===== SECȚIUNEA 3: PROFITABILITATE =====
        st.markdown("### 💰 Analiza Profitabilității")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 6. Bubble Chart - Marja de profit
            if all(col in vanzari_df.columns for col in ['Valoare', 'Adaos', 'Cantitate']):
                # Creez o copie pentru a gestiona valorile negative
                profit_df = vanzari_df.copy()
                # Identific tipul de tranzacție
                profit_df['Tip_Tranzactie'] = profit_df['Cantitate'].apply(lambda x: 'Retur' if x < 0 else 'Vânzare')
                # Folosesc valoarea absolută pentru size
                profit_df['Size_Abs'] = abs(profit_df['Cantitate'])
                
                fig = px.scatter(
                    profit_df,
                    x='Valoare',
                    y='Adaos',
                    size='Size_Abs',
                    color='Tip_Tranzactie',
                    title="Marja de Profit (Valoare vs Adaos) - Vânzări vs Retururi",
                    hover_data=['Denumire'] if 'Denumire' in profit_df.columns else None,
                    color_discrete_map={'Vânzare': 'green', 'Retur': 'red'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 7. Heatmap - Profitabilitate pe gestiune și grupă
            if all(col in vanzari_df.columns for col in ['DenumireGestiune', 'Denumire grupa', 'Adaos']):
                heatmap_data = vanzari_df.groupby(['DenumireGestiune', 'Denumire grupa'])['Adaos'].sum().reset_index()
                heatmap_pivot = heatmap_data.pivot(index='DenumireGestiune', columns='Denumire grupa', values='Adaos').fillna(0)
                
                fig = px.imshow(
                    heatmap_pivot,
                    title="Heatmap Profitabilitate (Gestiune vs Grupă)",
                    aspect='auto',
                    color_continuous_scale='RdYlBu_r'
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ===== SECȚIUNEA 4: AGENȚI ȘI CLIENȚI =====
        st.markdown("### 👥 Performanța Agenților și Clienților")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 8. Performanța agenților
            if 'Agent' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
                agenti_valoare = vanzari_df.groupby('Agent')['Valoare'].sum().nlargest(10).reset_index()
                
                fig = px.bar(
                    agenti_valoare,
                    x='Valoare',
                    y='Agent',
                    orientation='h',
                    title="Top 10 Agenți după Performanță"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # 9. Top 15 Clienți
            if 'Client' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
                top_clienti = vanzari_df.groupby('Client')['Valoare'].sum().nlargest(15).reset_index()
                
                fig = px.bar(
                    top_clienti,
                    x='Valoare',
                    y='Client',
                    orientation='h',
                    title="Top 15 Clienți după Valoare"
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # ===== SECȚIUNEA 6: ANALIZA RETURURILOR =====
        st.markdown("### 🔄 Analiza Retururilor")
        
        # Filtrez doar retururile (cantități negative)
        if 'Cantitate' in vanzari_df.columns:
            retururi_df = vanzari_df[vanzari_df['Cantitate'] < 0].copy()
            
            if not retururi_df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Metrici retururi
                    total_retururi_valoare = retururi_df['Valoare'].sum() if 'Valoare' in retururi_df.columns else 0
                    nr_retururi = len(retururi_df)
                    
                    st.metric("Valoare Totală Retururi", f"{abs(total_retururi_valoare):,.0f} RON")
                    st.metric("Număr Retururi", f"{nr_retururi:,}")
                    
                    # Top produse returnate
                    if 'Denumire' in retururi_df.columns:
                        top_retururi = retururi_df.groupby('Denumire')['Cantitate'].sum().nsmallest(10).reset_index()
                        top_retururi['Cantitate'] = abs(top_retururi['Cantitate'])  # Fac pozitiv pentru afișare
                        
                        fig = px.bar(
                            top_retururi,
                            x='Cantitate',
                            y='Denumire',
                            orientation='h',
                            title="Top 10 Produse Returnate",
                            color_discrete_sequence=['red']
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Retururi pe gestiuni
                    if 'DenumireGestiune' in retururi_df.columns:
                        retururi_gestiuni = retururi_df.groupby('DenumireGestiune')['Valoare'].sum().reset_index()
                        retururi_gestiuni['Valoare'] = abs(retururi_gestiuni['Valoare'])
                        
                        fig = px.pie(
                            retururi_gestiuni,
                            values='Valoare',
                            names='DenumireGestiune',
                            title="Distribuția Retururilor pe Gestiuni",
                            color_discrete_sequence=px.colors.sequential.Reds_r
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Retururi în timp
                    if 'Data' in retururi_df.columns:
                        retururi_df_copy = retururi_df.copy()
                        retururi_df_copy['Data_Str'] = retururi_df_copy['Data'].dt.strftime('%Y-%m-%d')
                        retururi_zilnic = retururi_df_copy.groupby('Data_Str')['Valoare'].sum().reset_index()
                        retururi_zilnic['Valoare'] = abs(retururi_zilnic['Valoare'])
                        
                        fig = px.line(
                            retururi_zilnic,
                            x='Data_Str',
                            y='Valoare',
                            title="Evoluția Retururilor în Timp",
                            color_discrete_sequence=['red']
                        )
                        fig.update_xaxes(title="Data")
                        fig.update_yaxes(title="Valoare Retururi")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nu au fost găsite retururi în perioada analizată.")
        
        st.markdown("---")
        
        # ===== SECȚIUNEA 7: PRODUCĂTORI =====
        st.markdown("### 🏭 Analiza Producătorilor")
        
        # 10. Market share producători
        if 'Producator' in vanzari_df.columns and 'Valoare' in vanzari_df.columns:
            producatori_valoare = vanzari_df.groupby('Producator')['Valoare'].sum().nlargest(10).reset_index()
            
            fig = px.pie(
                producatori_valoare,
                values='Valoare',
                names='Producator',
                title="Top 10 Producători - Market Share"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
