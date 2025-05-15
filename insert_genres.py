import os
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

def fetch_genres_from_api():
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # 失敗時は例外
    genres = response.json().get("genres", [])
    return genres  # ← [{"id": 28, "name": "Action"}, ...] の形式

def insert_genres_into_db(genres, db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for genre in genres:
        cursor.execute('''
            INSERT OR IGNORE INTO genres (id, name)
            VALUES (?, ?)
        ''', (genre["id"], genre["name"]))

    conn.commit()
    conn.close()
    print("✅ ジャンルを genres テーブルに挿入しました！")

if __name__ == "__main__":
    genres = fetch_genres_from_api()
    insert_genres_into_db(genres)

