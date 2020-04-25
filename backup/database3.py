# -*- coding: utf-8 -*-
import sqlite3

# Create a 'Connection' object.
conn = sqlite3.connect('mail.db')

# Create a 'Cursor' object from 'Connection' object.
cur = conn.cursor()

# Create a table
cur.execute('''DROP TABLE mailLabel''')
cur.execute('''CREATE TABLE mailLabel
    (mailID int PRIMARY KEY,labelID int)''')
cur.execute('''CREATE TABLE labelIndex
    (labelID int PRIMARY KEY,labelCount int)''')
cur.execute('''CREATE TABLE trainData
    (labelID int,wordID int,count int ,PRIMARY KEY(labelID,wordID))''')
cur.execute('''CREATE TABLE trainMail
    (labelID int PRIMARY KEY,content TEXT)''')
cur.execute('''CREATE TABLE mailList
    (mailID int PRIMARY KEY,date TEXT,title TEXT,content TEXT)''')
cur.execute('''CREATE TABLE label
    (labelID int PRIMARY KEY,label TEXT)''')

cur.execute('''CREATE TABLE word
    (wordID int PRIMARY KEY,word TEXT)''')
