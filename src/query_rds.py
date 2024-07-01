
import psycopg2


def get_db():
    cur = ''
    conn = psycopg2.connect(database="tst",
                            user="postrgres",
                            password="postgres",
                            host="localhost", port="5432"
                            )

    if conn:
        print('connected')
        cur = conn.cursor()
    return cur


get_db()