import sqlite3

conn = sqlite3.connect("movies.db")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM movies")
print("🎬 映画件数:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM movie_genres")
print("🎭 映画×ジャンルの中間テーブル件数:", cur.fetchone()[0])
