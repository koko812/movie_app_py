import tkinter as tk
from tkinter import ttk
import sqlite3

DB_NAME = "movies.db"

def get_all_genres():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM genres ORDER BY name")
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres

def get_selected_genres():
    indices = genre_listbox.curselection()
    return [genre_listbox.get(i) for i in indices]

def search_movies_gui(keyword=None, genres=None, min_score=None, year=None, limit=50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    conditions = []
    params = []

    genre_ids = []
    if genres:
        cursor.execute(f"SELECT id FROM genres WHERE name IN ({','.join('?' for _ in genres)})", genres)
        genre_ids = [row[0] for row in cursor.fetchall()]
        if len(genre_ids) != len(genres):
            return [], "⚠️ 一部のジャンルが見つかりませんでした。"

    if min_score is not None:
        conditions.append("m.vote_average >= ?")
        params.append(min_score)

    if year is not None:
        conditions.append("substr(m.release_date, 1, 4) = ?")
        params.append(str(year))

    if keyword:
        conditions.append("m.title LIKE ?")
        params.append(f"%{keyword}%")

    query = '''
        SELECT m.title, m.release_date, m.vote_average, GROUP_CONCAT(g.name)
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
    '''

    if genre_ids:
        query += f" WHERE g.id IN ({','.join('?' for _ in genre_ids)})"
        params = genre_ids + params
        if conditions:
            query += " AND " + " AND ".join(conditions)
    elif conditions:
        query += " WHERE " + " AND ".join(conditions)
    else:
        query += " WHERE 1=1"

    query += " GROUP BY m.id"

    if genre_ids:
        query += f" HAVING COUNT(DISTINCT g.id) = {len(genre_ids)}"

    query += " ORDER BY m.vote_average DESC"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return results, None


def on_search():
    keyword = entry_keyword.get().strip()
    genres = get_selected_genres()
    min_score = score_var.get()
    year = entry_year.get().strip()
    year = int(year) if year.isdigit() else None

    results, err = search_movies_gui(
        keyword=keyword,
        genres=genres,
        min_score=min_score,
        year=year
    )

    result_listbox.delete(0, tk.END)
    if err:
        result_listbox.insert(tk.END, err)
    elif results:
        for title, date, score, g in results:
            result_listbox.insert(tk.END, f"{title} ({date}) ★{score} [{g}]")
    else:
        result_listbox.insert(tk.END, "🔍 一致する映画が見つかりませんでした。")



# ============ GUI 構築 ============

root = tk.Tk()
root.title("映画検索アプリ（ジャンル & キーワード）")

ttk.Label(root, text="🔎 キーワード").pack()
entry_keyword = ttk.Entry(root, width=40)
entry_keyword.pack(pady=(0, 10))

ttk.Label(root, text="🎭 ジャンル（複数選択可）").pack()
genre_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=40, height=10)
genre_listbox.pack(pady=(0, 10))
for genre in get_all_genres():
    genre_listbox.insert(tk.END, genre)

# --- 評価スコア入力 ---
ttk.Label(root, text="⭐ 最低評価スコア").pack()
score_var = tk.DoubleVar(value=0.0)
score_slider = ttk.Scale(root, from_=0.0, to=10.0, variable=score_var, orient="horizontal", length=200)
score_slider.pack(pady=(0, 10))
score_display = ttk.Label(root, textvariable=score_var)
score_display.pack()

# --- 公開年入力 ---
ttk.Label(root, text="📅 公開年（例: 2018）").pack()
entry_year = ttk.Entry(root, width=20)
entry_year.pack(pady=(0, 10))

search_button = ttk.Button(root, text="検索する", command=on_search)
search_button.pack(pady=5)

result_listbox = tk.Listbox(root, width=60, height=15)
result_listbox.pack(pady=10)

root.mainloop()

