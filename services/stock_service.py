from db import get_connection

def get_all_stock():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM stock")
    data = cur.fetchall()
    con.close()
    return data


def add_product(pcode, name, qty, price):
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO stock VALUES (%s,%s,%s,%s)",
        (pcode, name, qty, price)
    )

    con.commit()
    con.close()