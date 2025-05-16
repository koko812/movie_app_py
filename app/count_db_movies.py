import sqlite3
conn = sqlite3.connect("movies.db")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM movies")
print(f"🎥 DB内の映画総数: {cur.fetchone()[0]}")
