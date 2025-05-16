import os
from dotenv import load_dotenv
import requests

# .envファイルの内容を読み込む
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
if not API_KEY:
    raise ValueError("TMDB_API_KEYが設定されていません。")

def fetch_movies(region="JP", start_year=2020, end_year=2020):
    url = (
        f"https://api.themoviedb.org/3/discover/movie"
        f"?api_key={API_KEY}"
        f"&region={region}"
        f"&primary_release_date.gte={start_year}-01-01"
        f"&primary_release_date.lte={end_year}-12-31"
        f"&page=1"
    )
    response = requests.get(url)
    data = response.json()
    return data.get("results", [])

if __name__ == "__main__":
    movies = fetch_movies()
    for m in movies:
        print(f"{m['title']} ({m['release_date']}) - Rating: {m['vote_average']}")
