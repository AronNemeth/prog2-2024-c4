import pandas as pd
from connect_db import conn_rds_db


def pivot_cat_severity() -> pd.DataFrame:
    """Enables dynamic dropdowns
       Pivots the parents_guides table, categories in cat become columns

    Returns:
        pd.DataFrame: pivoted parents_guide without duplicates
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

    conn, cur = conn_rds_db()
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(rows)

    return df


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

    conn, cur = conn_rds_db()
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

    return filtered_df.sample(n=1)


def q_series(series_ids: tuple):
    """Queries for TV series based on series_ids

    Args:
        series_id (tuple): series_ids

    Returns:
        pd.DataFrame: rows are series
    """

    # Only one str in a tuple is unpacked from it
    if isinstance(series_ids, str):
        sql_query = """
            SELECT * FROM series
            WHERE series_id = %s;
        """

        conn, cur = conn_rds_db()
        cur.execute(sql_query, (series_ids,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        return pd.DataFrame([row])

    else:
        sql_query = """
            SELECT * FROM series
            WHERE series_id IN %s;
        """

        conn, cur = conn_rds_db()
        cur.execute(sql_query, (series_ids,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return pd.DataFrame(rows)


def get_titles() -> dict:
    """_summary_

    Returns:
        dict: keys: title, values: series_id
    """

    conn, cur = conn_rds_db()
    cur.execute("SELECT title, series_id FROM series")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {item["title"]: item["series_id"] for item in rows}


def get_seasons_episodes(series_id: str) -> pd.DataFrame:

    conn, cur = conn_rds_db()
    cur.execute(
        "SELECT season, episode_title, episode_id FROM episodes WHERE series_id = %s",
        (series_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return pd.DataFrame(rows)


def get_keywords(ep_id: str):

    conn, cur = conn_rds_db()
    cur.execute("SELECT kw FROM episode_kws WHERE episode_id = %s", (ep_id,))
    kws = cur.fetchall()
    cur.close()
    conn.close()

    return [dict_["kw"] for dict_ in kws]


if __name__ == "__main__":
    print(get_keywords("tt1668746"))
