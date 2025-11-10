# * ALL CRUD OPERATIONS (* Queries)
from .connection import get_connection, release_connection

def get_all_users(conn: Connection):
    cursor = conn.execute('SELECT id, username, isAdmin FROM users')
    return cursor.fetchall()

def get_user_by_id(conn: Connection, user_id: int):
    cursor = conn.execute('SELECT id, username, isAdmin FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone()

def get_user_by_username(conn: Connection, username: str):
    cursor = conn.execute('SELECT id, username FROM users WHERE username = ?', (username,))
    return cursor.fetchone()


def check_authentication(conn: Connection, username: str):
    cursor = conn.execute(
        'SELECT id, username, password FROM users WHERE username = ?', (username,)
    )
    return cursor.fetchone()


def create_user(conn: Connection, username: str, password: str, isAdmin: bool = False):
    with conn:
        cursor = conn.execute(
            'INSERT INTO users (username, password, isAdmin) VALUES (?, ?, ?)',
            (username, password, isAdmin)
        )
        user_id = cursor.lastrowid
        conn.commit()

    return get_user_by_id(conn, user_id)

# ! *************************************** ! #
# !ONLY DEV, DELETE BEFORE DEPLOY
def get_all_users_with_pass(conn: Connection):
    cursor = conn.execute('SELECT id, username, password, isAdmin FROM users')
    return cursor.fetchall()
# ! *************************************** ! #
