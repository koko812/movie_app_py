import os
import requests
from dotenv import load_dotenv
from db import init_db, insert_movie

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_genre_mapping():
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    genres = response.json().get("genres", [])
    return {genre["id"]: genre["name"] for genre in genres}

def fetch_movies_by_page(region="JP", start_year=2020, end_year=2020, pages=3):
    genre_map = fetch_genre_mapping()
    base_url = "https://api.themoviedb.org/3/discover/movie"
    all_movies = []

    for page in range(1, pages + 1):
        params = {
            "api_key": API_KEY,
            "region": region,
            "primary_release_date.gte": f"{start_year}-01-01",
            "primary_release_date.lte": f"{end_year}-12-31",
            "page": page
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        results = data.get("results", [])

        for movie in results:
            genre_ids = movie.get("genre_ids", [])
            genre_names = [genre_map.get(gid, "") for gid in genre_ids]

            movie_data = {
                "id": movie["id"],
                "title": movie["title"],
                "release_date": movie.get("release_date", ""),
                "vote_average": movie.get("vote_average", 0),
                "genres": genre_names
            }
            all_movies.append(movie_data)

    return all_movies

if __name__ == "__main__":
    init_db()
    movies = fetch_movies_by_page(region="JP", start_year=2010, end_year=2024, pages=5)
    for m in movies:
        insert_movie(m)
    print(f"{len(movies)} 件の映画を保存しました！")

