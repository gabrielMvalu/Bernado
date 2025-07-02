import streamlit as st

# Configurare pagină
st.set_page_config(
    page_title="BrenadoForHouse",
    page_icon="🏠",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🏠 BrenadoForHouse")
    st.caption("Segmentul rezidențial")

# Header
st.title("🏠 BrenadoForHouse")
st.subheader("Dashboard pentru segmentul rezidențial")

st.markdown("---")

# Selectare locație
st.subheader("📍 Selectează Locația")
location = st.selectbox(
    "Alege depozitul/showroom:",
    ["Showroom Galicea", "Depozit Grele Galicea", "Depozit 3"]
)

st.markdown(f"### 📊 Date pentru: **{location}**")

# Metrici pentru locația selectată
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Vânzări Totale", "Loading...", "")
with col2:
    st.metric("Stoc Disponibil", "Loading...", "")
with col3:
    st.metric("Clienți Luna", "Loading...", "")
with col4:
    st.metric("Valoare Medie", "Loading...", "")

st.markdown("---")

# Tabs pentru diferite secțiuni
tab1, tab2, tab3 = st.tabs(["📈 Vânzări", "📦 Stocuri", "👥 Clienți"])

with tab1:
    st.subheader(f"📈 Vânzări - {location}")
    st.info("Grafice vânzări vor fi adăugate aici")

with tab2:
    st.subheader(f"📦 Stocuri - {location}")
    st.info("Date stocuri vor fi adăugate aici")

with tab3:
    st.subheader(f"👥 Clienți - {location}")
    st.info("Analiza clienți va fi adăugată aici")
