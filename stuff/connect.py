import psycopg2
from config import config


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL database version:")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        postgres_insert_query = (
            """ INSERT INTO customers (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
        )
        record_to_insert = (5, "One Plus 6", 950)
        cur.execute("SELECT version()")
        cur.execute(
            "CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, model VARCHAR(255), price INT)"
        )
        print("executed")

        cur.execute(postgres_insert_query, record_to_insert)

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    connect()
