import pandas as pd


def add_medication(conn, user_id, name, dosage, time):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO medications (user_id, name, dosage, time) VALUES (?, ?, ?, ?)",
        (user_id, name, dosage, time)
    )
    conn.commit()


def get_all_medications(conn, user_id):
    return pd.read_sql(
        "SELECT * FROM medications WHERE user_id=?",
        conn,
        params=(user_id,)
    )


def delete_medication(conn, med_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medications WHERE id=?", (med_id,))
    conn.commit()


def mark_as_taken(conn, med_id):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE medications SET status='Taken' WHERE id=?",
        (med_id,)
    )
    conn.commit()