import streamlit as st
import pandas as pd

# Using an expander for data selection
with st.expander("Select Data"):
    # Radio buttons for data selection
    selected_data = st.radio("Alege datele", ('Data1', 'Data2', 'Data3'))

# Main page display logic based on data selection
if selected_data == 'Data1':
    df = pd.read_excel('./assets/data1.xlsx')
elif selected_data == 'Data2':
    df = pd.read_excel('./assets/data2.xlsx')
elif selected_data == 'Data3':
    df = pd.read_excel('./assets/data3.xlsx')
else:
    st.info("Va rugam alegeti datele pentru analiza", icon="ℹ️")
    st.stop()

# Display the selected data
st.write(f"Ati ales: {selected_data}")
st.dataframe(df)  # Display the DataFrame as a table
