import streamlit as st
import pandas as pd

#custom background for the sidebar 

page_bg_img= """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://as1.ftcdn.net/v2/jpg/02/83/52/90/1000_F_283529087_B8MDUrb18jy5m0OaKpWWXjtY5UhJZ3cb.jpg');
    background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

#itt hívom be az adatokat, ehelyett kell majd függvény queryvel
filepath_1 = "C:/progos_cuccok/prog2/c_4/series.csv"
series = pd.read_csv(filepath_1)

filepath_2 ="C:/progos_cuccok/prog2/c_4/episodes.csv"
adatok = pd.read_csv(filepath_2)

filepath_3 ="C:/progos_cuccok/prog2/c_4/episode-kws.csv"
episode_kw = pd.read_csv(filepath_3)

filepath_4 ="C:/progos_cuccok/prog2/c_4/parental-guides.csv"
parental_guide = pd.read_csv(filepath_4)

title = "Series, parental guide tags and episode keywords"
header = "To get strated please choose a series!"
st.title(title)

#itt kiválasztod a sorozatot
series_list = series["title"].tolist()
valasztott_sorozat = st.selectbox(header, series_list)

st.write("You selected", valasztott_sorozat, '. Lets see, how this series looks in the parental guide categories!')

filetered_row = series[series['title'] == valasztott_sorozat]
imdb_score = filetered_row['rating'].iloc[0]

st.write("The Imdb score for this series is ", imdb_score)

#sorozat nevéből visszakeresi a kódot
result = series[series['title'] == valasztott_sorozat]

# Check if any rows match the known name
if not result.empty:
    # Extract the code from the result (assuming there's only one match)
    sorozat_kodja = result.iloc[0]['t']
else:
    print(f"No code found for {valasztott_sorozat}")

# kikeresni a parental giude categóriákat ----

# Filter DataFrame based on the keyword in the 't' column
filtered_df = parental_guide[parental_guide['t'] == sorozat_kodja]

# Select the 'cat' and 'level' columns for the filtered rows
result_table = filtered_df[['cat', 'level']]
result_table = result_table.rename(columns={"cat":"Parental guide warning", "level":"Severity"})
# Print the resulting table
st.table(data=result_table)

#epizódok kiválasztása és kw-k listázása
st.write ("If you now choose an episode, you will see the keywords, so you will get further insights to the triggers and themes the episode contains.")

episode_names_list =adatok.loc[adatok['t'] == sorozat_kodja, 'episode_title'].tolist()
valasztott_epizod = st.selectbox(header, episode_names_list, key = "episode")
text_header="Keywords for " + valasztott_epizod + ":"
st.header( text_header )

result_2 = adatok[adatok['episode_title'] == valasztott_epizod]

# Check if any rows match the known name
if not result.empty:
    # Extract the code from the result (assuming there's only one match)
    epizod_kodja = result_2.iloc[0]['episode_tt']
else:
    print(f"No code found for {valasztott_sorozat}")


#make a list from all the keywords for the episode
kw_valasztott_epizod =episode_kw.loc[episode_kw['episode_tt'] == epizod_kodja, 'kw'].tolist()
kw_valasztott_epizod=sorted(kw_valasztott_epizod)

for item in kw_valasztott_epizod:
    st.write(item)

#github dokumntációra mutató link png-re aggatva
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")
st.write("\n")

col1, col2 = st.columns(2)

website_url = "https://github.com/soaei/soaei.github.io"
image_url= "https://cdn4.iconfinder.com/data/icons/iconsimple-logotypes/512/github-512.png"
image_width = 30
with col2:
    st.markdown(f'<a href="{website_url}"><img src="{image_url}" width="{image_width}"></a>', unsafe_allow_html=True)
with col1:
    st.write("You can find the documentation here:")
