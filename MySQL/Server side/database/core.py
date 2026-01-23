import pymysql

DB_HOST = "localhost"
DB_USER = "apiuser"
DB_PASSWORD = "Ilovemygpu!1"
DB_NAME = "dnd"

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_one(query, params=None):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
    finally:
        conn.close()

def fetch_all(query, params=None):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute(query, params=None):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    finally:
        conn.close()