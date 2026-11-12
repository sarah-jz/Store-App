
from database.db import get_connection

con = get_connection()

try:
    cursor = con.cursor()

    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        print("\n" + "=" * 60)
        print(f"TABLE: {table}")
        print("=" * 60)

        # Display table structure
        cursor.execute(f"SHOW CREATE TABLE `{table}`")
        result = cursor.fetchone()
        print(result[1])

        # Display number of records
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        print(f"\nNumber of records: {count}")

    cursor.close()

finally:
    con.close()
