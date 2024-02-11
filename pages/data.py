import streamlit as st
import pandas as pd

# Assuming your assets folder is in the same directory as your Streamlit script
data_path = "assets/"

# Dictionary to map data options to their corresponding filenames
data_files = {
    'Data1': 'data1.xlsx',
    'Data2': 'data2.xlsx',
    'Data3': 'data3.xlsx',
}

# Using an expander for data selection
with st.expander("Select Data"):
    # Example data options for selection
    data_options = list(data_files.keys())
    selected_data = st.selectbox("Alege datele", options=data_options)

# Main page display logic based on data selection
if not selected_data:
    st.info("Va rugam alegeti datele pentru analiza", icon="ℹ️")
else:
    # Get the filename for the selected data
    filename = data_files[selected_data]

    # Construct the full path to the selected data file
    file_path = data_path + filename
    
    try:
        # Read the selected Excel file into a DataFrame
        df = pd.read_excel(file_path)

        # Proceed with analysis using the selected data
        st.write(f"Ati ales: {selected_data}")
        st.dataframe(df)  # Display the DataFrame as a table
        # Add your analysis code here

    except Exception as e:
        st.error(f"Failed to read {selected_data} from {file_path}. Error: {e}")
