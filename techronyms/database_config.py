import os
import sqlite3
from sqlite3 import Error

project_path = r"C:/Users/Lime/pyProjects/tech_abs_quiz"

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

def main_create():
    database = f"{project_path}/abbs.db"

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

def add_question(conn, q):
    sql = '''INSERT INTO scoreboard(nick, score, date) VALUES(?,?,?)'''
    c = conn.cursor()
    c.execute(sql, q)
    return c.lastrowid

def main_create_base():
    database = f'{project_path}/abbs.db'

    conn = sq_connect(database)
    with conn:
        for i in range(10,21):
            q = ('test'+str(i), i, '2020-02-17');
            query_id = add_question(conn, q)



if __name__ == '__main__':

    main_create_base()
