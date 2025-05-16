import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import japanize_matplotlib

#@st.cache_data
def load_data():
    conn = sqlite3.connect("movies.db")
    query = '''
        SELECT g.name AS genre, m.vote_average, m.release_date
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
        WHERE m.vote_average IS NOT NULL
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("📈 年代ごとのジャンル別スコア推移")

df = load_data()
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df.dropna(subset=["year", "vote_average", "genre"])
df["year"] = df["year"].astype(int)

# 年範囲指定
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.slider("表示する年の範囲", min_year, max_year, (2000, 2020))

# 表示するジャンル選択（複数可）
all_genres = sorted(df["genre"].unique())
selected_genres = st.multiselect("表示するジャンルを選んでね", all_genres, default=all_genres[:5])

# フィルタ
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["genre"].isin(selected_genres))
]

# 集計：ジャンル×年で平均スコア
grouped = filtered_df.groupby(["year", "genre"])["vote_average"].mean().reset_index()
pivot = grouped.pivot(index="year", columns="genre", values="vote_average")

# --- すでにある部分 ---
grouped = filtered_df.groupby(["year", "genre"])["vote_average"].mean().reset_index()
pivot = grouped.pivot(index="year", columns="genre", values="vote_average")

# 年ごとの映画数をジャンルごとに集計
count_grouped = filtered_df.groupby(["year", "genre"]).size().reset_index(name="movie_count")
count_pivot = count_grouped.pivot(index="year", columns="genre", values="movie_count")

# --- 描画 ---
fig, ax1 = plt.subplots(figsize=(12, 6))

# 評価スコア（左軸）
pivot.plot(ax=ax1)
ax1.set_xlabel("公開年")
ax1.set_ylabel("平均スコア")
ax1.set_title("ジャンル別の平均評価スコアと映画本数の推移")

# 映画本数（右軸）を破線グラフで重ねる
ax2 = ax1.twinx()
count_pivot.plot(ax=ax2, linestyle="--", alpha=0.3)
ax2.set_ylabel("映画本数")

# 凡例調整
ax1.legend(title="ジャンル（スコア）", loc="upper left")
ax2.legend(title="ジャンル（本数）", loc="upper right")

st.pyplot(fig)


