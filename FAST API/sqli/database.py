# Import module
import sqlite3
  
# Connecting to sqlite
conn = sqlite3.connect('tutorial.db')
  
# Creating a cursor object using the 
# cursor() method
cursor = conn.cursor()
  
# Creating table
drop = """DROP TABLE IF EXISTS todos"""
cursor.execute(drop)

table ="""CREATE TABLE todos(ID INTEGER PRIMARY KEY AUTOINCREMENT,USER_ID INTEGER(12), TASK VARCHAR(255));"""
cursor.execute(table)
