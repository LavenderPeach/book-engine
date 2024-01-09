import requests

key = "AIzaSyCnZ0XLCHO5J6q7aq7YoxH4w4_F_KBxBO8"
url = "https://www.googleapis.com/books/v1/volumes"

book_title = input("Enter the book title: ")

book_title_universal = book_title.lower()

params = {"q": book_title_universal, "key": key}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    if 'items' in data:
        first_book = data['items'][0]['volumeInfo']
        print('First Title Found:')
        print(f"- Title: {first_book.get('title', 'N/A')}")
        print(f"- Author(s): {first_book.get('authors', 'N/A')}")
        print(f"- Published Date: {first_book.get('publishedDate', 'N/A')}")
        print(f"- Description: {first_book.get('description', 'N/A')}")

else:
    print("Error:", response.status_code)

