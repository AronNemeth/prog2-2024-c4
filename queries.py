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


def pivot_cat_severity():

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


def q_parents_guide(s_id: str):
    """Queries for rows in parents_guide table based in series id

    Args:
        s_id (str): series id (retrieved from series table)

    Returns:
        pd.DataFrame: a df with 5 rows (or 4 for one series)
    """

    sql_query = """
        SELECT * FROM parents_guides
        WHERE series_id = %s;
    """

    conn, cur = conn_db()
    cur.execute(sql_query, (s_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(rows)

    return df


if __name__ == "__main__":
    print(pivot_cat_severity())
