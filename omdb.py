import requests
import mysql.connector

api_key = 'a7472fe0'

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Edgerunner77',
    database = 'books'
)

cursor = conn.cursor()

cursor.execute("SELECT id, title FROM movie ORDER BY id desc")
movies = cursor.fetchall()