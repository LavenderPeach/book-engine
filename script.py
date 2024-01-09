import requests
import mysql.connector

# connection to mysql

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Edgerunner77',
    database='books'
)

cursor = conn.cursor()
key = "AIzaSyCnZ0XLCHO5J6q7aq7YoxH4w4_F_KBxBO8"


def get_and_store(key):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": "a", "key": key}


    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
# ...

        if 'items' in data:
            for book in data['items']:
                title = book.get('volumeInfo', {}).get('title', 'Unknown Title')[:45]
                authors = book.get('volumeInfo', {}).get('authors', ['Unknown Author'])
                author = ', '.join(authors)
                year = book.get('volumeInfo', {}).get('publishedDate', 'Unknown Year')[:4]
                synopsis = book.get('volumeInfo', {}).get('description', 'No synopsis available')[:495]

                insert_query = "INSERT INTO book_info (title, author, year, synopsis) VALUES (%s, %s, %s, %s)"
                insert_data = (title, author, year, synopsis)
                cursor.execute(insert_query, insert_data)
                conn.commit()
        print(f"Inserted {len(data['items'])} books into the database.")

    else:
        print("Error:", response.status_code)
        print(response.text)
get_and_store(key)

cursor.close()
conn.close()