"""Database table schemas"""

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Список всіх таблиць для створення
ALL_TABLES = [
    CREATE_USERS_TABLE,
]

# Список для видалення (в зворотному порядку через foreign keys)
DROP_TABLES = [
    "DROP TABLE IF EXISTS users CASCADE;",
]