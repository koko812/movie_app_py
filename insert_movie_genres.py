import sqlite3
import json

def insert_movie_genre_relations(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # すべての映画を取得（genre_ids カラムがあることを前提とする）
    cursor.execute("SELECT id, genres FROM movies")
    rows = cursor.fetchall()

    inserted = 0
    skipped = 0

    for movie_id, genre_string in rows:
        if not genre_string:
            skipped += 1
            continue

        try:
            # カンマ区切り or JSON形式の処理に対応（["Action", "Thriller"] のようなものを無視）
            genre_ids = [int(gid.strip()) for gid in genre_string.split(",") if gid.strip().isdigit()]
        except Exception as e:
            print(f"❌ パース失敗 (movie_id={movie_id}): {e}")
            skipped += 1
            continue

        for genre_id in genre_ids:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO movie_genres (movie_id, genre_id)
                    VALUES (?, ?)
                ''', (movie_id, genre_id))
                inserted += 1
            except Exception as e:
                print(f"❌ INSERT失敗 (movie_id={movie_id}, genre_id={genre_id}): {e}")

    conn.commit()
    conn.close()
    print(f"\n✅ 登録完了: {inserted} 件の関係を追加しました（スキップ: {skipped} 件）")

import sqlite3

def insert_movie_genres_from_names(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 1. ジャンル名→IDの対応をgenresテーブルから取得
    cursor.execute("SELECT id, name FROM genres")
    genre_map = {name.strip(): gid for gid, name in cursor.fetchall()}

    # 2. 映画テーブルからジャンル文字列を取得
    cursor.execute("SELECT id, genres FROM movies")
    rows = cursor.fetchall()

    inserted = 0
    skipped = 0

    for movie_id, genre_string in rows:
        if not genre_string:
            skipped += 1
            continue

        genre_names = [name.strip() for name in genre_string.split(",")]
        for name in genre_names:
            genre_id = genre_map.get(name)
            if genre_id:
                cursor.execute('''
                    INSERT OR IGNORE INTO movie_genres (movie_id, genre_id)
                    VALUES (?, ?)
                ''', (movie_id, genre_id))
                inserted += 1
            else:
                print(f"⚠️ ジャンル名 '{name}' に対応するIDが見つかりません")

    conn.commit()
    conn.close()
    print(f"\n✅ 完了: {inserted} 件を登録しました（スキップ: {skipped} 映画）")

if __name__ == "__main__":
    #insert_movie_genres()
    insert_movie_genres_from_names()
