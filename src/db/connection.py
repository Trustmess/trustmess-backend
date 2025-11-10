import psycopg2
from psycopg2 import pool 
from psycopg2.extras import RealDictCursor
import os 
from dotenv import load_dotenv


load_dotenv()

#Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'messenger_db')
    DB_USER = os.getenv('DB_USER', 'messenger_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'localhost')
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

connection_pool = None

def init_connection_pool():
    ...

def get_connection():
    ...

def get_admin_connection():
    ...

def release_connection():
    ...

def close_all_connection():
    ...

