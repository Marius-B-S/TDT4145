import sqlite3 as sql

conn = sql.connect('TrondelagTeater.db')
cur = conn.cursor()

with open("TeaterDB.sql") as file:
    sql_script = file.read()
cur.executescript(sql_script)

cur.close()
conn.close()
