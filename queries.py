import pandas as pd
from connect_db import conn_db


# Ez nem kell valszeg
def q_series_titles() -> list:
    """Queries the series table for every title

    Returns:
        list: series titles
    """

    conn, cur = conn_db()
    cur.execute("SELECT title FROM series")
    dicts = cur.fetchall()
    cur.close()
    conn.close()

    return [list(d.values())[0] for d in dicts]


# TODO megcsinálni, hogy a None value nan-re legyen átírva
def pivot_cat_severity() -> pd.DataFrame:
    """Queries the entire parents_guides table to enable dynamic dropdowns
       Performs pivot on the table, so that values in cat become columns
       Cell values are values in level

    Returns:
        pd.DataFrame: Columns are unique values in cat and values are unique values in level
    """

    conn, cur = conn_db()
    cur.execute("SELECT * FROM parents_guides")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(rows)

    pivot_df = df.pivot(index="series_id", columns="cat", values="level")
    pivot_df.reset_index(inplace=True)
    pivot_df = pivot_df.rename(
        columns={
            "Alcohol, Drugs & Smoking": "alcohol",
            "Frightening & Intense Scenes": "fright",
            "Profanity": "profanity",
            "Sex & Nudity": "sex",
            "Violence & Gore": "violence",
        }
    )

    return pivot_df.iloc[:, 1:]


# Zseni ötlet -> ennek az outputját el lehet menteni s3-ban egy külön fájlként -> ha van már ilyen, nem kell még egyszer megcsinálni a query-t?


# TODO sqllel megoldani, hogy csak random visszadjon egyet
# TODO kaphat dropdownból olyat, hogy "all"
def q_pg_series(alcohol, fright, profanity, sex, violence) -> pd.DataFrame:
    """Joins the series and the parents_guides tables
       The categories from the paretns_guides are added as cols to series

    Args:
        alcohol (str): level of Alcohol, Drugs & Smoking smoking
        fright (str): level of Frightening & Intense Scenes
        profanity (str): level of Profanity
        sex (str): level of Sex & Nudity
        violence (str): level of Violence & Gore

    Returns:
        pd.DataFrame: one TV series with the categories from parents_guides joined as columns
    """
    # pyspark: vajon gyorsabb ha sqllel csak lekérem a táblákat és a joint és szűrést pysparkkal csinálom?
    # Simán %%timeittel lemérni

    conn, cur = conn_db()
    cur.execute("SELECT * FROM parents_guides;")
    pg = cur.fetchall()
    cur.execute("SELECT * FROM series;")
    ser = cur.fetchall()
    cur.close()
    conn.close()

    parents_guides = pd.DataFrame(pg)
    series = pd.DataFrame(ser)

    parents_guides = parents_guides.pivot_table(
        index="series_id", columns="cat", values="level", aggfunc="first"
    )

    df = pd.merge(series, parents_guides, on="series_id", how="left")

    filtered_df = df[
        (df["Alcohol, Drugs & Smoking"] == alcohol)
        & (df["Frightening & Intense Scenes"] == fright)
        & (df["Profanity"] == profanity)
        & (df["Sex & Nudity"] == sex)
        & (df["Violence & Gore"] == violence)
    ]

    if len(filtered_df) > 0:
        return filtered_df.sample(n=1)
    else:  # TODO Ezt majd ki lehet venni, ha megbízható a dynamic dropdown
        return "I can't get no satisfaction"


def q_series(title: str):
    """Queries for one TV series based on title form the series table in postgreSQL

    Args:
        title (str): title of the series

    Returns:
        pd.DataFrame: a df with one row
    """

    sql_query = """
        SELECT * FROM series
        WHERE title = %s;
    """

    conn, cur = conn_db()
    cur.execute(sql_query, (title,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    df = pd.DataFrame([row])

    return df


if __name__ == "__main__":
    print(
        q_pg_series(
            alcohol="Moderate",
            fright="Severe",
            profanity="Severe",
            sex="Severe",
            violence="Severe",
        )
    )
