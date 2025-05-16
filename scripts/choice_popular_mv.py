import sqlite3

def search_movies(min_vote=7.5, db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT title, release_date, vote_average, genres
        FROM movies
        WHERE vote_average >= ?
        ORDER BY vote_average DESC
    ''', (min_vote,))

    results = cursor.fetchall()
    conn.close()

    print(f"\n--- 評価 {min_vote} 以上の映画一覧 ---")
    for title, release_date, vote_average, genres in results:
        print(f"{title} ({release_date}) - 評価: {vote_average} - ジャンル: {genres}")

if __name__ == "__main__":
    search_movies()

