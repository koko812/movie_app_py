import time
from db import insert_movie, init_db
from sample import fetch_movies_by_page

init_db()

all_movies = []
total_pages = 30

for page in range(1, total_pages + 1):
    print(f"📦 ページ {page} を取得中...")
    movies = fetch_movies_by_page(start_year=2000, end_year=2024, pages=1)
    for m in movies:
        insert_movie(m)
    time.sleep(0.4)  # サーバーへの配慮
    all_movies.extend(movies)

print(f"\n✅ {len(all_movies)} 件の映画を保存しました！")

