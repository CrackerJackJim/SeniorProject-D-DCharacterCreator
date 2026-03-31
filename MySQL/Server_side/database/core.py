import pymysql
import threading
from queue import Queue
import asyncio

DB_HOST = "localhost"
DB_USER = "apiuser"
DB_PASSWORD = "Ilovemygpu!1"
DB_NAME = "dnd"

# ------------------------------------------------------------
# SIMPLE THREAD-SAFE CONNECTION POOL
# ------------------------------------------------------------
POOL_SIZE = 10
_pool_lock = threading.Lock()
_connection_pool = Queue(maxsize=POOL_SIZE)


def _create_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# Pre-fill the pool
for _ in range(POOL_SIZE):
    _connection_pool.put(_create_connection())


def get_db():
    """Get a pooled connection."""
    conn = _connection_pool.get()
    try:
        conn.ping(reconnect=True)
    except Exception:
        conn = _create_connection()
    return conn


def release_db(conn):
    """Return connection to the pool."""
    _connection_pool.put(conn)


# ------------------------------------------------------------
# ASYNC QUERY HELPERS
# ------------------------------------------------------------
async def fetch_one(query, params=None):
    def run():
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        finally:
            release_db(conn)

    return await asyncio.to_thread(run)


async def fetch_all(query, params=None):
    def run():
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            release_db(conn)

    return await asyncio.to_thread(run)


async def execute(query, params=None):
    def run():
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                last_id = cursor.lastrowid
            conn.commit()
            return last_id

        except Exception as e:
            print("\n" + "="*80)
            print("SQL EXECUTION ERROR")
            print("Error:", e)
            print("Query:")
            print(query)
            print("Params:", params)
            print("="*80 + "\n")
            raise  # <-- IMPORTANT: propagate error

        finally:
            release_db(conn)

    return await asyncio.to_thread(run)