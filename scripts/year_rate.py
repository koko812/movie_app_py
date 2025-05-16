import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import japanize_matplotlib


# データ読み込み
@st.cache_data
def load_data():
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()
    return df

st.title("📊 年ごとの映画評価スコアの平均")

df = load_data()

# 年を抽出
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df.dropna(subset=["year", "vote_average"])
df["year"] = df["year"].astype(int)

# スライダーで年の範囲指定
min_year, max_year = df["year"].min(), df["year"].max()
year_range = st.slider("表示する年の範囲", int(min_year), int(max_year), (2000, 2020))

# 年ごとに平均を計算
avg_by_year = df.groupby("year")["vote_average"].mean().reset_index()

# 範囲でフィルタ
avg_by_year = avg_by_year[
    (avg_by_year["year"] >= year_range[0]) & (avg_by_year["year"] <= year_range[1])
]

# グラフ表示
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(avg_by_year["year"], avg_by_year["vote_average"], marker="o")
ax.set_xlabel("公開年")
ax.set_ylabel("平均スコア")
ax.set_title("📈 年ごとの映画評価スコアの平均")
st.pyplot(fig)

