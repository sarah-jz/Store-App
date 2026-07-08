from database.db import get_connection
from flask_bcrypt import check_password_hash


def get_user(username):

    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        SELECT id, username, password, role
        FROM users
        WHERE username=%s
    """, (username,))

    user = cur.fetchone()

    con.close()

    return user


def verify_user(username, password):

    user = get_user(username)

    if not user:
        return None

    stored_password = user[2]

    # Supports both old plaintext passwords and bcrypt hashes
    if stored_password.startswith("$2b$") or stored_password.startswith("$2a$"):
        if check_password_hash(stored_password, password):
            return user
    else:
        if stored_password == password:
            return user

    return None