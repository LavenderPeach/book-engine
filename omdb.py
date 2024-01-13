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

for movie in movies:
    title = movie[1]
    omdb_api_url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(omdb_api_url)
        response.raise_for_status()
        data = response.json()

        imdb_rating = data.get("imdbRating", "0")
        mpaa_rating = data.get("Rated", "Unknown")
        metascore = data.get("Metascore", "0")
        rotten_tomatoes = next((rating['Value'] for rating in data.get('Ratings', []) if 'Rotten Tomatoes' in rating.get('Source', '')), "N/A")
        imdb_count = data.get("imdbVotes", 0)
        awards = data.get("Awards", "None")
        poster = data.get("Poster", "No Poster")
        box_office = data.get("BoxOffice", "0")
        
        update_query = "UPDATE movie SET imdb_score = %s, rating = %s, metascore = %s, rotten_tomatoes_score = %s, imdb_vote_count = %s, awards = %s, box_office = %s, poster_url = %s WHERE id = %s"
        values = (imdb_rating, mpaa_rating, metascore, imdb_count, awards, box_office, poster, movie[0])

        cursor.execute(update_query, values)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {title}: {e}")

conn.commit() 
cursor.close()
conn.close()