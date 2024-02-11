import streamlit as st
import pandas as pd

# Radio buttons for data selection directly in the app, not inside an expander
selected_data = st.radio("Alege datele", ('Date ani anteriori', 'Date Depozit', 'Date Predictii'))

# Main page display logic based on data selection
if selected_data == 'Date ani anteriori':
    df = pd.read_excel('./assets/Data2.xlsx')
elif selected_data == 'Date Depozit':
    df = pd.read_excel('./assets/Data1.xlsx')
elif selected_data == 'Date Predictii':
    df = pd.read_excel('./assets/data3.xlsx')
else:
    st.info("Vă rugăm alegeți datele pentru analiză", icon="ℹ️")
    st.stop()

# Display the selected data
st.write(f"Ați ales: {selected_data}")
st.dataframe(df)  # Display the DataFrame as a table
