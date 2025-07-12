"""
Pagina Balanță Stocuri pentru aplicația Brenado For House
Conține 2 subcategorii: La Dată și În Perioadă
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loaders import load_balanta_la_data, load_balanta_perioada

# Titlu pagină
st.markdown("### 📦 Balanță Stocuri")

# Tabs pentru subcategoriile Balanță Stocuri
tab1, tab2, tab3 = st.tabs(["📅 În Dată", "📊 Perioadă", "🔍 Analize Stocuri"])

with tab1:
    st.markdown("#### 📅 Balanță Stocuri la Dată")
    
    # Încărcare date
    balanta_df = load_balanta_la_data()
    
    # Calculare metrici
    total_valoare_vanzare = balanta_df['ValoareVanzare'].sum() if 'ValoareVanzare' in balanta_df.columns else 0
    total_valoare_stoc_final = balanta_df['ValoareStocFinal'].sum() if 'ValoareStocFinal' in balanta_df.columns else 0
    
    # Metrici principale
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Valoare Stoc Final", f"{total_valoare_stoc_final:,.0f} RON")
    with col2:
        st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare:,.0f} RON")
    
    st.markdown("---")
    
    # Filtrare date - INTERDEPENDENTE
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'DenumireGest' in balanta_df.columns:
            gestiune_filter = st.multiselect(
                "Filtrează după gestiune:",
                options=balanta_df['DenumireGest'].unique(),
                default=[],
                key="gestiune_filter_tab1"
            )
    
    # Filtrare pentru grupa bazată pe gestiunea selectată
    df_for_grupa = balanta_df.copy()
    if 'DenumireGest' in balanta_df.columns and gestiune_filter:
        df_for_grupa = df_for_grupa[df_for_grupa['DenumireGest'].isin(gestiune_filter)]
    
    with col2:
        if 'Grupa' in balanta_df.columns:
            # Afișează doar grupele din gestiunile selectate
            grupa_options = df_for_grupa['Grupa'].unique() if not df_for_grupa.empty else []
            grupa_filter = st.multiselect(
                "Filtrează după grupă:",
                options=grupa_options,
                default=[],
                key="grupa_filter_tab1"
            )
    
    # Filtrare pentru produs bazată pe gestiunea și grupa selectate
    df_for_produs = df_for_grupa.copy()
    if 'Grupa' in balanta_df.columns and grupa_filter:
        df_for_produs = df_for_produs[df_for_produs['Grupa'].isin(grupa_filter)]
    
    with col3:
        if 'Denumire' in balanta_df.columns:
            # Afișează doar produsele din gestiunile și grupele selectate
            produs_options = df_for_produs['Denumire'].unique() if not df_for_produs.empty else []
            produs_filter = st.multiselect(
                "Filtrează după produs:",
                options=produs_options,
                default=[],
                key="produs_filter_tab1"
            )
    
    # Aplicare filtre
    filtered_balanta = balanta_df.copy()
    if 'DenumireGest' in balanta_df.columns and gestiune_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['DenumireGest'].isin(gestiune_filter)]
    
    if 'Grupa' in balanta_df.columns and grupa_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['Grupa'].isin(grupa_filter)]
    
    if 'Denumire' in balanta_df.columns and produs_filter:
        filtered_balanta = filtered_balanta[filtered_balanta['Denumire'].isin(produs_filter)]
    
    # Tabel cu date
    st.dataframe(filtered_balanta, use_container_width=True)


    
    # Statistici pentru datele filtrate (doar când s-au aplicat filtre)
    if not filtered_balanta.empty and (gestiune_filter or grupa_filter or produs_filter):
        st.markdown("#### 📊 Statistici Date Filtrate")
        col1, col2 = st.columns(2)
        
        with col1:
            valoare_stoc_filtrata = filtered_balanta['ValoareStocFinal'].sum() if 'ValoareStocFinal' in filtered_balanta.columns else 0
            st.metric("Total Valoare Stoc Final Filtrată", f"{valoare_stoc_filtrata:,.0f} RON")
        with col2:
            valoare_vanzare_filtrata = filtered_balanta['ValoareVanzare'].sum() if 'ValoareVanzare' in filtered_balanta.columns else 0
            st.metric("Total Valoare Vânzare Filtrată", f"{valoare_vanzare_filtrata:,.0f} RON")
    
    # Donut Chart pentru stocuri pe gestiuni (doar când se filtrează după produs)
    if produs_filter and 'Stoc final' in filtered_balanta.columns and 'DenumireGest' in filtered_balanta.columns:
        st.markdown("#### 📊 Distribuția Stocului pe Gestiuni")
        
        # Grupare după gestiune și sumarea stocurilor
        stoc_pe_gestiune = filtered_balanta.groupby('DenumireGest')['Stoc final'].sum().reset_index()
        stoc_pe_gestiune = stoc_pe_gestiune[stoc_pe_gestiune['Stoc final'] > 0]  # Doar gestiunile cu stoc
        
        if not stoc_pe_gestiune.empty:
            # Calculare total pentru centru
            total_stoc = stoc_pe_gestiune['Stoc final'].sum()
            
            # Extragerea unității de măsură pentru produsul selectat
            if 'UM' in filtered_balanta.columns:
                um_produs = filtered_balanta['UM'].iloc[0] if not filtered_balanta.empty else "unități"
            else:
                um_produs = "unități"
            
            # Numele produsului pentru label central
            nume_produs = produs_filter[0] if len(produs_filter) == 1 else "Produse Selectate"
            
            # Crearea donut chart-ului
            fig = go.Figure(data=[go.Pie(
                labels=stoc_pe_gestiune['DenumireGest'],
                values=stoc_pe_gestiune['Stoc final'],
                hole=0.4,  # Crează gaura din mijloc pentru donut
                textinfo='label+value',
                texttemplate=f'%{{label}}<br>%{{value}} {um_produs}',
                textposition='outside',
                hovertemplate=f'<b>%{{label}}</b><br>Stoc: %{{value}} {um_produs}<extra></extra>'
            )])
            
            # Adăugare text în centru cu totalul - DINAMIC
            fig.add_annotation(
                text=f"<b>Stoc total:<br>{total_stoc:,.0f} {um_produs}</b>",
                x=0.5, y=0.5,
                font_size=16,
                showarrow=False
            )
            
            # Configurare layout
            fig.update_layout(
                title=f"Distribuția Stocului: {nume_produs} ({um_produs})",
                title_x=0.5,
                height=500,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            
            # Afișare grafic
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nu există date de stoc pentru produsele filtrate.")




with tab2:
    st.markdown("#### 📊 Balanță Stocuri pe Perioadă")
    
    # Încărcare date
    perioada_df = load_balanta_perioada()
    
    # Calculare metrici
    total_valoare_intrare = perioada_df['Valoare intrare'].sum() if 'Valoare intrare' in perioada_df.columns else 0
    # Calculare total preț vânzare = Stoc final × Preț vânzare pentru fiecare produs
    if 'Stoc final' in perioada_df.columns and 'Pret vanzare' in perioada_df.columns:
        total_pret_vanzare = (perioada_df['Stoc final'] * perioada_df['Pret vanzare']).sum()
    else:
        total_pret_vanzare = 0
    
    # Metrici principale
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Valoare Intrare", f"{total_valoare_intrare:,.0f} RON")
    with col2:
        st.metric("Total Preț Vânzare", f"{total_pret_vanzare:,.0f} RON")
    
    st.markdown("---")
    
    # Filtrare date
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if 'Denumire gestiune' in perioada_df.columns:
            gestiune_filter = st.multiselect(
                "Filtrează după gestiune:",
                options=perioada_df['Denumire gestiune'].unique(),
                default=[],
                key="gestiune_filter_tab2"
            )
    
    with col2:
        if 'Denumire' in perioada_df.columns:
            produs_filter = st.multiselect(
                "Filtrează după produs:",
                options=perioada_df['Denumire'].unique(),
                default=[],
                key="produs_filter_tab2"
            )
    
    with col3:
        if 'Furnizor IN' in perioada_df.columns:
            furnizor_filter = st.multiselect(
                "Filtrează după furnizor:",
                options=perioada_df['Furnizor IN'].unique(),
                default=[],
                key="furnizor_filter_tab2"
            )
    
    with col4:
        if 'Producator' in perioada_df.columns:
            producator_filter = st.multiselect(
                "Filtrează după producător:",
                options=perioada_df['Producator'].unique(),
                default=[],
                key="producator_filter_tab2"
            )
    
    # Aplicare filtre
    filtered_perioada = perioada_df.copy()
    if 'Denumire gestiune' in perioada_df.columns and gestiune_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Denumire gestiune'].isin(gestiune_filter)]
    
    if 'Denumire' in perioada_df.columns and produs_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Denumire'].isin(produs_filter)]
    
    if 'Furnizor IN' in perioada_df.columns and furnizor_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Furnizor IN'].isin(furnizor_filter)]
    
    if 'Producator' in perioada_df.columns and producator_filter:
        filtered_perioada = filtered_perioada[filtered_perioada['Producator'].isin(producator_filter)]
    
    # Tabel cu date
    st.dataframe(filtered_perioada, use_container_width=True)
    
    # Statistici pentru datele filtrate
    if not filtered_perioada.empty:
        st.markdown("#### 📊 Statistici Date Filtrate")
        col1, col2 = st.columns(2)
        
        with col1:
            valoare_intrare_filtrata = filtered_perioada['Valoare intrare'].sum() if 'Valoare intrare' in filtered_perioada.columns else 0
            st.metric("Total Valoare Intrare Filtrată", f"{valoare_intrare_filtrata:,.0f} RON")
        with col2:
            # Calculare total preț vânzare filtrat = Stoc final × Preț vânzare pentru datele filtrate
            if 'Stoc final' in filtered_perioada.columns and 'Pret vanzare' in filtered_perioada.columns:
                pret_vanzare_filtrat = (filtered_perioada['Stoc final'] * filtered_perioada['Pret vanzare']).sum()
            else:
                pret_vanzare_filtrat = 0
            st.metric("Total Preț Vânzare Filtrat", f"{pret_vanzare_filtrat:,.0f} RON")





with tab3:
    st.markdown("#### 🔍 Analize Stocuri ")
    
    # Folosim datele și totalurile deja calculate în tab1
    analiza_df = balanta_df.copy()  # Folosim aceleași date
    
    if not analiza_df.empty and all(col in analiza_df.columns for col in ['DenumireGest', 'Grupa', 'ValoareStocFinal', 'ValoareVanzare']):
        
        # Folosim totalurile deja calculate în tab1
        # total_valoare_stoc_general = total_valoare_stoc_final (din tab1)
        # total_valoare_vanzare_general = total_valoare_vanzare (din tab1)
        
        # Metrici generale în partea de sus (folosind valorile din tab1)
        st.markdown("#### 📊 Totaluri Generale")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Valoare Stoc Final", f"{total_valoare_stoc_final:,.0f} RON")
        with col2:
            st.metric("Total Valoare Vânzare", f"{total_valoare_vanzare:,.0f} RON")
        
        st.markdown("---")
        
        # Vizualizare Treemap ierarhic cu ambele valori
        st.markdown("#### 🗂️ Vizualizare Treemap Ierarhic")
        
        # Preparare date pentru Treemap ierarhic
        import pandas as pd
        
        # Construire date pentru treemap cu path ierarhic
        treemap_data = []
        
        # Grupe - nivelul cel mai detaliat
        grupe_data = analiza_df.groupby(['DenumireGest', 'Grupa']).agg({
            'ValoareStocFinal': 'sum',
            'ValoareVanzare': 'sum'
        }).reset_index()
        
        for _, grupa in grupe_data.iterrows():
            treemap_data.append({
                'ids': f"{grupa['DenumireGest']}-{grupa['Grupa']}",
                'labels': grupa['Grupa'],
                'parents': grupa['DenumireGest'],
                'values': grupa['ValoareStocFinal'],
                'vanzare': grupa['ValoareVanzare'],
                'niveau': 'grupa'
            })
        
        # Gestiuni - nivelul intermediar
        gestiuni_data = analiza_df.groupby('DenumireGest').agg({
            'ValoareStocFinal': 'sum',
            'ValoareVanzare': 'sum'
        }).reset_index()
        
        for _, gestiune in gestiuni_data.iterrows():
            treemap_data.append({
                'ids': gestiune['DenumireGest'],
                'labels': gestiune['DenumireGest'],
                'parents': 'Brenado For House',
                'values': gestiune['ValoareStocFinal'],
                'vanzare': gestiune['ValoareVanzare'],
                'niveau': 'gestiune'
            })
        
        # Total - root (folosind totalurile din tab1)
        treemap_data.append({
            'ids': 'Brenado For House',
            'labels': 'Brenado For House',
            'parents': '',
            'values': total_valoare_stoc_final,  # Din tab1
            'vanzare': total_valoare_vanzare,    # Din tab1
            'niveau': 'total'
        })
        
        # Conversie la DataFrame
        df_treemap = pd.DataFrame(treemap_data)
        
        # Crearea Treemap cu go.Figure pentru control complet
        fig = go.Figure(go.Treemap(
            ids=df_treemap['ids'],
            labels=df_treemap['labels'],
            parents=df_treemap['parents'],
            values=df_treemap['values'],
            customdata=df_treemap['vanzare'],
            branchvalues="total",
            maxdepth=3,
            textinfo="label+value",
            texttemplate="<b>%{label}</b><br>Total_Stoc: %{value:,.0f}<br>Total_Vânzare: %{customdata:,.0f}",
            hovertemplate='<b>%{label}</b><br>' +
                         'Stoc Final: %{value:,.0f} RON<br>' +
                         'Vânzare: %{customdata:,.0f} RON<extra></extra>',
            textposition="middle center",
            textfont_size=11,
            pathbar_textfont_size=12,
            marker_line_width=2,
            marker_line_color="white"
        ))
        
        # Layout optimizat pentru treemap
        fig.update_layout(
            height=700,
            title="Analiză Treemap: Brenado For House → Gestiuni → Grupe",
            title_x=0.5,
            font_size=11,
            margin=dict(t=60, l=10, r=10, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Analiză detaliată pe gestiuni cu ambele valori
        st.markdown("#### 📊 Analiză Detaliată pe Gestiuni")
        gestiuni_summary = analiza_df.groupby('DenumireGest').agg({
            'ValoareStocFinal': 'sum',
            'ValoareVanzare': 'sum'
        }).reset_index()
        
        # Păstrăm valorile numerice pentru metrici
        gestiuni_summary_numeric = gestiuni_summary.copy()
        
        # Rotunjirea valorilor pentru afișare
        gestiuni_summary['ValoareStocFinal'] = gestiuni_summary['ValoareStocFinal'].round(0).astype(int)
        gestiuni_summary['ValoareVanzare'] = gestiuni_summary['ValoareVanzare'].round(0).astype(int)
        
        # Sortarea înainte de formatare (pe valori numerice)
        gestiuni_summary = gestiuni_summary.sort_values('ValoareStocFinal', ascending=False)
        gestiuni_summary_numeric = gestiuni_summary_numeric.sort_values('ValoareStocFinal', ascending=False)
        
        # Formatarea cu separatoare de mii după sortare DOAR pentru DataFrame afișat
        gestiuni_summary_display = gestiuni_summary.copy()
        gestiuni_summary_display['ValoareStocFinal'] = gestiuni_summary_display['ValoareStocFinal'].apply(lambda x: f"{x:,}")
        gestiuni_summary_display['ValoareVanzare'] = gestiuni_summary_display['ValoareVanzare'].apply(lambda x: f"{x:,}")
        
        gestiuni_summary_display.columns = ['Gestiune', 'Valoare Stoc Final', 'Valoare Vânzare']
        
        st.dataframe(gestiuni_summary_display, use_container_width=True)
        
        # Metrici sumare - folosind valorile numerice
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            nr_gestiuni = analiza_df['DenumireGest'].nunique()
            st.metric("Gestiuni", f"{nr_gestiuni}")
        
        with col2:
            gestiune_top = gestiuni_summary_numeric.iloc[0]['DenumireGest']
            st.metric("Top Gestiune", gestiune_top)
        
        with col3:
            valoare_top_stoc = gestiuni_summary_numeric.iloc[0]['ValoareStocFinal']
            st.metric("Valoare Top Stoc", f"{valoare_top_stoc:,.0f} RON")
        
        with col4:
            valoare_top_vanzare = gestiuni_summary_numeric.iloc[0]['ValoareVanzare']
            st.metric("Valoare Top Vânzare", f"{valoare_top_vanzare:,.0f} RON")
    
    else:
        st.warning("Nu sunt disponibile datele necesare pentru analiza Treemap. Verifică că fișierul conține coloanele: DenumireGest, Grupa, ValoareStocFinal, ValoareVanzare.")
