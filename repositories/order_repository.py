from database.db import get_connection
def create_order_with_connection(con, user, product_code, quantity, total_price):
    cur = con.cursor()

    cur.execute("""
        INSERT INTO orders
        (user, product_code, quantity, total_price)
        VALUES (%s, %s, %s, %s)
    """, (user, product_code, quantity, total_price))

    cur.close()

# ============================
# CREATE ORDER
# ============================

def create_order(user, product_code, quantity, total_price):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO orders
        (
            user,
            product_code,
            quantity,
            total_price
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
    """,
    (
        user,
        product_code,
        quantity,
        total_price
    ))

    con.commit()
    con.close()


# ============================
# GET USER ORDERS
# ============================

def get_orders_by_user(user):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT

            o.id,

            s.Pname,

            o.quantity,

            o.total_price,

            o.order_date

        FROM orders o

        JOIN stock s

        ON o.product_code = s.Pcode

        WHERE o.user=%s

        ORDER BY o.order_date DESC

    """, (user,))

    orders = cur.fetchall()

    con.close()

    return orders


# ============================
# TOTAL SPENT
# ============================

def get_total_spent(user):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            SUM(total_price)
        FROM orders
        WHERE user=%s
    """, (user,))

    total = cur.fetchone()[0]

    con.close()

    return total or 0


# ============================
# TOTAL REVENUE
# ============================

def get_total_revenue():

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            SUM(total_price)
        FROM orders
    """)

    revenue = cur.fetchone()[0]

    con.close()

    return revenue or 0


# ============================
# TOTAL ORDERS
# ============================

def get_total_orders():

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM orders
    """)

    total = cur.fetchone()[0]

    con.close()

    return total


# ============================
# TOP SELLING PRODUCTS
# ============================

def get_top_products():

    con = get_connection()
    cur = con.cursor()

    cur.execute("""

        SELECT

            s.Pname,

            SUM(o.quantity)

        FROM orders o

        JOIN stock s

        ON o.product_code=s.Pcode

        GROUP BY s.Pname

        ORDER BY SUM(o.quantity) DESC

        LIMIT 5

    """)

    products = cur.fetchall()

    con.close()

    return products