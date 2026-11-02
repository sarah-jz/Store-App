from database.db import get_connection


# ---------------- GET ALL PRODUCTS ---------------- #

def get_all_products():

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            Pcode,
            Pname,
            Quantity,
            Price,
            COALESCE(image, 'default.png'),
            description
        FROM stock
        ORDER BY Pname
    """)

    products = cur.fetchall()

    con.close()

    return products


# ---------------- GET SINGLE PRODUCT ---------------- #

def get_product(pcode):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            Pcode,
            Pname,
            Quantity,
            Price,
            COALESCE(image, 'default.png'),
            description
        FROM stock
        WHERE Pcode=%s
    """, (pcode,))

    product = cur.fetchone()

    con.close()

    return product


# ---------------- INSERT PRODUCT ---------------- #

def insert_product(
    pcode,
    name,
    qty,
    price,
    image,
    description
):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO stock
        (
            Pcode,
            Pname,
            Quantity,
            Price,
            image,
            description
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """,
    (
        pcode,
        name,
        qty,
        price,
        image,
        description
    ))

    con.commit()
    con.close()


# ---------------- DELETE PRODUCT ---------------- #

def delete_product(pcode):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        DELETE
        FROM stock
        WHERE Pcode=%s
    """, (pcode,))

    con.commit()
    con.close()


# ---------------- UPDATE PRICE ---------------- #

def update_product_price(
    pcode,
    price
):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET Price=%s
        WHERE Pcode=%s
    """,
    (
        price,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- UPDATE DESCRIPTION ---------------- #

def update_product_description(
    pcode,
    description
):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET description=%s
        WHERE Pcode=%s
    """,
    (
        description,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- UPDATE STOCK ---------------- #

def update_stock(
    pcode,
    quantity
):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET Quantity=%s
        WHERE Pcode=%s
    """,
    (
        quantity,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- REDUCE STOCK ---------------- #

def reduce_stock(
    pcode,
    quantity
):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET Quantity = Quantity - %s
        WHERE Pcode=%s
    """,
    (
        quantity,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- GET AVAILABLE STOCK ---------------- #

def get_available_stock(pcode):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT Quantity
        FROM stock
        WHERE Pcode=%s
    """, (pcode,))

    result = cur.fetchone()

    con.close()

    if result:
        return result[0]

    return 0

# ---------------- GET PRODUCT FOR CHECKOUT ---------------- #

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


# ---------------- REDUCE STOCK USING EXISTING CONNECTION ---------------- #

def reduce_stock_with_connection(con, pcode, quantity):

    cur = con.cursor()

    cur.execute("""
        UPDATE stock
        SET Quantity = Quantity - %s
        WHERE Pcode=%s
        AND Quantity >= %s
    """, (quantity, pcode, quantity))

    affected_rows = cur.rowcount

    cur.close()

    return affected_rows