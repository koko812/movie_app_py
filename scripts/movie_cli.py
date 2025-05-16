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

def search_movies_by_genres(genre_names):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ジャンル名 → ID 変換
    placeholders = ','.join('?' for _ in genre_names)
    cursor.execute(f"SELECT id FROM genres WHERE name IN ({placeholders})", genre_names)
    genre_ids = [row[0] for row in cursor.fetchall()]

    if len(genre_ids) != len(genre_names):
        print("⚠️ 一部のジャンルが見つかりませんでした。スペルミスに注意！")
        return

    # 映画を genre_ids すべて含むものだけに絞る
    query = f'''
        SELECT m.title, GROUP_CONCAT(g.name)
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
        WHERE g.id IN ({','.join('?' for _ in genre_ids)})
        GROUP BY m.id
        HAVING COUNT(DISTINCT g.id) = ?
        ORDER BY m.vote_average DESC
    '''
    params = genre_ids + [len(genre_ids)]
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    print(f"\n🎬 {genre_names} を含む映画一覧:")
    for title, genres in results:
        print(f"・{title}  [{genres}]")

def main():
    parser = argparse.ArgumentParser(description="🎬 映画検索CLIツール")
    parser.add_argument('--list-genres', action='store_true', help="ジャンル一覧を表示")
    parser.add_argument('--genres', type=str, help="ジャンルをカンマで指定（例: Action,Horror）")

    args = parser.parse_args()

    if args.list_genres:
        list_all_genres()
    elif args.genres:
        genre_names = [g.strip() for g in args.genres.split(",")]
        search_movies_by_genres(genre_names)
    else:
        print("⚠️ オプションが指定されていません。--help を見てね！")

if __name__ == "__main__":
    main()

