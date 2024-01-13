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
        if imdb_rating == 'N/A':
            imdb_rating = '0'
        mpaa_rating = data.get("Rated", "Unknown")
        metascore = data.get("Metascore", "0")
        if metascore == 'N/A':
            metascore = '0'
        rotten_tomatoes = next((rating['Value'] for rating in data.get('Ratings', []) if 'Rotten Tomatoes' in rating.get('Source', '')), "N/A")
        if rotten_tomatoes == 'N/A':
            rotten_tomatoes_score = '0'
        elif rotten_tomatoes != 'N/A':
            rotten_tomatoes_score = int(rotten_tomatoes[:-1])
        imdb_count = data.get("imdbVotes", 0)
        if imdb_count == 'N/A':
            imdb_count_int = '0'
        elif imdb_count != 'N/A':
            imdb_count_int = int(imdb_count.replace(',', ''))
        awards = data.get("Awards", "None")
        poster = data.get("Poster", "No Poster")
        box_office = data.get("BoxOffice", "0")
        if box_office == 'N/A':
            box_office = '0'
        elif box_office != 'N/A':
            box_office = int(box_office.replace('$', '').replace(',', ''))
        
        update_query = "UPDATE movie SET imdb_score = %s, rating = %s, metascore = %s, rotten_tomatoes_score = %s, imdb_vote_count = %s, awards = %s, box_office = %s, poster_url = %s WHERE id = %s"
        values = (imdb_rating, mpaa_rating, metascore, rotten_tomatoes_score, imdb_count_int, awards, box_office, poster, movie[0])

        cursor.execute(update_query, values)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {title}: {e}")

conn.commit() 
cursor.close()
conn.close()