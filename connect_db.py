import psycopg2
import os
from dotenv import load_dotenv


def connect_to_database():
    """Connects to a postgreSQL DB with configuarations specified as environmental variables

    Returns:
        connection: represents a connection to a postgreSQL DB (dtype: class)
        cursor: used to interact with a DB, allows to execute SQL commands (dtype: class)
    """

    load_dotenv()

    try:
        connection = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            database=os.getenv("DATABASE"),
        )

        cursor = connection.cursor()

        return connection, cursor

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return None, None


def close_connection(connection, cursor):
    """Closes the connection and the cursor

    Returns:
    """
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


if __name__ == "__main__":
    connection, cursor = connect_to_database()
    if connection:
        close_connection(connection, cursor)
