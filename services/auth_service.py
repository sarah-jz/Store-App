
import bcrypt
from database.db import get_connection


# ---------------- GET USER ---------------- #

def get_user(username):
    con = get_connection()

    try:
        cur = con.cursor()

        cur.execute("""
            SELECT id, username, password, role
            FROM users
            WHERE username = %s
        """, (username,))

        user = cur.fetchone()
        cur.close()

        return user

    finally:
        con.close()


# ---------------- VERIFY LOGIN ---------------- #

def verify_user(username, password):
    user = get_user(username)

    if not user:
        return None

    stored_password = user[2]

    # Check existing bcrypt password hashes
    if stored_password.startswith(("$2b$", "$2a$", "$2y$")):
        try:
            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            ):
                return user
        except ValueError:
            return None

    # Support older plaintext passwords temporarily
    elif stored_password == password:
        return user

    return None


# ---------------- REGISTER CUSTOMER ---------------- #

def register_customer(username, password):

    if not username or not password:
        raise ValueError("Username and password are required.")

    if len(username) < 3:
        raise ValueError("Username must contain at least 3 characters.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    if get_user(username):
        raise ValueError("This username is already taken.")

    # Hash password before storing it
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    con = get_connection()

    try:
        cur = con.cursor()

        cur.execute("""
            INSERT INTO users (username, password, role)
            VALUES (%s, %s, 'customer')
        """, (username, hashed_password))

        con.commit()
        cur.close()

    except Exception:
        con.rollback()
        raise

    finally:
        con.close()
