import sqlite3

def get_all_genres(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT genres FROM movies")
    rows = cursor.fetchall()
    conn.close()

    genre_set = set()
    for row in rows:
        genre_str = row[0]
        if genre_str:
            genres = [g.strip() for g in genre_str.split(",")]
            genre_set.update(genres)

    return sorted(genre_set)

def search_movies(min_vote=0.0, keyword="", genre="", db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = '''
        SELECT title, release_date, vote_average, genres
        FROM movies
        WHERE vote_average >= ?
    '''
    params = [min_vote]

    if keyword:
        query += " AND title LIKE ?"
        params.append(f"%{keyword}%")

    if genre:
        query += " AND genres LIKE ?"
        params.append(f"%{genre}%")

    query += " ORDER BY vote_average DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    print(f"\n--- 検索結果 ---")
    if not results:
        print("該当する映画が見つかりませんでした。")
    for title, release_date, vote_average, genres in results:
        print(f"{title} ({release_date}) - 評価: {vote_average} - ジャンル: {genres}")

if __name__ == "__main__":
    print("🎬 映画検索ツール 🎬")
    try:
        vote_input = input("最低評価（例: 7.5）：").strip()
        min_vote = float(vote_input) if vote_input else 0.0
    except ValueError:
        min_vote = 0.0

    keyword = input("タイトルに含まれるキーワード（空でもOK）：").strip()

    all_genres = get_all_genres()
    print("\n🎭 利用可能なジャンル一覧:")
    for idx, g in enumerate(all_genres, 1):
        print(f"{idx}. {g}")

    try:
        genre_choice = input("\nジャンル番号を選んでください（空白でスキップ）：").strip()
        genre = all_genres[int(genre_choice) - 1] if genre_choice else ""
    except (ValueError, IndexError):
        genre = ""

    search_movies(min_vote=min_vote, keyword=keyword, genre=genre)

