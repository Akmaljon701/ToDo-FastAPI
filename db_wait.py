import time
import psycopg2
from psycopg2 import OperationalError

def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(
                dbname="todo_fast_api",
                user="postgres",
                password="123123",
                host="db",
                port="5432"
            )
            conn.close()
            print("PostgreSQL is ready!")
            break
        except OperationalError:
            print("Waiting for PostgreSQL to be ready...")
            time.sleep(2)

if __name__ == "__main__":
    wait_for_postgres()
