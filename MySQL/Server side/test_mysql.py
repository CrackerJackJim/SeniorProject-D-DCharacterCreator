import mysql.connector

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="apiuser",
        password="Ilovemygpu!1",
        database="dnd"
    )
    print("✅ Connected successfully!")
    conn.close()
except mysql.connector.Error as err:
    print("❌ Connection failed:", err)