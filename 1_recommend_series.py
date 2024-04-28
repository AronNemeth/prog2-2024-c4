import streamlit as st
import pandas as pd
import queries as q
import visualization as v

# TODO normális elrendezés a dropdownoknak
st.set_page_config(page_title="IMDB parents guide", layout="wide")
st.title("TV series recommendation")
"st.session_state object:", st.session_state


# TODO kicsit bugos a dynamic dropdown, mintha nem szelektálná a többi dropdown kategóriát, amikor beállítom a frighteninget (moderate fright, moderate prof -> no options to select)
# TODO miért van None és NaN is a Fright opciók között
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

    sex = st.selectbox(
        "Sex & Nudity",
        options=sex_options,
        on_change=update_df,
        kwargs={"df": df},
        key="sex",
    )
    fright = st.selectbox(
        "Frightening & Intense Scenes",
        options=fright_options,
        on_change=update_df,
        kwargs={"df": df},
        key="fright",
    )
    profanity = st.selectbox(
        "Profanity",
        options=profanity_options,
        on_change=update_df,
        kwargs={"df": df},
        key="profanity",
    )
    alcohol = st.selectbox(
        "Alcohol, Drugs & Smoking",
        options=alcohol_options,
        on_change=update_df,
        kwargs={"df": df},
        key="alcohol",
    )
    violence = st.selectbox(
        "Violence & Gore",
        options=violence_options,
        on_change=update_df,
        kwargs={"df": df},
        key="violence",
    )

    st.write(df.astype("object"))


if st.button("Show charts"):

    n_series = len(df)

    if n_series == 1:
        pass  # TODO a sima chartot még megírni
    elif n_series > 1 and n_series < 6:
        bar1, bar2 = v.bar_charts(tuple(df.iloc[:, 0]))
        st.write(bar1, bar2)
    else:
        scatter = v.scatter_plot(tuple(df.iloc[:, 0]))
        st.write(scatter)
