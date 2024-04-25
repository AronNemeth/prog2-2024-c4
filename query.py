import pandas as pd
from connect_db import conn_db


def query_series(title: str):
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


def query_parents_guide(s_id: str):
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
    print(query_series("Game of Thrones"))
