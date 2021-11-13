import sqlite3
import random

if __name__ == "__main__":
    # Connecting to db file
    db = sqlite3.connect('my_database.db')
    # Opening cursor
    cur = db.cursor()
    # Creating table 'test' if doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS test (
            id INTEGER PRIMARY KEY, string TEXT, number INTEGER
        )
    """)
    # Inserting new row
    cur.execute("INSERT INTO test (string, number) VALUES ('one', {})".format(random.randint(0, 100)))
    # Committing to DB
    db.commit()
    # Printing out the contents of the table 'test'
    for row in cur.execute("SELECT * FROM test"):
        print(row)
    db.close()
