import os
import sqlite3
from sqlite3 import Error

cwd = os.getcwd()

create_fragrance_table = """
CREATE TABLE IF NOT EXISTS fragrances (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  size INTEGER NOT NULL,
  fs_url TEXT,
  fd_url TEXT,
  jl_url TEXT,
  ps_url TEXT
);
"""

frag = {
    "name": "test",
    "size": 50,
    "fs_url": "test",
    "fd_url": "test",
    "jl_url": "test",
    "ps_url": "test",
}

def create_fragrance(f: dict):
    create_fragrance = (
        
        f"INSERT INTO\n"
        f"fragrances (name, size, fs_url, fd_url, jl_url, ps_url)\n"
        f"VALUES"
        f"({f.get('name')},"
        f"{f.get('size')}," 
        f"{f.get('fs_url')},"
        f"{f.get('fd_url')},"
        f"{f.get('jl_url')}," 
        f"{f.get('ps_url')});")
    execute_query(connection, create_fragrance)



def get_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB Successful.")
    except Error as e:
        print(f"Error {e} occured.")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error '{e}' occurred")
        print(query)


if __name__ == "__main__":
    connection = get_connection(os.path.join(cwd, "frag.db"))
    execute_query(connection, create_fragrance_table)
    create_fragrance(frag)
