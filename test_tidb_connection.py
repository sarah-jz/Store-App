
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    connection = mysql.connector.connect(
        host=os.getenv("TIDB_HOST"),
        port=int(os.getenv("TIDB_PORT", "4000")),
        user=os.getenv("TIDB_USER"),
        password=os.getenv("TIDB_PASSWORD"),
        database="project_computer",
        ssl_ca=os.getenv("TIDB_SSL_CA"),
        ssl_verify_cert=True
    )

    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")

    print("TiDB connection successful!")
    print("Database version:", cursor.fetchone()[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Connection failed:")
    print(error)
