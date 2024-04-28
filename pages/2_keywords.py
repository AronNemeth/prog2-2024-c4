import streamlit as st
import queries as q


st.set_page_config(page_title="IMDB parents guide", layout="wide")
st.title("Check keywords")
"st.session_state object:", st.session_state


titles_dict = q.get_titles()
# st.session_state["seasons"] = ["Please select a series first"]
# episodes = ["Please select a season first"]

with st.expander("Display", expanded=True):

    ser_choice = st.selectbox("Please select a series", options=titles_dict.keys())

    # Update session state variables
    st.session_state["seas_eps"] = q.get_seasons_episodes(titles_dict[ser_choice])
    st.session_state["seasons"] = st.session_state["seas_eps"]["season"].unique()

    sea_choice = st.selectbox(
        "Please select a season", options=st.session_state["seasons"]
    )

    # Update session state variables
    st.session_state["ep_titles"] = st.session_state["seas_eps"]["episode_title"]

    ep_choice = st.selectbox(
        "Please select an epidose", options=st.session_state["ep_titles"]
    )


if st.button("Display keywords"):
    ep_id = (
        st.session_state["seas_eps"]
        .loc[st.session_state["seas_eps"]["episode_title"] == ep_choice, "episode_id"]
        .iloc[0]
    )
    ep_id
    kws = q.get_keywords(ep_id)

    # TODO itt még lehet szépíteni
    # st.text_area("Keywords:", value=kws)
    num_columns = 3

    # Calculate the number of rows required
    num_rows = -(-len(kws) // num_columns)  # Ceiling division to get the next integer

    # Create a list to store the strings for each column
    columns = [kws[i * num_rows : (i + 1) * num_rows] for i in range(num_columns)]

    # Display the strings in multiple columns
    st.write("Contents of the long list:")
    for row in zip(*columns):
        st.write(row)
