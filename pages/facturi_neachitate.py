"""
Pagina Facturi Neachitate pentru aplicația Brenado For House
Cu analiză Plăți Cu Efecte și vizualizare Sunburst
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_loaders import load_neachitate

# Titlu pagină
st.markdown("### ❌ Facturi Neachitate")

# Încărcare date
neachitate_df = load_neachitate()

# Adăugare coloană AchitatEfecte pentru demo (în realitate va fi în Excel)
if 'AchitatEfecte' not in neachitate_df.columns:
    # Simulez coloana AchitatEfecte cu valori random pentru demo
    import numpy as np
    np.random.seed(42)
    neachitate_df['AchitatEfecte'] = np.random.choice([0, 1500, 2000, 0, 3000, 0], len(neachitate_df))

# Conversie DataScadenta la datetime
if 'DataScadenta' in neachitate_df.columns:
    neachitate_df['DataScadenta'] = pd.to_datetime(neachitate_df['DataScadenta'])

# Calculare metrici globali
total_sold = neachitate_df['Sold'].sum() if 'Sold' in neachitate_df.columns else 0

# Calculare Scadenta Azi
scadenta_azi = 0
if 'DataScadenta' in neachitate_df.columns:
    data_curenta = datetime.now().date()
    facturi_azi = neachitate_df[neachitate_df['DataScadenta'].dt.date == data_curenta]
    scadenta_azi = facturi_azi['Sold'].sum() if not facturi_azi.empty and 'Sold' in facturi_azi.columns else 0

# Metrici principale (doar cele originale)
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sold", f"{total_sold:,.0f} RON")
with col2:
    st.metric("Scadența Azi", f"{scadenta_azi:,.0f} RON")

st.markdown("---")

# Filtre (doar cele originale)
col1, col2 = st.columns(2)

with col1:
    # Filtru furnizor
    if 'Furnizor' in neachitate_df.columns:
        furnizor_filter = st.multiselect(
            "Filtrează după furnizor:",
            options=neachitate_df['Furnizor'].unique(),
            default=[],
            key="furnizor_filter"
        )

with col2:
    # Filtru scadențe depășite
    scadenta_filter = st.selectbox(
        "Filtrează facturi cu scadența depășită:",
        options=["Toate", "Săptămâna Curentă", "Luna Curentă"],
        index=0,
        key="scadenta_filter"
    )

# Aplicare filtre
filtered_df = neachitate_df.copy()

# Filtru furnizor
if 'Furnizor' in neachitate_df.columns and furnizor_filter:
    filtered_df = filtered_df[filtered_df['Furnizor'].isin(furnizor_filter)]

# Filtru scadențe depășite
if 'DataScadenta' in neachitate_df.columns and scadenta_filter != "Toate":
    data_curenta = datetime.now().date()
    
    if scadenta_filter == "Săptămâna Curentă":
        start_week = data_curenta - timedelta(days=data_curenta.weekday())
        filtered_df = filtered_df[
            (filtered_df['DataScadenta'].dt.date < data_curenta) & 
            (filtered_df['DataScadenta'].dt.date >= start_week)
        ]
    
    elif scadenta_filter == "Luna Curentă":
        start_month = data_curenta.replace(day=1)
        filtered_df = filtered_df[
            (filtered_df['DataScadenta'].dt.date < data_curenta) & 
            (filtered_df['DataScadenta'].dt.date >= start_month)
        ]

# Afișare tabel cu datele filtrate
st.dataframe(filtered_df, use_container_width=True)

# Metrici pentru datele filtrate (sub tabel)
if not filtered_df.empty:
    st.markdown("#### 📊 Statistici Date Filtrate")
    total_sold_filtrat = filtered_df['Sold'].sum() if 'Sold' in filtered_df.columns else 0
    st.metric("Total Sold Filtrat", f"{total_sold_filtrat:,.0f} RON")

st.markdown("---")

# ===== GRAFIC PLĂȚI CU EFECTE (PERMANENT) =====
st.markdown("### 💳 Plăți Cu Efecte")

# Filtrare doar facturile cu AchitatEfecte > 0
df_efecte = neachitate_df[neachitate_df['AchitatEfecte'] > 0].copy()

if not df_efecte.empty:
    # Categorizare după scadență
    data_curenta = datetime.now().date()
    
    def get_categoria_scadenta(data_scadenta):
        if pd.isna(data_scadenta):
            return "Necunoscută"
        if data_scadenta.date() == data_curenta:
            return "Azi"
        elif data_scadenta.date() > data_curenta:
            return "Scadență Viitoare"
        else:
            return "Scadență Depășită"
    
    df_efecte['Categoria'] = df_efecte['DataScadenta'].apply(get_categoria_scadenta)
    
    # Construire date pentru Sunburst
    # Nivel 1: Root
    total_efecte = df_efecte['Total'].sum()
    
    # Nivel 2: Categorii (Azi, Scadență Viitoare, Scadență Depășită) - toate sumele
    categorii_sume = df_efecte.groupby('Categoria')[['Total', 'Sold', 'AchitatEfecte']].sum()
    
    # Nivel 3: Furnizori pe fiecare categorie - toate sumele
    furnizori_categorii = df_efecte.groupby(['Categoria', 'Furnizor'])[['Total', 'Sold', 'AchitatEfecte']].sum()
    
    # Calcul sume totale pentru root
    total_efecte = df_efecte['Total'].sum()
    total_sold = df_efecte['Sold'].sum()
    total_achitat_efecte = df_efecte['AchitatEfecte'].sum()
    
    # Construire liste pentru Sunburst
    ids = ['PLATI_CU_EFECTE']
    labels = [f'PLĂȚI CU EFECTE<br>Total: {total_efecte:,.0f}<br>Sold: {total_sold:,.0f}<br>Efecte: {total_achitat_efecte:,.0f}']  
    parents = ['']
    values = [total_efecte]
    
    # Adaugă categoriile
    for categoria, row in categorii_sume.iterrows():
        ids.append(f'CAT_{categoria}')
        labels.append(f'{categoria}<br>Total: {row["Total"]:,.0f}<br>Sold: {row["Sold"]:,.0f}<br>Efecte: {row["AchitatEfecte"]:,.0f}')
        parents.append('PLATI_CU_EFECTE')
        values.append(row['Total'])
    
    # Adaugă furnizorii
    for (categoria, furnizor), row in furnizori_categorii.iterrows():
        ids.append(f'CAT_{categoria}_FURN_{furnizor}')
        labels.append(f'{furnizor}<br>Total: {row["Total"]:,.0f}<br>Sold: {row["Sold"]:,.0f}<br>Efecte: {row["AchitatEfecte"]:,.0f}')
        parents.append(f'CAT_{categoria}')
        values.append(row['Total'])
    
    # Creare Sunburst Chart
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        maxdepth=3,
        hovertemplate='<b>%{label}</b><br>Suma: %{value:,.0f} RON<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 Distribuția Plăților Cu Efecte",
        height=500,
        font_size=12
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Afișare statistici
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Efecte", f"{total_efecte:,.0f} RON")
    with col2:
        st.metric("Facturi", f"{len(df_efecte)}")
    with col3:
        if total_sold > 0:
            procent = (total_efecte / total_sold) * 100
            st.metric("% din Total", f"{procent:.1f}%")

else:
    st.info("Nu există facturi cu Plăți Cu Efecte (AchitatEfecte > 0)")
