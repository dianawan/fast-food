import os
import psycopg2
from flask import current_app


class FastFoodDB:
    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')

        self.connection = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            user=self.db_user,
            password=self.db_password)
        
        self.cursor = self.connection.cursor()


class CreateTables(FastFoodDB):
    def __init__(self):
        super().__init__()

    def create_tables(self):
        ''' create tables '''
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE ,
                email VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                is_admin VARCHAR NOT NULL
            )
            ''', '''
            CREATE TABLE IF NOT EXISTS fooditems(
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                description VARCHAR NOT NULL,
                price VARCHAR NOT NULL,
                date TIMESTAMP
            )
            ''', '''
            CREATE TABLE IF NOT EXISTS orders(
                id serial PRIMARY KEY,
                name VARCHAR NOT NULL,
                username VARCHAR NOT NULL,
                destination VARCHAR NOT NULL,
                price INTEGER NOT NULL,
                status VARCHAR NOT NULL,
                date TIMESTAMP
            )
            '''
        ]

        for query in queries:
            self.cursor.execute(query)

        self.connection.commit()
        self.cursor.close()

    def drop_tables(self):
        ''' Drop tables '''
        queries = [
            '''
            DROP TABLE IF EXISTS users 
            ''', '''
            DROP TABLE IF EXISTS fooditems
            ''', '''
            DROP TABLE IF EXISTS orders
            '''
        ]

        for query in queries:
            self.cursor.execute(query)

        self.connection.commit()
        self.cursor.close()


if __name__ == '__main__':
    CreateTables().drop_tables()
    CreateTables().create_tables()
