
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

from database.db import get_connection

load_dotenv()

ca_path = Path(__file__).resolve().parent / os.getenv(
    "TIDB_SSL_CA", "ca.pem"
)

tidb = mysql.connector.connect(
    host=os.getenv("TIDB_HOST"),
    port=int(os.getenv("TIDB_PORT", "4000")),
    user=os.getenv("TIDB_USER"),
    password=os.getenv("TIDB_PASSWORD"),
    database="project_computer",
    ssl_ca=str(ca_path),
    ssl_verify_cert=True,
    autocommit=True
)

table_definitions = {
    "users": """
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(100) DEFAULT NULL,
            password VARCHAR(255) DEFAULT NULL,
            role VARCHAR(50) DEFAULT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,

    "stock": """
        CREATE TABLE IF NOT EXISTS stock (
            Pcode INT NOT NULL,
            Pname VARCHAR(25) NOT NULL,
            Quantity INT NOT NULL,
            Price INT NOT NULL,
            image VARCHAR(255) DEFAULT NULL,
            description TEXT,
            category VARCHAR(100) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,

    "cart": """
        CREATE TABLE IF NOT EXISTS cart (
            id INT NOT NULL AUTO_INCREMENT,
            user VARCHAR(100) DEFAULT NULL,
            pcode INT DEFAULT NULL,
            quantity INT DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,

    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            id INT NOT NULL AUTO_INCREMENT,
            product_code INT DEFAULT NULL,
            quantity INT DEFAULT NULL,
            total_price INT DEFAULT NULL,
            order_date TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            user VARCHAR(100) DEFAULT NULL,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
}

source = None
target_cursor = None
source_cursor = None

try:
    source = get_connection()
    source_cursor = source.cursor()
    target_cursor = tidb.cursor()

    print("Creating application tables in TiDB...")

    for table, definition in table_definitions.items():
        target_cursor.execute(definition)
        print(f"Table ready: {table}")

    for table in table_definitions:
        target_cursor.execute(
            f"SELECT COUNT(*) FROM `{table}`"
        )
        count = target_cursor.fetchone()[0]

        if count != 0:
            raise RuntimeError(
                f"TiDB table '{table}' already contains "
                f"{count} records. Migration stopped."
            )

    print("\nStarting data migration...\n")

    # Begin one transaction for all copied records.
    tidb.start_transaction()

    for table in table_definitions:
        source_cursor.execute(f"SELECT * FROM `{table}`")
        rows = source_cursor.fetchall()

        columns = [
            description[0]
            for description in source_cursor.description
        ]

        if rows:
            column_names = ", ".join(
                f"`{column}`" for column in columns
            )
            placeholders = ", ".join(
                ["%s"] * len(columns)
            )

            insert_query = (
                f"INSERT INTO `{table}` "
                f"({column_names}) "
                f"VALUES ({placeholders})"
            )

            target_cursor.executemany(insert_query, rows)

        print(f"{table}: copied {len(rows)} records")

    tidb.commit()

    print("\nMigration completed successfully!")
    print("\nVerifying TiDB record counts:")

    for table in table_definitions:
        target_cursor.execute(
            f"SELECT COUNT(*) FROM `{table}`"
        )
        count = target_cursor.fetchone()[0]
        print(f"{table}: {count} records")

except Exception as error:
    tidb.rollback()
    print("\nMigration failed:")
    print(error)

finally:
    if source_cursor:
        source_cursor.close()

    if source:
        source.close()

    if target_cursor:
        target_cursor.close()

    tidb.close()
