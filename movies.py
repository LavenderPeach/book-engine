import requests
import mysql.connector

api_key = 'f6a2e921cb0f74ee8188d6a0ad58fdab'  

# connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Edgerunner77',
    database='books'
)

cursor = conn.cursor()

def get_and_store_random_movies(api_key, movie_id):
    url = f"https://api.themoviedb.org/3/movie/top_rated"
    params = {"api_key": api_key}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        movie_data = response.json()
        results = movie_data.get("results", [])

        for movie in results:
            title = movie.get("title", "Unknown Title")
            overview = movie.get("overview", "No overview available")
            released_date = movie.get("release_date", "Unknown Release Date")
            rating = movie_data.get("vote_average", 0.0)
            runtime = movie_data.get("runtime", 0)

            # Genre Information
            genres = movie_data.get("genres", [])
            genre = ", ".join([genre["name"] for genre in genres]) if genres else "Unknown Genre"

            # Director info

            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
            credits_params = {"api_key": api_key}
            credits_response = requests.get(credits_url, params = credits_params)

            if credits_response.status_code == 200:
                credits_data = credits_response.json()
                crew = credits_data.get("crew", [])
                directors = [member["name"] for member in crew if member["job"] == "Director"]
                director = ", ".join(directors) if directors else "Unknown"

                writers = [member["name"] for member in crew if member["job"] == "Writer"]
                writers_list = ", ".join(writers) if writers else "Unknown"

                #Top two actors

                cast = credits_data.get("cast", [])
                actors = [actor["name"] for actor in cast[:2]]
                first_actor = actors[0] if actors else "Unknown Actor"
                second_actor = actors[1] if len(actors) > 1 else "Unknown Actor"

            # Insert movie details into the database
            insert_query = """
            INSERT INTO movie (title, overview, released_date, rating, runtime, genre, director, writers, first_actor, second_actor)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            insert_data = (title, overview, released_date, rating, runtime, genre, director, writers_list, first_actor, second_actor)
            cursor.execute(insert_query, insert_data)
            conn.commit()
    else:
        print(f"Error: {response.status_code}")

# Example: Get and store random movies from page 1
get_and_store_random_movies(api_key, movie_id=220)

# Close the database connection
cursor.close()
conn.close()
