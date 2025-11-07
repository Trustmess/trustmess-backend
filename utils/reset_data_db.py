import sys
import os

import sqlite3

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  

DB_PATH_MAIN = './db.db'

def reset_database():
    '''Delete all info in DB'''
    conn = sqlite3.connect(DB_PATH_MAIN)
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM users')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')
        conn.commit()

        print('DB was been reset')
    except sqlite3.Error as error:
        print(f'Error reset database {error}')
        conn.rollback
    finally:
        conn.close()

if __name__ == "__main__":
    confirm = input('Delete ALL info in DB? Press "Y" if YES or "N" if NO \n')

    if confirm == 'y':
        reset_database()
    else:
        print('Cancel delete info in DB')

