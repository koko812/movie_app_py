import sqlite3

def create_normalized_tables(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # ✅ genres テーブル（APIのIDをそのまま使う）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY,  -- ← AUTOINCREMENT 外した！
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # ✅ movie_genres 中間テーブル（多対多）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movie_genres (
            movie_id INTEGER,
            genre_id INTEGER,
            PRIMARY KEY (movie_id, genre_id),
            FOREIGN KEY (movie_id) REFERENCES movies(id),
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ 正規化用のテーブルを修正して作成しました！")

if __name__ == "__main__":
    create_normalized_tables()

