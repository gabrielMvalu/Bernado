import streamlit as st
import pandas as pd

# Inițializează st.session_state pentru selecția datelor dacă nu există deja
if 'selected_data' not in st.session_state:
    st.session_state['selected_data'] = None

# Funcție pentru a actualiza st.session_state când se face o nouă selecție
def update_selected_data():
    st.session_state['selected_data'] = selected_data

# Radio buttons for data selection directly in the app
selected_data = st.radio("Alege datele", ('Date ani anteriori', 'Date Depozit', 'Date Predictii'), 
                         index=['Date ani anteriori', 'Date Depozit', 'Date Predictii'].index(st.session_state['selected_data']) if st.session_state['selected_data'] else 0,
                         on_change=update_selected_data)

# Main page display logic based on data selection
if st.session_state['selected_data'] == 'Date ani anteriori':
    df = pd.read_excel('./assets/Data2.xlsx')
elif st.session_state['selected_data'] == 'Date Depozit':
    df = pd.read_excel('./assets/Data1.xlsx')
elif st.session_state['selected_data'] == 'Date Predictii':
    df = pd.read_excel('./assets/Data3.xlsx')
else:
    st.info("Vă rugăm alegeți datele pentru analiză", icon="ℹ️")
    st.stop()

# Display the selected data
st.write(f"Ați ales: {st.session_state['selected_data']}")
st.dataframe(df)  # Display the DataFrame as a table

