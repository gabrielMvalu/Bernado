import streamlit as st


# Using an expander for data selection
with st.expander("Select Data"):
    # Example data options for selection
    data_options = ['Data 1', 'Data 2', 'Data 3']
    selected_data = st.selectbox("Choose your data", options=data_options)

# Main page display logic based on data selection
if not selected_data:
    st.info("Please select data for analysis", icon="ℹ️")
else:
    # Proceed with analysis using the selected data
    st.write(f"You have selected: {selected_data}")
    # Add your analysis code here
