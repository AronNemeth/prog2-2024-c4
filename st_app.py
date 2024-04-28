import streamlit as st
import pandas as pd
import queries as q

# TODO normális elrendezés a dropdownoknak
st.set_page_config(page_title="IMDB parents guide", layout="wide")
st.title("IMDB parents guide")


# TODO kicsit bugos a dynamic dropdown, mintha nem szelektálná a többi dropdown kategóriát, amikor beállítom a frighteninget (moderate fright, moderate prof -> no options to select)
# TODO miért van None és NaN is a Fright opciók között
# TODO biztos jó a pivot? -> több None value is fright-nál -> ennyi hiányzó nem volt a parents_guide táblában
@st.cache_data
def get_data():
    df = q.pivot_cat_severity()

    return df


# TODO lehet itt van a fent említett bug
def update_df(df: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    sex = st.session_state["sex"]
    fright = st.session_state["fright"]
    profanity = st.session_state["profanity"]
    alcohol = st.session_state["alcohol"]
    violence = st.session_state["violence"]
    if sex != "All":
        df = df.query(f"sex == '{sex}'")
    if fright != "All":
        df = df.query(f"fright == '{fright}'")
    if profanity != "All":
        df = df.query(f"profanity == '{profanity}'")
    if alcohol != "All":
        df = df.query(f"alcohol == '{alcohol}'")
    if violence != "All":
        df = df.query(f"violence == '{violence}'")
    st.session_state["df"] = df
    st.session_state["fresh_data"] = False


df = get_data()


if "df" not in st.session_state:
    st.session_state.df = df
if "fresh_data" not in st.session_state:
    st.session_state.fresh_data = True

with st.expander("Display", expanded=True):
    if st.button("Refresh data"):
        df = q.pivot_cat_severity()
        st.session_state["df"] = df
        st.session_state["fresh_data"] = True

    df = st.session_state["df"]
    col1, col2, col3, col4, col5 = st.columns(5)

    sex_options = df.sex.unique().tolist()
    fright_options = df.fright.unique().tolist()
    profanity_options = df.profanity.unique().tolist()
    alcohol_options = df.alcohol.unique().tolist()
    violence_options = df.violence.unique().tolist()

    # if st.session_state.fresh_data:
    fright_options.insert(0, "All")
    profanity_options.insert(0, "All")
    sex_options.insert(0, "All")
    alcohol_options.insert(0, "All")
    violence_options.insert(0, "All")

    sex = col1.selectbox(
        "Sex & Nudity",
        options=sex_options,
        on_change=update_df,
        kwargs={"df": df},
        key="sex",
    )
    fright = col2.selectbox(
        "Frightening & Intense Scenes",
        options=fright_options,
        on_change=update_df,
        kwargs={"df": df},
        key="fright",
    )
    profanity = col3.selectbox(
        "Profanity",
        options=profanity_options,
        on_change=update_df,
        kwargs={"df": df},
        key="profanity",
    )
    alcohol = col3.selectbox(
        "Alcohol, Drugs & Smoking",
        options=alcohol_options,
        on_change=update_df,
        kwargs={"df": df},
        key="alcohol",
    )
    violence = col3.selectbox(
        "Violence & Gore",
        options=violence_options,
        on_change=update_df,
        kwargs={"df": df},
        key="violence",
    )

    # st.write(df.astype("object"))


if st.button("Query data"):
    series = q.q_pg_series(
        alcohol=alcohol, fright=fright, profanity=profanity, sex=sex, violence=violence
    )

    st.write(series.astype("object"))
