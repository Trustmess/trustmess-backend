import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  

import src.db_connector as db_connector
import src.secure.passhashing as pswhach

DB_PATH_MAIN = './db.db'

conn = db_connector.get_db_connection(DB_PATH_MAIN)
print(db_connector.init_db(conn))

# Hash passwords before creating users
admin_hashed_pass = pswhach.hash_password_def('adminpass')
user1_hashed_pass = pswhach.hash_password_def('password')
user2_hashed_pass = pswhach.hash_password_def('password')

db_connector.create_user(conn, 'admin1', admin_hashed_pass, True)
db_connector.create_user(conn, 'usertest1', user1_hashed_pass, False)
db_connector.create_user(conn, 'usertest2', user2_hashed_pass, False)

users = db_connector.get_all_users(conn)
conn.close(

)
print("Test Users:", [dict(user) for user in users])
