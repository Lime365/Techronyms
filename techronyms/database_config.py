import os
import sqlite3
from sqlite3 import Error

project_path = r"C:/Users/Lime/pyProjects/techronyms"

#Create our SQL connection
def sq_connect(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print (e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print (e)

def main_create_table():
    database = f"{project_path}/acronyms.db"
#----------- Modify to create new table if needed ------------#
    sql_make_table = """CREATE TABLE IF NOT EXISTS scoreboard
                        (id integer PRIMARY KEY,
                        nick NOT NULL,
                        score integer NOT NULL,
                        date
                        )"""

    conn = sq_connect(database)

    if conn is not None:
        create_table(conn, sql_make_table)
    else:
        print('Error!')

def make_query(conn, q):
    #---------------- Modify to make a new entry to the database ---------------#
    sql = '''INSERT INTO scoreboard(nick, score, date) VALUES(?,?,?)'''
    c = conn.cursor()
    c.execute(sql, q)
    return c.lastrowid

def main_add_entry():
    database = f'{project_path}/acronyms.db'

    conn = sq_connect(database)
    with conn:
        q = ('nick', 'score', '2020-02-17');
        query_id = make_query(conn, q)



if __name__ == '__main__':
# Run main_create_table() to create table or main_add_entry() to add a new entry

    #main_create_table()
    #main_add_entry()
