"""
Funcții pentru încărcarea datelor din fișierele Excel
"""

import streamlit as st
import pandas as pd

@st.cache_data
def load_balanta_la_data():
    """Încarcă datele din Excel - Balanță la dată"""
    try:
        df = pd.read_excel("data/LaData.xlsx")
        return df
    except:
        return pd.DataFrame({
            'DenumireGest': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ValoareStocFinal': [5000]
        })

@st.cache_data
def load_balanta_perioada():
    """Încarcă datele din Excel - Balanță pe perioadă"""
    try:
        df = pd.read_excel("data/Perioada.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Denumire gestiune': ['Demo Gestiune'],
            'Denumire': ['Produs Demo'],
            'Stoc final': [100],
            'ZileVechime': [10]
        })



@st.cache_data
def load_neachitate():
    """Încarcă datele din Excel - Facturi Neachitate"""
    try:
        df = pd.read_excel("data/FacturiNeachitate.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Furnizor': ['Furnizor Demo 1', 'Furnizor Demo 2'],
            'Numar': ['F001', 'F002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [5000, 3000],
            'Sold': [5000, 1500],
            'Valuta': ['EUR', 'EUR'],
            'Serie': ['Demo1', 'Demo2'],
            'PL': ['PL 01', 'PL 02']
        })


@st.cache_data
def load_neincasate():
    """Încarcă datele din Excel - Facturi Neîncasate"""
    try:
        df = pd.read_excel("data/FacturiNeincasate.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Client': ['Client Demo 1', 'Client Demo 2'],
            'Numar': ['F001', 'F002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Total': [5000, 3000],
            'Sold': [5000, 1500],
            'Valuta': ['RON', 'RON'],
            'Serie': ['Demo1', 'Demo2'],
            'PL': ['PL 01', 'PL 02']
        })

# TODO: Adăugare alte funcții load_* pentru celelalte pagini
