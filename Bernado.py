#Main Page
import streamlit as st
from streamlit import config as _config

# Asigurați-vă că titlul paginii este setat conform preferințelor dvs.
st.set_page_config(page_title='Statistici curente', page_icon=None, layout='centered', initial_sidebar_state='auto')

# Puteți adăuga un logo și un titlu în bara laterală dacă doriți
# st.sidebar.image('./assets/Brenado.PNG', use_column_width=True)
st.sidebar.title('Navigare')

col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", "2 °C", "1.2 °C")
col2.metric("Vant", "3 Kmph", "-8%")
col3.metric("Umiditate", "86%", "4%")

st.markdown("""
       <style>
       @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');
       .title {
           color: #7FBBE9; /* A modern shade of blue */
           font-family: 'Comic Sans MS', cursive, sans-serif; /* Comic Sans MS with fallbacks */
           font-size: 30px; /* Adjust the size as needed */
           font-weight: 700; /* 700 is for bold text */
           text-align: center; /* Center align for modern aesthetics */
           margin-bottom: 20px; /* Add some space below the title */
       }
       </style>
  
       <h1 class='title'>Vanzarile actualizate si statistici viitoare</h1>
       """, unsafe_allow_html=True)

st.divider()  # 👈 Draws a horizontal rule

# sectiune lucrari efectuate

tab1, tab2, tab3 = st.tabs(["Vanzari", "Stocuri", "Predictii"])
with tab1:
   st.header("Vanzari luna in curs")
 
with tab2:
   st.header("Stocuri existente")

with tab3:
   st.header("Predictii evolutie piata")


container = st.container(border=True)
container.write(" ")

#Sectiune adaugare 
prompt = st.chat_input("Adauga mesaj/sau valori/comunicari interne")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

st.divider()  # 👈 Draws a horizontal rule

st.write("Vanzarile actuale")

st.divider()  # 👈 Another horizontal rule
#Sectiune meniuri comandate
st.bar_chart({"vanzari": [1, 5, 2, 6, 2, 1]})
with st.expander(f"{prompt}"):
    st.write("Vanzarile per produs specific")
    st.image("https://tomkelcy.com/pic.png")
