
import os
from pathlib import Path

import mysql.connector
from config import Config


def get_connection():

    # Use TiDB when deployed on Render
    if os.getenv("USE_TIDB", "").lower() == "true":

        project_root = Path(__file__).resolve().parent.parent

        ca_path = project_root / os.getenv(
            "TIDB_SSL_CA", "ca.pem"
        )

        return mysql.connector.connect(
            host=os.getenv("TIDB_HOST"),
            port=int(os.getenv("TIDB_PORT", "4000")),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            database="project_computer",
            ssl_ca=str(ca_path),
            ssl_verify_cert=True
        )

    # Otherwise, use your existing local MySQL database
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )
