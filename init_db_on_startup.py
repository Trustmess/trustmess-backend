import os
import src.db_connector as db_connector
from src.secure.passhashing import hash_password_def

def initialize_database():
    """
    Initializes the database if it doesn't exist and populates it with test users.
    This function is designed to be run once at container startup.
    """
    if not os.path.exists(db_connector.DB_PATH_MAIN):
        print("Database not found, initializing...")
        try:
            # Get connection
            conn = db_connector.get_db_connection(db_connector.DB_PATH_MAIN)
            
            # Initialize schema
            db_connector.init_db(conn)
            
            # Add test users
            test_users = [
                ('admin', hash_password_def('admin123'), 1),
                ('user1', hash_password_def('password1'), 0),
                ('user2', hash_password_def('password2'), 0),
            ]
            
            for username, password, is_admin in test_users:
                try:
                    conn.execute(
                        'INSERT INTO users (username, password, isAdmin) VALUES (?, ?, ?)',
                        (username, password, is_admin)
                    )
                except Exception as e:
                    print(f"Could not add user {username}. It might already exist. Error: {e}")
            
            conn.commit()
            print("✅ Database initialized and populated.")
            
        except Exception as e:
            print(f"❌ Failed to initialize database: {e}")
            # Re-raise the exception to make sure the container startup fails
            # if the database can't be initialized.
            raise
        finally:
            if 'conn' in locals() and conn:
                conn.close()
                print("Database connection closed.")
    else:
        print("Database already exists, skipping initialization.")

if __name__ == "__main__":
    initialize_database()
