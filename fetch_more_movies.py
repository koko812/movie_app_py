import time
from db import insert_movie, init_db
from sample import fetch_movies_by_page
import sqlite3

init_db()

all_movies = []
total_pages = 50

db_name='movies.db'

def movie_exists(movie_id, db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM movies WHERE id = ?", (movie_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


for page in range(1, total_pages + 1):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    print(f"📦 ページ {page} を取得中...")
    movies = fetch_movies_by_page(start_year=1980, end_year=2024, pages=page)
    print(f"🎥 APIから取得した映画の数: {len(movies)}")
    before = cur.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    for m in movies:
    #    if movie_exists(m["id"]):
    #        print(f"⚠️ 重複: {m['title']} ({m['id']})")
    #    else:
    #        print(f"✅ 新規: {m['title']} ({m['id']})")
        insert_movie(m)
    time.sleep(0.4)  # サーバーへの配慮
    all_movies.extend(movies)
    after = cur.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    print(f"✅ 実際に保存された件数: {after - before}")
    conn.commit()
    conn.close()

print(f"\n✅ {len(all_movies)} 件の映画を保存しました！")

