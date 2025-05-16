import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# データロード
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

st.title("🎬 ジャンル別の評価スコアと映画本数 (インタラクティブ版)")

df = load_data()
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df.dropna(subset=["year", "vote_average", "genre"])
df["year"] = df["year"].astype(int)

# 年・ジャンル選択
min_year, max_year = df["year"].min(), df["year"].max()
year_range = st.slider("表示する年の範囲", int(min_year), int(max_year), (2000, 2020))
all_genres = sorted(df["genre"].unique())
selected_genres = st.multiselect("表示するジャンルを選んでね", all_genres, default=all_genres[:5])

# フィルタ
filtered_df = df[
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1]) &
    (df["genre"].isin(selected_genres))
]

# 平均スコア
grouped = filtered_df.groupby(["year", "genre"])["vote_average"].mean().reset_index()
# 映画本数
count_grouped = filtered_df.groupby(["year", "genre"]).size().reset_index(name="movie_count")

# Plotlyで2軸グラフ作成
fig = make_subplots(specs=[[{"secondary_y": True}]])
for genre in selected_genres:
    # スコアライン
    genre_data = grouped[grouped["genre"] == genre]
    fig.add_trace(
        go.Scatter(
            x=genre_data["year"],
            y=genre_data["vote_average"],
            mode="lines+markers",
            name=f"{genre}（スコア）"
        ),
        secondary_y=False
    )

    # 本数バー
    genre_count = count_grouped[count_grouped["genre"] == genre]
    fig.add_trace(
        go.Bar(
            x=genre_count["year"],
            y=genre_count["movie_count"],
            name=f"{genre}（本数）",
            opacity=0.4
        ),
        secondary_y=True
    )

fig.update_layout(
    title="ジャンル別の平均評価スコアと映画本数（インタラクティブ）",
    hovermode="x unified"
)
fig.update_yaxes(title_text="平均スコア", secondary_y=False)
fig.update_yaxes(title_text="映画本数", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

