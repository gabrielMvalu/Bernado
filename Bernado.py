import streamlit as st

# Configurare pagină
st.set_page_config(
    page_title="BRENADO Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar cu logo
with st.sidebar:
    st.title("🏢 BRENADO")
    st.caption("Multi-Business Dashboard")
    st.markdown("---")

# Pagina principală (Home)
st.title("🏢 BRENADO Dashboard")
st.subheader("Bun venit la sistemul de rapoarte multi-business")

st.markdown("""
## 📊 Companiile BRENADO

Folosește meniul din stânga pentru a accesa:

- **🏠 BrenadoForHouse** - Segmentul rezidențial
- **🏗️ BrenadoConstruct** - Segmentul construcții  
- **⚙️ BrenadoSteel** - Segmentul oțel și metale
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "🟢 Online")
with col2:
    st.metric("Pagini", "3")
with col3:
    st.metric("Update", "Live")

st.info("💡 Selectează o companie din meniul lateral pentru a vedea rapoartele.")
