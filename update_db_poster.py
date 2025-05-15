import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
DB_NAME = "movies.db"

def fetch_movie_from_api(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        return res.json()
    return None

def update_poster_paths():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM movies WHERE poster_path IS NULL OR poster_path = ''")
    ids = [row[0] for row in cursor.fetchall()]
    
    print(f"🎬 更新対象: {len(ids)} 本")

    for movie_id in ids:
        data = fetch_movie_from_api(movie_id)
        if data and data.get("poster_path"):
            cursor.execute("UPDATE movies SET poster_path = ? WHERE id = ?", (data["poster_path"], movie_id))
            print(f"✅ {movie_id} にポスター追加: {data['poster_path']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_poster_paths()

