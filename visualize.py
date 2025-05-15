import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def fetch_movies(db_name="movies.db"):
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query("SELECT release_date FROM movies", conn)
    conn.close()
    return df

def plot_movie_count_by_year(df):
    # release_date から年だけを抽出
    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year

    # 年ごとの件数をカウント
    year_counts = df["year"].value_counts().sort_index()

    # プロット
    plt.figure(figsize=(10, 6))
    plt.plot(year_counts.index, year_counts.values, marker="o")
    plt.title("年ごとの映画公開本数")
    plt.xlabel("公開年")
    plt.ylabel("本数")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = fetch_movies()
    plot_movie_count_by_year(df)

