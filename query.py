import pandas as pd
from connect_db import conn_db


def query_series(title: str) -> dict:
    """Queries for one TV series based on title form the series table in postgreSQL

    Args:
        title (str): title of the series

    Returns:
        RealDictRow: the row of the specified series as dict
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

    return row


def query_parents_guide(s_id: str) -> dict:
    """_summary_

    Args:
        s_id (str): series id (retrieved from series table)

    Returns:
        dict: _description_
    """

    sql_query = """
        SELECT * FROM series
        WHERE title = %s;
    """

    conn, cur = conn_db()
    cur.execute(sql_query, (s_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row


if __name__ == "__main__":
    print(query_series("Game of Thrones"))
