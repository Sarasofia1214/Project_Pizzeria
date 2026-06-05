import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        if self._pool is None:
            self._pool = pool.SimpleConnectionPool(
                1, 10,
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            print("✅ Conectado a PostgreSQL")
        return self._pool.getconn()

    def disconnect(self, conn):
        if self._pool and conn:
            self._pool.putconn(conn)

db_instance = Database()