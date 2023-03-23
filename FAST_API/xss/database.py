# Import module
import sqlite3
  
# Connecting to sqlite
conn = sqlite3.connect('tutorial.db')
  
# Creating a cursor object using the 
# cursor() method
cursor = conn.cursor()
  
# Creating table
table ="""CREATE TABLE IF NOT EXISTS todos(ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER(12), TASK VARCHAR(255));"""
cursor.execute(table)
