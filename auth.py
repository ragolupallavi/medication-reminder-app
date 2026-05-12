import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(conn, username, password, email):
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email)
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


def login_user(conn, username, password):
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )

    return cursor.fetchone()