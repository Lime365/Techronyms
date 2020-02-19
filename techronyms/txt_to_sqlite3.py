import os
import sqlite3
from sqlite3 import Error

path = r'C:/Users/Lime/pyProjects/tech_abs_quiz/'

def connect(db_file):
    conn = sqlite3.connect(db_file)
    return conn

with open(path + 'acronyms.txt', 'r') as a:
    with open(path + 'terms.txt', 'r') as t:
        acr = a.readlines()
        terms = t.readlines()

acro = [abb[:-1] for abb in acr]
exlp = [term[:-1] for term in terms]
merged = list(zip(acro, exlp))


def get_existing():
    conn = connect(path+'abbs.db')
    c = conn.cursor()
    get = '''SELECT abb FROM abbs;'''
    abbs = [abb for abb in c.execute(get)]
    ls = [x[0] for x in abbs]
    print(ls)
    return ls






def insert_to_db():
    conn = connect(path+'abbs.db')
    c = conn.cursor()

    for a, t in merged:
        if a not in get_existing():
            c.execute("INSERT INTO abbs (abb, answer, difficulty, date_added) VALUES(?, ?, ?, ?)", (a,t, 'Nan', '2020-02-13'))
        print(c.lastrowid)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_to_db()
