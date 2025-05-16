import sqlite3
import argparse

DB_NAME = "movies.db"

def list_all_genres():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM genres ORDER BY name")
    genres = cursor.fetchall()
    conn.close()

    print("🎭 利用可能なジャンル一覧:")
    for gid, name in genres:
        print(f"{gid:4} | {name}")

def search_movies(args):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    conditions = []
    params = []

    # ジャンル名 → ID に変換
    genre_ids = []
    if args.genres:
        genre_names = [g.strip() for g in args.genres.split(",")]
        cursor.execute(f"SELECT id FROM genres WHERE name IN ({','.join('?' for _ in genre_names)})", genre_names)
        genre_ids = [row[0] for row in cursor.fetchall()]
        if len(genre_ids) != len(genre_names):
            print("⚠️ 一部のジャンルが見つかりませんでした。")
            return

    # スコア・年・キーワードのフィルタ
    if args.min_score is not None:
        conditions.append("m.vote_average >= ?")
        params.append(args.min_score)
    if args.year:
        conditions.append("substr(m.release_date, 1, 4) = ?")
        params.append(str(args.year))
    if args.keyword:
        conditions.append("m.title LIKE ?")
        params.append(f"%{args.keyword}%")

    # ベースクエリ（JOIN）
    query = '''
        SELECT m.title, m.release_date, m.vote_average, GROUP_CONCAT(g.name)
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
    '''

    if genre_ids:
        query += f" WHERE g.id IN ({','.join('?' for _ in genre_ids)})"
        params = genre_ids + params
    elif conditions:
        query += " WHERE " + " AND ".join(conditions)
    elif not genre_ids and not conditions:
        query += " WHERE 1=1"  # fallback

    query += " GROUP BY m.id"

    if genre_ids:
        query += f" HAVING COUNT(DISTINCT g.id) = {len(genre_ids)}"

    query += " ORDER BY m.vote_average DESC"

    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    print(f"\n🎬 検索結果 ({len(results)} 件):")
    for title, date, score, genres in results:
        print(f"・{title} ({date}) - 評価: {score} - ジャンル: {genres}")

def main():
    parser = argparse.ArgumentParser(description="🎬 映画検索CLIツール")
    parser.add_argument('--list-genres', action='store_true', help="ジャンル一覧を表示")
    parser.add_argument('--genres', type=str, help="ジャンルをカンマで指定（例: Action,Horror）")
    parser.add_argument('--min-score', type=float, help="最低評価スコアで絞る")
    parser.add_argument('--year', type=int, help="公開年で絞る")
    parser.add_argument('--keyword', type=str, help="タイトルに含まれるキーワード")
    parser.add_argument('--limit', type=int, help="最大表示件数")

    args = parser.parse_args()

    if args.list_genres:
        list_all_genres()
    else:
        search_movies(args)

if __name__ == "__main__":
    main()

