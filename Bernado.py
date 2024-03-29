import random
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#######################################
# PAGE SETUP
#######################################


st.set_page_config(page_title="Vanzari Dashboard", page_icon=":bar_chart:", layout="wide")
st.header(':blue[Dashboard Vanzari Brenado SRL]', divider='rainbow')

st.markdown("Prototip aplicatie")

with st.sidebar:
    st.header("Configurare")
    
    # Select Box pentru alegerea sursa de date
    data_source = st.selectbox("Alegeți sursa de date:", ["Upload File", "Predefined Data"])

    # Încărcător de fișiere devine activ numai când se alege "Upload File"
    uploaded_file = None
    if data_source == "Upload File":
        uploaded_file = st.file_uploader("Choose a file")
    
    # Afișează mesaj de informare dacă nu este selectată nici o sursă de date
    if data_source == "Predefined Data" and not uploaded_file:
        st.info("Se vor prelucra datele Locale")


#######################################
# DATA LOADING
#######################################

# Definiția listei cu numele lunilor
all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]



@st.cache
def load_data(path_or_buffer):
    if isinstance(path_or_buffer, str):
        # Încărcarea datelor dintr-o cale de fișier
        df = pd.read_excel(path_or_buffer)
    else:
        # Încărcarea datelor dintr-un buffer de fișier încărcat
        df = pd.read_excel(path_or_buffer)
    return df

# Determină sursa datelor și încarcă datele
if uploaded_file is not None:
    df = load_data(uploaded_file)
elif data_source == "Predefined Data":
    df = load_data('./assets/Data1.xlsx')
else:
    st.stop()

#######################################
# VISUALIZATION METHODS
#######################################


def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
            },
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(0, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="#212121",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_gauge(
    indicator_number, indicator_color, indicator_suffix, indicator_title, max_bound
):
    fig = go.Figure(
        go.Indicator(
            value=indicator_number,
            mode="gauge+number",
            domain={"x": [0, 1], "y": [0, 1]},
            number={
                "suffix": indicator_suffix,
                "font.size": 26,
            },
            gauge={
                "axis": {"range": [0, max_bound], "tickwidth": 1},
                "bar": {"color": indicator_color},
            },
            title={
                "text": indicator_title,
                "font": {"size": 28},
            },
        )
    )
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        height=200,
        margin=dict(l=10, r=10, t=50, b=10, pad=8),
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_top_right():
    vanzari_data = duckdb.sql(
        f"""
        WITH vanzari_data AS (
            UNPIVOT ( 
                SELECT 
                    Scenario,
                    depozit_Galicea,
                    {','.join(all_months)} 
                    FROM df 
                    WHERE Year='2023' 
                    AND Account='Vanzari' 
                ) 
            ON {','.join(all_months)}
            INTO
                NAME month
                VALUE vanzari
        ),

        aggregated_vanzari AS (
            SELECT
                Scenario,
                depozit_Galicea,
                SUM(vanzari) AS vanzari
            FROM vanzari_data
            GROUP BY Scenario, depozit_Galicea
        )
        
        SELECT * FROM aggregated_vanzari
        """
    ).df()

    fig = px.bar(
        vanzari_data,
        x="depozit_Galicea",
        y="vanzari",
        color="Scenario",
        barmode="group",
        text_auto=".2s",
        title="Vanzari pentru anul 2023",
        height=400,
    )
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_bottom_left():
    vanzari_data = duckdb.sql(
        f"""
        WITH vanzari_data AS (
            SELECT 
            Scenario,{','.join(all_months)} 
            FROM df 
            WHERE Year='2023' 
            AND Account='Vanzari'
            AND depozit_Galicea='Software'
        )

        UNPIVOT vanzari_data 
        ON {','.join(all_months)}
        INTO
            NAME month
            VALUE vanzari
    """
    ).df()

    fig = px.line(
        vanzari_data,
        x="month",
        y="vanzari",
        color="Scenario",
        markers=True,
        text="vanzari",
        title="Vanzari lunare comparativ cu predictii lunare 2023",
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)


def plot_bottom_right():
    vanzari_data = duckdb.sql(
        f"""
        WITH vanzari_data AS (
            UNPIVOT ( 
                SELECT 
                    Account,Year,{','.join([f'ABS({month}) AS {month}' for month in all_months])}
                    FROM df 
                    WHERE Scenario='Actuals'
                    AND Account!='Vanzari'
                ) 
            ON {','.join(all_months)}
            INTO
                NAME year
                VALUE vanzari
        ),

        aggregated_vanzari AS (
            SELECT
                Account,
                Year,
                SUM(vanzari) AS vanzari
            FROM vanzari_data
            GROUP BY Account, Year
        )
        
        SELECT * FROM aggregated_vanzari
    """
    ).df()

    fig = px.bar(
        vanzari_data,
        x="Year",
        y="vanzari",
        color="Account",
        title="Vanzarile anuale / cont",
    )
    st.plotly_chart(fig, use_container_width=True)


#######################################
# STREAMLIT LAYOUT
#######################################

top_left_column, top_right_column = st.columns((2, 1))
bottom_left_column, bottom_right_column = st.columns(2)

with top_left_column:
    column_1, column_2, column_3, column_4 = st.columns(4)

    with column_1:
        plot_metric(
            "Total Incasari",
            6621280,
            prefix="RON",
            suffix="",
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
        plot_gauge(1.86, "#0068C9", "%", "Rata curenta", 3)

    with column_2:
        plot_metric(
            "Total Plati",
            1630270,
            prefix="RON",
            suffix="",
            show_graph=True,
            color_graph="rgba(255, 43, 43, 0.2)",
        )
        plot_gauge(10, "#FF8700", " zile", "In stoc", 31)

    with column_3:
        plot_metric("Capital", 75.38, prefix="", suffix=" %", show_graph=False)
        plot_gauge(7, "#FF2B2B", " zile", "Fara stocuri", 31)
        
    with column_4:
        plot_metric("Datorii", 1.10, prefix="", suffix=" %", show_graph=False)
        plot_gauge(28, "#29B09D", " zile", "Intarzieri", 31)

with top_right_column:
    plot_top_right()

with bottom_left_column:
    plot_bottom_left()

with bottom_right_column:
    plot_bottom_right()
