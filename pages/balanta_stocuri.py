"""
Pagina Balanță Stocuri pentru aplicația Brenado For House - OPTIMIZATĂ
Conține 2 subcategorii: La Dată și În Perioadă
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loaders import load_balanta_la_data, load_balanta_perioada

# ===== FUNCȚII HELPER PENTRU REUTILIZARE =====

@st.cache_data
def calculate_metrics(df, columns):
    """Calculează metrici pentru coloanele specificate"""
    metrics = {}
    for col in columns:
        metrics[col] = df[col].sum() if col in df.columns else 0
    return metrics

def safe_column_check(df, column):
    """Verifică dacă coloana există și returnează valorile unice"""
    return df[column].unique() if column in df.columns else []

def apply_filters(df, filters_dict):
    """Aplică multiple filtre pe DataFrame"""
    filtered_df = df.copy()
    for column, values in filters_dict.items():
        if column in df.columns and values:
            filtered_df = filtered_df[filtered_df[column].isin(values)]
    return filtered_df

def render_metrics_row(metrics_dict, format_str="{:,.0f} RON"):
    """Randează o linie de metrici"""
    cols = st.columns(len(metrics_dict))
    for i, (label, value) in enumerate(metrics_dict.items()):
        with cols[i]:
            st.metric(label, format_str.format(value))

def create_donut_chart(data_df, group_col, value_col, title, unit="unități"):
    """Creează un donut chart standard"""
    if data_df.empty:
        st.info("Nu există date pentru grafic.")
        return
    
    total_value = data_df[value_col].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=data_df[group_col],
        values=data_df[value_col],
        hole=0.4,
        textinfo='label+value',
        texttemplate=f'%{{label}}<br>%{{value}} {unit}',
        textposition='outside',
        hovertemplate=f'<b>%{{label}}</b><br>{value_col}: %{{value}} {unit}<extra></extra>'
    )])
    
    fig.add_annotation(
        text=f"<b>Total:<br>{total_value:,.0f} {unit}</b>",
        x=0.5, y=0.5, font_size=16, showarrow=False
    )
    
    fig.update_layout(
        title=title, title_x=0.5, height=500,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
    )
    
    return fig

def filter_and_display_table(df, columns_to_show):
    """Filtrează și afișează doar coloanele specificate"""
    available_columns = [col for col in columns_to_show if col in df.columns]
    
    if available_columns:
        return df[available_columns]
    else:
        st.warning(f"Coloanele cerute nu sunt disponibile în date: {columns_to_show}")
        return df

# ===== ÎNCĂRCARE DATE ȘI CONFIGURARE =====
st.markdown("### 📦 Balanță Stocuri")

# Încărcare date o singură dată
balanta_df = load_balanta_la_data()
perioada_df = load_balanta_perioada()

# Definire coloane pentru afișarea restrânsă
COLUMNS_TO_SHOW = ['DenumireGest', 'Denumire', 'UM', 'Pret', 'Stoc final', 'PretVanzare', 'Producator']

# Tabs pentru subcategoriile Balanță Stocuri
tab1, tab2, tab3 = st.tabs(["📅 În Dată", "📊 Perioadă", "🔍 Analize Stocuri"])

# ===== TAB 1: BALANȚĂ LA DATĂ =====
with tab1:
    st.markdown("#### 📅 Balanță Stocuri la Dată")
    
    # Calculare metrici principali
    metrics_tab1 = calculate_metrics(balanta_df, ['ValoareVanzare', 'ValoareStocFinal'])
    
    # Afișare metrici
    render_metrics_row({
        "Total Valoare Stoc Final": metrics_tab1['ValoareStocFinal'],
        "Total Valoare Vânzare": metrics_tab1['ValoareVanzare']
    })
    
    st.markdown("---")
    
    # FILTRARE INTERDEPENDENTĂ OPTIMIZATĂ - cu Producător în loc de Grupă
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gestiune_options = safe_column_check(balanta_df, 'DenumireGest')
        gestiune_filter = st.multiselect(
            "Filtrează după gestiune:",
            options=gestiune_options,
            default=[],
            key="gestiune_filter_tab1"
        )
    
    # Filtrare progresivă pentru producător (în loc de grupă)
    df_for_producator = apply_filters(balanta_df, {'DenumireGest': gestiune_filter})
    
    with col2:
        producator_options = safe_column_check(df_for_producator, 'Producator')
        producator_filter = st.multiselect(
            "Filtrează după producător:",
            options=producator_options,
            default=[],
            key="producator_filter_tab1"
        )
    
    # Filtrare progresivă pentru produs
    df_for_produs = apply_filters(df_for_producator, {'Producator': producator_filter})
    
    with col3:
        produs_options = safe_column_check(df_for_produs, 'Denumire')
        produs_filter = st.multiselect(
            "Filtrează după produs:",
            options=produs_options,
            default=[],
            key="produs_filter_tab1"
        )
    
    # Aplicare toate filtrele
    filters_tab1 = {
        'DenumireGest': gestiune_filter,
        'Producator': producator_filter,
        'Denumire': produs_filter
    }
    filtered_balanta = apply_filters(balanta_df, filters_tab1)
    
    # Filtrare și afișare tabel cu coloane restrânse
    st.markdown("#### 📋 Date Stocuri")
    table_data = filter_and_display_table(filtered_balanta, COLUMNS_TO_SHOW)
    st.dataframe(table_data, use_container_width=True)
    
    # Statistici filtrate
    if not filtered_balanta.empty and any(filters_tab1.values()):
        st.markdown("#### 📊 Statistici Date Filtrate")
        filtered_metrics = calculate_metrics(filtered_balanta, ['ValoareStocFinal', 'ValoareVanzare'])
        render_metrics_row({
            "Total Valoare Stoc Final Filtrată": filtered_metrics['ValoareStocFinal'],
            "Total Valoare Vânzare Filtrată": filtered_metrics['ValoareVanzare']
        })
    
    # Donut Chart (doar pentru produse selectate)
    if (produs_filter and 
        'Stoc final' in filtered_balanta.columns and 
        'DenumireGest' in filtered_balanta.columns):
        
        st.markdown("#### 📊 Distribuția Stocului pe Gestiuni")
        
        stoc_pe_gestiune = (filtered_balanta
                           .groupby('DenumireGest')['Stoc final']
                           .sum()
                           .reset_index())
        stoc_pe_gestiune = stoc_pe_gestiune[stoc_pe_gestiune['Stoc final'] > 0]
        
        if not stoc_pe_gestiune.empty:
            um_produs = filtered_balanta['UM'].iloc[0] if 'UM' in filtered_balanta.columns else "unități"
            nume_produs = produs_filter[0] if len(produs_filter) == 1 else "Produse Selectate"
            
            fig = create_donut_chart(
                stoc_pe_gestiune, 
                'DenumireGest', 
                'Stoc final',
                f"Distribuția Stocului: {nume_produs} ({um_produs})",
                um_produs
            )
            st.plotly_chart(fig, use_container_width=True)

# ===== TAB 2: BALANȚĂ PERIOADĂ =====
with tab2:
    st.markdown("#### 📊 Balanță Stocuri pe Perioadă")
    
    # Calculare metrici optimizat
    valoare_intrare = perioada_df['Valoare intrare'].sum() if 'Valoare intrare' in perioada_df.columns else 0
    
    # Calculare preț vânzare optimizat
    if all(col in perioada_df.columns for col in ['Stoc final', 'Pret vanzare']):
        pret_vanzare = (perioada_df['Stoc final'] * perioada_df['Pret vanzare']).sum()
    else:
        pret_vanzare = 0
    
    # Afișare metrici
    render_metrics_row({
        "Total Valoare Intrare": valoare_intrare,
        "Total Preț Vânzare": pret_vanzare
    })
    
    st.markdown("---")
    
    # Filtre tab2 - toate în același loc
    col1, col2, col3, col4 = st.columns(4)
    filter_configs = [
        (col1, 'Denumire gestiune', "gestiune"),
        (col2, 'Denumire', "produs"),
        (col3, 'Furnizor IN', "furnizor"),
        (col4, 'Producator', "producator")
    ]
    
    filters_tab2 = {}
    for col_widget, column_name, filter_name in filter_configs:
        with col_widget:
            options = safe_column_check(perioada_df, column_name)
            filters_tab2[column_name] = st.multiselect(
                f"Filtrează după {filter_name}:",
                options=options,
                default=[],
                key=f"{filter_name}_filter_tab2"
            )
    
    # Aplicare filtre
    filtered_perioada = apply_filters(perioada_df, filters_tab2)
    
    # Definire coloane pentru tab2 (perioada)
    COLUMNS_TO_SHOW_PERIOADA = ['Denumire gestiune', 'Denumire', 'UM', 'Pret vanzare', 'Stoc final', 'Valoare intrare', 'Producator']
    
    # Tabel cu date restrânse
    st.markdown("#### 📋 Date Perioada")
    table_data_perioada = filter_and_display_table(filtered_perioada, COLUMNS_TO_SHOW_PERIOADA)
    st.dataframe(table_data_perioada, use_container_width=True)
    
    # Statistici filtrate
    if not filtered_perioada.empty:
        st.markdown("#### 📊 Statistici Date Filtrate")
        
        intrare_filtrata = filtered_perioada['Valoare intrare'].sum() if 'Valoare intrare' in filtered_perioada.columns else 0
        
        if all(col in filtered_perioada.columns for col in ['Stoc final', 'Pret vanzare']):
            pret_vanzare_filtrat = (filtered_perioada['Stoc final'] * filtered_perioada['Pret vanzare']).sum()
        else:
            pret_vanzare_filtrat = 0
        
        render_metrics_row({
            "Total Valoare Intrare Filtrată": intrare_filtrata,
            "Total Preț Vânzare Filtrat": pret_vanzare_filtrat
        })

# ===== TAB 3: ANALIZE - OPTIMIZAT =====
with tab3:
    st.markdown("#### 🔍 Analize Stocuri")
    
    required_columns = ['DenumireGest', 'Producator', 'ValoareStocFinal', 'ValoareVanzare']
    
    if not balanta_df.empty and all(col in balanta_df.columns for col in required_columns):
        
        # Refolosim metricii calculați în tab1
        st.markdown("#### 📊 Totaluri Generale")
        render_metrics_row({
            "Total Valoare Stoc Final": metrics_tab1['ValoareStocFinal'],
            "Total Valoare Vânzare": metrics_tab1['ValoareVanzare']
        })
        
        st.markdown("---")
        st.markdown("#### 🗂️ Vizualizare Treemap Ierarhic")
        
        # Construire date treemap optimizat - cu Producator în loc de Grupa
        producatori_data = (balanta_df
                           .groupby(['DenumireGest', 'Producator'])
                           .agg({'ValoareStocFinal': 'sum', 'ValoareVanzare': 'sum'})
                           .reset_index())
        
        gestiuni_data = (balanta_df
                        .groupby('DenumireGest')
                        .agg({'ValoareStocFinal': 'sum', 'ValoareVanzare': 'sum'})
                        .reset_index())
        
        # Construire date treemap
        treemap_data = []
        
        # Producători
        for _, row in producatori_data.iterrows():
            treemap_data.append({
                'ids': f"{row['DenumireGest']}-{row['Producator']}",
                'labels': row['Producator'],
                'parents': row['DenumireGest'],
                'values': row['ValoareStocFinal'],
                'vanzare': row['ValoareVanzare']
            })
        
        # Gestiuni
        for _, row in gestiuni_data.iterrows():
            treemap_data.append({
                'ids': row['DenumireGest'],
                'labels': row['DenumireGest'],
                'parents': 'Brenado For House',
                'values': row['ValoareStocFinal'],
                'vanzare': row['ValoareVanzare']
            })
        
        # Root
        treemap_data.append({
            'ids': 'Brenado For House',
            'labels': 'Brenado For House',
            'parents': '',
            'values': metrics_tab1['ValoareStocFinal'],
            'vanzare': metrics_tab1['ValoareVanzare']
        })
        
        # Crearea și afișarea treemap
        df_treemap = pd.DataFrame(treemap_data)
        
        fig = go.Figure(go.Treemap(
            ids=df_treemap['ids'],
            labels=df_treemap['labels'],
            parents=df_treemap['parents'],
            values=df_treemap['values'],
            customdata=df_treemap['vanzare'],
            branchvalues="total",
            maxdepth=3,
            textinfo="label+value",
            texttemplate="<b>%{label}</b><br>Stoc: %{value:,.0f}<br>Vânzare: %{customdata:,.0f}",
            hovertemplate='<b>%{label}</b><br>Stoc Final: %{value:,.0f} RON<br>Vânzare: %{customdata:,.0f} RON<extra></extra>',
            textposition="middle center",
            textfont_size=11,
            marker_line_width=2,
            marker_line_color="white"
        ))
        
        fig.update_layout(
            height=700,
            title="Analiză Treemap: Brenado For House → Gestiuni → Producători",
            title_x=0.5,
            font_size=11,
            margin=dict(t=60, l=10, r=10, b=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Analiză detaliată optimizată
        st.markdown("#### 📊 Analiză Detaliată pe Gestiuni")
        
        # Formatare și sortare optimizată
        gestiuni_display = gestiuni_data.sort_values('ValoareStocFinal', ascending=False).copy()
        gestiuni_display['ValoareStocFinal'] = gestiuni_display['ValoareStocFinal'].apply(lambda x: f"{x:,.0f}")
        gestiuni_display['ValoareVanzare'] = gestiuni_display['ValoareVanzare'].apply(lambda x: f"{x:,.0f}")
        gestiuni_display.columns = ['Gestiune', 'Valoare Stoc Final', 'Valoare Vânzare']
        
        st.dataframe(gestiuni_display, use_container_width=True)
        
        # Metrici sumare
        top_gestiune = gestiuni_data.iloc[0]
        render_metrics_row({
            "Gestiuni": gestiuni_data['DenumireGest'].nunique(),
            "Valoare Top Stoc": top_gestiune['ValoareStocFinal'],
            "Valoare Top Vânzare": top_gestiune['ValoareVanzare']
        })
        
        # Afișare top gestiune ca text
        st.info(f"🏆 **Top Gestiune:** {top_gestiune['DenumireGest']}")
    
    else:
        st.warning("Nu sunt disponibile datele necesare pentru analize. Verifică coloanele: DenumireGest, Producator, ValoareStocFinal, ValoareVanzare.")
