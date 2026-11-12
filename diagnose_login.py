
from getpass import getpass

from database.db import get_connection
from services.auth_service import verify_user

username = input("Enter your username: ").strip()
password = getpass("Enter your password: ")

print("\nChecking TiDB user record...")

con = get_connection()

try:
    cur = con.cursor()

    cur.execute("""
        SELECT username, password, role
        FROM users
        WHERE username = %s
    """, (username,))

    user = cur.fetchone()

    if user:
        print("User found: YES")
        print("Role:", user[2])
        print("Password hash prefix:", user[1][:4])
        print("Password hash length:", len(user[1]))
    else:
        print("User found: NO")

    cur.close()

finally:
    con.close()

print("\nTesting authentication service...")

result = verify_user(username, password)

if result:
    print("Authentication successful!")
    print("Returned user ID:", result[0])
    print("Returned role:", result[3])
else:
    print("Authentication failed.")
