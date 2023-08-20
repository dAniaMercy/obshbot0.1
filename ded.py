import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
userid = 0
def checkconnect():
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test'")
    result = cursor.fetchone()

    if result is not None:
        print("Table 'test' exists in the database.")
    else:
        print("Table 'test' does not exist in the database.")

def db_table_val(user_id: int, user_name: str, username: str, datareg: str):
	cursor.execute('INSERT INTO test (user_id, user_name, username, datareg) VALUES (?, ?, ?, ?)', (user_id, user_name, username, datareg))
	conn.commit()

def importid():
    a = 0
    while True:
        cursor.execute('select user_id from test WHERE user_id')
        for row in c.execute("SELECT name, age FROM "):
            name, age = row
            break
        else:
            print("not found")


