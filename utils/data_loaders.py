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


@st.cache_data
def load_scadente_plati():
    """Încarcă datele din Excel - Scadențe Plăți Cu Efecte"""
    try:
        df = pd.read_excel("data/ScadentePlatiCuEfecte.xlsx")
        return df
    except:
        return pd.DataFrame({
            'Beneficiar': ['Beneficiar Demo 1', 'Beneficiar Demo 2'],
            'Numar': ['E001', 'E002'],
            'Data': ['2024-01-01', '2024-01-02'],
            'DataScadenta': ['2024-01-31', '2024-02-01'],
            'Valoare': [10000, 15000],
            'Valuta': ['RON', 'RON'],
            'TipEfect': ['Cambie', 'Bilet la ordin'],
            'Serie': ['Demo1', 'Demo2']
        })




@st.cache_data
def load_vanzari():
    """Încarcă datele din Excel - Vânzări"""
    try:
        df = pd.read_excel("data/VS.xlsx")

        
        return df
    except Exception as e:
        # Date demo în caz de eroare
        return pd.DataFrame({
            'Data': pd.to_datetime(['2024-07-01', '2024-07-02', '2024-07-03']),
            'Client': ['Client Demo 1', 'Client Demo 2', 'Client Demo 3'],
            'Denumire': ['Produs Demo A', 'Produs Demo B', 'Produs Demo C'],
            'Cantitate': [10, 5, 15],
            'Valoare': [1000, 500, 1500],
            'Adaos': [100, 50, 150],
            'Agent': ['Agent Demo 1', 'Agent Demo 1', 'Agent Demo 2'],
            'DenumireGestiune': ['Gestiune Demo 1', 'Gestiune Demo 2', 'Gestiune Demo 1'],
            'Cod': ['P001', 'P002', 'P003'],
            'UM': ['buc', 'buc', 'buc']
        })




# TODO: Adăugare alte funcții load_* pentru celelalte pagini
