import streamlit as st
import queries as q


st.set_page_config(page_title="IMDB parents guide", layout="wide")
st.title("Check keywords")
"st.session_state object:", st.session_state


titles_dict = q.get_titles()
seasons = ["Please select a series first"]
episodes = ["Please select a season first"]

seasons_episodes = st.session_state.get(seasons_episodes=None)

with st.expander("Display", expanded=True):

    # TODO on_change callbackkel meg lehet csinálni
    ser_choice = st.selectbox("Please select a series", options=titles_dict.keys())

    if st.button("Query seasons"):
        seasons_episodes = q.get_seasons_episodes(titles_dict[ser_choice])
        seasons = seasons_episodes["season"].unique()
        st.write(seasons_episodes.astype("object"))

    sea_choice = st.selectbox("Please select a season", options=seasons)

    if st.button("Query episodes"):
        episodes = seasons_episodes["episode_title"]
        st.write(episodes.astype("object"))

    st.selectbox("Please select an epidose", options=episodes)


if st.button("Display keywords"):
    pass
