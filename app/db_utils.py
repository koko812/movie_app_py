import sqlite3

def init_db(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            release_date TEXT,
            vote_average REAL,
            genres TEXT,
            poster_path TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_movie(movie, db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO movies (id, title, release_date, vote_average, genres, poster_path)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            movie["id"],
            movie["title"],
            movie.get("release_date"),
            movie.get("vote_average"),
            ", ".join(movie.get("genres", [])),
            movie.get("poster_path", "")
        ))
    except Exception as e:
        print(f"⚠️ insert_movie() エラー: {movie.get('title')} | {e}")

    finally:
        conn.commit()
        conn.close()



if __name__ == "__main__":
    init_db()

    sample = {
        "id": 12345,
        "title": "Inception",
        "release_date": "2010-07-16",
        "vote_average": 8.8,
        "genres": ["Action", "Science Fiction", "Thriller"]
    }

    insert_movie(sample)
    print("映画を保存しました！")

