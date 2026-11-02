from database.db import get_connection


# ---------------- ADD ITEM ---------------- #

def add_item(username, pcode, quantity):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        INSERT INTO cart
        (
            user,
            pcode,
            quantity
        )
        VALUES
        (
            %s,
            %s,
            %s
        )
    """,
    (
        username,
        pcode,
        quantity
    ))

    con.commit()
    con.close()


# ---------------- GET USER CART ---------------- #

def get_cart(username):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT
            stock.Pcode,
            stock.Pname,
            cart.quantity,
            stock.Price,
            COALESCE(stock.image,'default.png')
        FROM cart

        JOIN stock

        ON cart.pcode = stock.Pcode

        WHERE cart.user=%s

        ORDER BY cart.id DESC
    """, (username,))

    items = cur.fetchall()

    con.close()

    return items


# ---------------- DELETE USER CART ---------------- #

def clear_cart(username):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        DELETE
        FROM cart
        WHERE user=%s
    """, (username,))

    con.commit()
    con.close()


# ---------------- DELETE SINGLE ITEM ---------------- #

def remove_item(username, pcode):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        DELETE
        FROM cart
        WHERE
            user=%s
        AND
            pcode=%s
    """,
    (
        username,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- UPDATE QUANTITY ---------------- #

def update_quantity(username, pcode, quantity):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE cart

        SET quantity=%s

        WHERE
            user=%s
        AND
            pcode=%s
    """,
    (
        quantity,
        username,
        pcode
    ))

    con.commit()
    con.close()


# ---------------- CHECK IF ITEM EXISTS ---------------- #

def item_exists(username, pcode):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT quantity
        FROM cart
        WHERE
            user=%s
        AND
            pcode=%s
    """,
    (
        username,
        pcode
    ))

    result = cur.fetchone()

    con.close()

    return result


# ---------------- INCREASE QUANTITY ---------------- #

def increase_quantity(username, pcode, quantity):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        UPDATE cart

        SET quantity = quantity + %s

        WHERE
            user=%s
        AND
            pcode=%s
    """,
    (
        quantity,
        username,
        pcode
    ))

    con.commit()
    con.close()

# ---------------- GET CART USING EXISTING CONNECTION ---------------- #

def get_cart_with_connection(con, username):

    cur = con.cursor()

    cur.execute("""
        SELECT pcode, quantity
        FROM cart
        WHERE user=%s
        FOR UPDATE
    """, (username,))

    items = cur.fetchall()

    cur.close()

    return items


# ---------------- CLEAR CART USING EXISTING CONNECTION ---------------- #

def clear_cart_with_connection(con, username):

    cur = con.cursor()

    cur.execute("""
        DELETE FROM cart
        WHERE user=%s
    """, (username,))

    cur.close()