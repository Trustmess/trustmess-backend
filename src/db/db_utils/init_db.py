import os 
import psycopg2
from dotenv import load_dotenv

from src.db.models import CREATE_USERS_TABLE

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def main():
    if not DATABASE_URL:
        raise SystemExit('ATABASE_URL not set in env')
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            conn.commit()
            print("SUCCESS. Users table created (or already exists)")
    except Exception as error:
        raise print(f'Creating table was been occured: {error}')
    finally:
        conn.close()

if __name__ == "__main__":
    main()