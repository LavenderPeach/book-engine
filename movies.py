import requests
import mysql.connector
import random 

api_key = 'f6a2e921cb0f74ee8188d6a0ad58fdab'  

# connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Edgerunner77',
    database='books'
)

cursor = conn.cursor()

def get_and_store_random_movies(api_key, page):
        url = f"https://api.themoviedb.org/3/movie/top_rated"

        params = {
            "api_key": api_key,
            "page": page,
         }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            movie_data = response.json()
            results = movie_data.get("results", [])
            for movie in results:
                try:
                    movie_id = movie.get("id")
                    movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
                    movie_params = {"api_key": api_key}
                    movie_response = requests.get(movie_url, params = movie_params)

                    if movie_response.status_code == 200:
                        detailed_movie_data = movie_response.json()
                    # for movie in results:
                        title = detailed_movie_data.get("title", "Unknown Title")
                        overview = detailed_movie_data.get("overview", "No overview available")
                        released_date = detailed_movie_data.get("release_date", "2024-01-01")
                        runtime = detailed_movie_data.get("runtime", 0)

                        # Genre Information
                        genres = detailed_movie_data.get("genres", [])
                        genre = ", ".join([genre["name"] for genre in genres]) if genres else "Unknown Genre"

                        # Director info

                        credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits"
                        credits_params = {"api_key": api_key}
                        credits_response = requests.get(credits_url, params = credits_params)

                        if credits_response.status_code == 200:
                            credits_data = credits_response.json()
                            crew = credits_data.get("crew", [])
                            directors = [member["name"] for member in crew if member["job"] == "Director"]
                            director = ", ".join(directors) if directors else "Unknown"

                            # Writer Info

                            writers = [member["name"] for member in crew if member["job"] == "Writer" or member["job"] == "Screenplay" or member["job"] == "Author"]
                            writers_list = ", ".join(writers) if writers else "Unknown"

                            #Top two actors

                            cast = credits_data.get("cast", [])
                            actors = [actor["name"] for actor in cast]
                            actor_list = ", ".join(actors) if actors else "Unknown Actors"


                            # Poster URL

                            poster_url = f"https://image.tmdb.org/t/p/w500/{movie_data.get('poster_path', 'No poster available')}"

                            # Insert movie details into the database
                            insert_query = """
                            INSERT INTO movie (title, plot, release_date, runtime, genre, director, writer, cast, poster_url)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            insert_data = (title, overview, released_date, runtime, genre, director, writers_list, actor_list, poster_url)
                            cursor.execute(insert_query, insert_data)
                            conn.commit()
                except mysql.connector.Error as err:
                    if "Duplicate entry" in str(err):
                      print(f"Skipped duplicate title: {title}")
                    else:
                      print(f"Error: {err}")
        else:
            print(f"Error: {response.status_code}")

# Example: Get and store random movies from page 1
for page_number in range(37, 39):
    get_and_store_random_movies(api_key, page=page_number)

# Close the database connection
cursor.close()
conn.close()