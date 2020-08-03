import sqlite3


conn = sqlite3.connect("cards.db")
cursor = conn.cursor()

with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM cards")
    rows = cur.fetchall()

    for row in rows:
        print(*row)
input('Нажмите любую клавишу чтобы выйти...')