import sqlite3
import csv

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

def search_movies(min_vote=0.0, keyword="", selected_genres=[], db_name="movies.db"):
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

    for genre in selected_genres:
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

    return results  # 👈 ここを追加

def save_to_csv(results, filename="results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Title", "Release Date", "Vote Average", "Genres"])  # ヘッダー
        writer.writerows(results)
    print(f"\n✅ {filename} に保存しました！")



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

    genre_input = input("\nジャンル番号をカンマ区切りで入力（例: 1,4）（空白でスキップ）：").strip()
    selected_genres = []

    if genre_input:
        try:
            indexes = [int(x.strip()) for x in genre_input.split(",")]
            selected_genres = [all_genres[i - 1] for i in indexes if 1 <= i <= len(all_genres)]
        except ValueError:
            pass  # 無効な入力は無視

    results = search_movies(min_vote=min_vote, keyword=keyword, selected_genres=selected_genres)

    if results:
        save = input("CSVに保存しますか？ (y/n)：").strip().lower()
        if save == "y":
            filename = input("保存するファイル名（例: action_horror.csv）：").strip() or "results.csv"
            save_to_csv(results, filename)

