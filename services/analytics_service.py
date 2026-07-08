from database.db import get_connection


def get_dashboard_data():

    con = get_connection()

    cur = con.cursor()

    cur.execute("""

        SELECT SUM(Quantity*Price)

        FROM stock

    """)

    total_inventory = cur.fetchone()[0] or 0

    cur.execute("""

        SELECT SUM(total_price)

        FROM orders

    """)

    revenue = cur.fetchone()[0] or 0

    cur.execute("""

        SELECT COUNT(*)

        FROM orders

    """)

    orders = cur.fetchone()[0]

    con.close()

    return {

        "inventory":total_inventory,

        "revenue":revenue,

        "orders":orders

    }