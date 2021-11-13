import sqlite3
import random

if __name__ == "__main__":
    print(f'Connecting to file: my_database.db')
    db = sqlite3.connect('my_database.db')
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test (
            id INTEGER PRIMARY KEY, string TEXT, number INTEGER
        )
    """)
    print("Inserting row")
    cur.execute("INSERT INTO test (string, number) VALUES ('one', {})".format(random.randint(0, 100)))
    print("Committing to db")
    db.commit()
    for row in cur.execute("SELECT * FROM test"):
        print(row)
    db.close()
