# -*- coding: utf-8 -*-
import sqlite3

# Create a 'Connection' object.
conn = sqlite3.connect('data2.db')

# Create a 'Cursor' object from 'Connection' object.
cur = conn.cursor()

# Create a table
cur.execute('''CREATE TABLE text
    (id int,text1 TEXT,text2 TEXT,text3 TEXT)''')