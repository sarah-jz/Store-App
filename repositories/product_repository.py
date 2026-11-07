from database.db import get_connection


def get_all_products():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT Pcode, Pname, Quantity, Price,
               COALESCE(image, 'default.png'), description
        FROM stock
        ORDER BY Pname
    """)

    products = cur.fetchall()
    con.close()
    return products


def get_product(pcode):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT Pcode, Pname, Quantity, Price,
               COALESCE(image, 'default.png'), description
        FROM stock
        WHERE Pcode=%s
    """, (pcode,))

    product = cur.fetchone()
    con.close()
    return product


def insert_product(pcode, name, qty, price, image, description):
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO stock
        (Pcode, Pname, Quantity, Price, image, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (pcode, name, qty, price, image, description))

    con.commit()
    con.close()


def delete_product(pcode):
    con = get_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM stock WHERE Pcode=%s", (pcode,))

    con.commit()
    con.close()


def update_product_price(pcode, price):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "UPDATE stock SET Price=%s WHERE Pcode=%s",
        (price, pcode)
    )

    con.commit()
    con.close()


def update_product_description(pcode, description):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "UPDATE stock SET description=%s WHERE Pcode=%s",
        (description, pcode)
    )

    con.commit()
    con.close()


def update_stock(pcode, quantity):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "UPDATE stock SET Quantity=%s WHERE Pcode=%s",
        (quantity, pcode)
    )

    con.commit()
    con.close()


def reduce_stock(pcode, quantity):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "UPDATE stock SET Quantity=Quantity-%s WHERE Pcode=%s",
        (quantity, pcode)
    )

    con.commit()
    con.close()


def get_available_stock(pcode):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "SELECT Quantity FROM stock WHERE Pcode=%s",
        (pcode,)
    )

    result = cur.fetchone()
    con.close()

    return result[0] if result else 0


def get_product_with_connection(con, pcode):
    cur = con.cursor()

    cur.execute("""
        SELECT Pcode, Pname, Quantity, Price
        FROM stock
        WHERE Pcode=%s
        FOR UPDATE
    """, (pcode,))

    product = cur.fetchone()
    cur.close()

    return product


def reduce_stock_with_connection(con, pcode, quantity):
    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET Quantity=Quantity-%s
        WHERE Pcode=%s AND Quantity >= %s
    """, (quantity, pcode, quantity))

    affected_rows = cur.rowcount
    cur.close()

    return affected_rows