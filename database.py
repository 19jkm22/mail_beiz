# -*- coding: utf-8 -*-
import sqlite3

# Create a 'Connection' object.
conn = sqlite3.connect('data.db')

# Create a 'Cursor' object from 'Connection' object.
cur = conn.cursor()

# Create a table
cur.execute('''CREATE TABLE tweet
    (id int,userID int,text TEXT, mediaID int)''')
cur.execute('''CREATE TABLE image
    (id int,mediaID int,url TEXT)''')
cur.execute('''CREATE TABLE user
    (userID int,name TEXT,image TEXT)''')