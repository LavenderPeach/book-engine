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
    params = {"q": 'Wuthering Heights', "key": key}


    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
# ...

        if 'items' in data:
            for book in data['items']:
                title = book.get('volumeInfo', {}).get('title', 'Unknown Title')
                authors = book.get('volumeInfo', {}).get('authors', ['Unknown Author'])
                author = ', '.join(authors)
                year = book.get('volumeInfo', {}).get('publishedDate', 'Unknown Year')[:4]
                synopsis = book.get('volumeInfo', {}).get('description', 'No synopsis available')[:495]
                category = ', '.join(book.get('volumeInfo', {}).get('categories', 'No genre available'))[:48]
                is_mature = book.get('volumeInfo', {}).get('maturityRating', 'Unknown maturity rating') == 'MATURE'
                is_mature_int = 1 if is_mature else 0
                average_rating = book.get('volumeIndo', {}).get('averageRating', '0.0')
                average_rating_flt = float(average_rating)
                insert_query = "INSERT INTO book_info (title, author, year, synopsis, category, is_mature, average_rating) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                insert_data = (title, author, year, synopsis, category, is_mature_int, average_rating_flt)
                cursor.execute(insert_query, insert_data)
                conn.commit()




        else:
            print("Error:", response.status_code)

get_and_store(key)

cursor.close()
conn.close()