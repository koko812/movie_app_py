import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import japanize_matplotlib

@st.cache_data
def load_data():
    conn = sqlite3.connect("movies.db")
    query = '''
        SELECT g.name AS genre, m.vote_average
        FROM movies m
        JOIN movie_genres mg ON m.id = mg.movie_id
        JOIN genres g ON mg.genre_id = g.id
        WHERE m.vote_average IS NOT NULL
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.title("🎭 ジャンル別の映画評価スコアの平均")

df = load_data()

# ジャンルごとに平均を集計
genre_avg = df.groupby("genre")["vote_average"].mean().sort_values(ascending=False)

# ジャンル数のスライダー
max_count = len(genre_avg)
top_n = st.slider("表示するジャンル数（上位）", 5, max_count, 10)

# 上位だけ取り出して可視化
genre_avg_top = genre_avg.head(top_n)

fig, ax = plt.subplots(figsize=(10, 6))
genre_avg_top.plot(kind="bar", ax=ax)
ax.set_ylabel("平均評価")
ax.set_xlabel("ジャンル")
ax.set_title("ジャンル別の平均スコア（上位）")
st.pyplot(fig)

