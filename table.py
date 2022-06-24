import sqlite3 as sql

con = sql.connect('database.db')
with open('table.sql') as f:
    con.executescript(f.read())