import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv


def conn_db():
    """Connects to a postgreSQL DB with configurations specified as environmental variables
    Cursor is set to return rows as dictionaries

    Returns:
        conn: represents a connection to a postgreSQL DB (dtype: class)
        cur: used to interact with a DB, allows to execute SQL commands (dtype: class)
    """

    load_dotenv()

    try:
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
        )

        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        return conn, cur

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None, None


if __name__ == "__main__":
    conn, cur = conn_db()
    if conn:
        cur.close()
        conn.close()
