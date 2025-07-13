"""
Pagina Facturi Neachitate pentru aplicația Brenado For House - ÎMBUNĂTĂȚITĂ
Cu analiză Plăți Cu Efecte și vizualizare Sunburst
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_loaders import load_neachitate

# ===== FUNCȚII HELPER =====

def categorize_by_scadenta(data_scadenta, data_curenta):
    """Categorizează facturile după scadență"""
    if pd.isna(data_scadenta):
        return "Necunoscută"
    
    if data_scadenta.date() == data_curenta:
        return "Azi"
    elif data_scadenta.date() > data_curenta:
        return "Scadență Viitoare"
    else:
        return "Scadență Depășită"

def create_sunburst_chart(df_efecte):
    """Creează Sunburst Chart pentru Plăți Cu Efecte"""
    if df_efecte.empty:
        st.warning("Nu există date pentru Plăți Cu Efecte")
        return None
    
    # Pregătire date pentru Sunburst
    data_curenta = datetime.now().date()
    
    # Adăugare categorie temporală
    df_efecte['Categorie_Scadenta'] = df_efecte['DataScadenta'].apply(
        lambda x: categorize_by_scadenta(x, data_curenta)
    )
    
    # Grupare pentru sunburst: Categorie -> Furnizor -> Suma
    sunburst_data = []
    
    # Nivel 1: Root (centru)
    total_efecte = df_efecte['Total'].sum()
    sunburst_data.append({
        'ids': 'PLATI_CU_EFECTE',
        'labels': 'PLĂȚI CU EFECTE',
        'parents': '',
        'values': total_efecte
    })
    
    # Nivel 2: Categorii temporale
    categorii = df_efecte.groupby('Categorie_Scadenta')['Total'].sum()
    for categorie, suma in categorii.items():
        sunburst_data.append({
            'ids': f'PLATI_CU_EFECTE_{categorie}',
            'labels': categorie,
            'parents': 'PLATI_CU_EFECTE',
            'values': suma
        })
    
    # Nivel 3: Furnizori pentru fiecare categorie
    furnizori_categorii = df_efecte.groupby(['Categorie_Scadenta', 'Furnizor'])['Total'].sum()
    for (categorie, furnizor), suma in furnizori_categorii.items():
        furnizor_id = f'PLATI_CU_EFECTE_{categorie}_{furnizor}'
        sunburst_data.append({
            'ids': furnizor_id,
            'labels': furnizor,
            'parents': f'PLATI_CU_EFECTE_{categorie}',
            'values': suma
        })
    
    # Nivel 4: Facturi individuale (opțional, pentru detalii)
    for _, row in df_efecte.iterrows():
        factura_id = f"PLATI_CU_EFECTE_{row['Categorie_Scadenta']}_{row['Furnizor']}_{row['Numar']}"
        sunburst_data.append({
            'ids': factura_id,
            'labels': f"{row['Numar']}: {row['Total']:,.0f} RON",
            'parents': f"PLATI_CU_EFECTE_{row['Categorie_Scadenta']}_{row['Furnizor']}",
            'values': row['Total']
        })
    
    # Creare DataFrame pentru Sunburst
    df_sunburst = pd.DataFrame(sunburst_data)
    
    # Creare Sunburst Chart
    fig = go.Figure(go.Sunburst(
        ids=df_sunburst['ids'],
        labels=df_sunburst['labels'],
        parents=df_sunburst['parents'],
        values=df_sunburst['values'],
        branchvalues="total",
        maxdepth=4,
        hovertemplate='<b>%{label}</b><br>Suma: %{value:,.0f} RON<br>Procent: %{percentParent}<extra></extra>',
    ))
    
    fig.update_layout(
        title={
            'text': "📊 Analiză Plăți Cu Efecte - Sunburst",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        height=600,
        margin=dict(t=80, l=50, r=50, b=50)
    )
    
    return fig

# ===== PAGINA PRINCIPALĂ =====

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

# Calculare metrici pentru Plăți Cu Efecte
total_efecte = neachitate_df[neachitate_df['AchitatEfecte'] > 0]['Total'].sum() if 'AchitatEfecte' in neachitate_df.columns else 0
nr_facturi_efecte = len(neachitate_df[neachitate_df['AchitatEfecte'] > 0]) if 'AchitatEfecte' in neachitate_df.columns else 0

# Metrici principale
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sold", f"{total_sold:,.0f} RON")
with col2:
    st.metric("Scadența Azi", f"{scadenta_azi:,.0f} RON")
with col3:
    st.metric("💳 Plăți Cu Efecte", f"{total_efecte:,.0f} RON", delta=f"{nr_facturi_efecte} facturi")

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

# ===== GRAFIC PLĂȚI CU EFECTE (PERMANENT SUB TABEL) =====
st.markdown("### 💳 Analiză Plăți Cu Efecte")

# Filtrare pentru Plăți Cu Efecte (din toate datele, nu din cele filtrate)
df_efecte = neachitate_df[neachitate_df['AchitatEfecte'] > 0].copy()

if not df_efecte.empty:
    # Creare și afișare Sunburst Chart
    fig = create_sunburst_chart(df_efecte)
    
    if fig:
        st.plotly_chart(fig, use_container_width=True)
    
    # Statistici rapide pentru Plăți Cu Efecte
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Plăți Cu Efecte", f"{total_efecte:,.0f} RON")
    with col2:
        st.metric("Facturi Cu Efecte", f"{nr_facturi_efecte}")
    with col3:
        if total_sold > 0:
            procent_efecte = (total_efecte / total_sold) * 100
            st.metric("% Din Total Sold", f"{procent_efecte:.1f}%")

else:
    st.info("🔍 Nu există facturi cu Plăți Cu Efecte (AchitatEfecte > 0)")
