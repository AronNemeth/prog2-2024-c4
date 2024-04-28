import pandas as pd
from connect_db import conn_db


# TODO ezt átírni, hogy csak unique-okat adjon vissza
# VAGY legyen benne a series_id is -> nem kell még egy query fv -> és az alapján lehet query-zni
def pivot_cat_severity() -> pd.DataFrame:
    """Queries the entire parents_guides table to enable dynamic dropdowns
       Performs pivot on the table, so that values in cat become columns
       Cell values are values in level

    Returns:
        pd.DataFrame: Columns are unique values in cat and values are unique values in level
    """

    sql_query = """
        SELECT
            series_id,
            MAX(CASE WHEN cat = 'Alcohol, Drugs & Smoking' THEN level END) AS alcohol,
            MAX(CASE WHEN cat = 'Frightening & Intense Scenes' THEN level END) AS fright,
            MAX(CASE WHEN cat = 'Profanity' THEN level END) AS profanity,
            MAX(CASE WHEN cat = 'Sex & Nudity' THEN level END) AS sex,
            MAX(CASE WHEN cat = 'Violence & Gore' THEN level END) AS violence
        FROM parents_guides
        GROUP BY series_id;
    """

    conn, cur = conn_db()
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(rows)

    return df


# Zseni ötlet -> ennek az outputját el lehet menteni s3-ban egy külön fájlként -> ha van már ilyen, nem kell még egyszer megcsinálni a query-t?
# TODO sqllel megoldani, hogy csak random visszadjon egyet
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

    # Add to filters if param is not "All"
    filters = {}
    if alcohol != "All":
        filters["Alcohol, Drugs & Smoking"] = alcohol
    if fright != "All":
        filters["Frightening & Intense Scenes"] = fright
    if profanity != "All":
        filters["Profanity"] = profanity
    if sex != "All":
        filters["Sex & Nudity"] = sex
    if violence != "All":
        filters["Violence & Gore"] = violence

    filtered_df = df
    for col, val in filters.items():
        filtered_df = filtered_df[filtered_df[col] == val]

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
    print(pivot_cat_severity())
