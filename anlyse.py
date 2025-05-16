import streamlit as st
import pandas as pd
import sqlite3

# DB からデータ取得
@st.cache_data
def load_data():
    conn = sqlite3.connect("movies.db")
    df = pd.read_sql_query("SELECT * FROM movies", conn)
    conn.close()
    return df

st.title("🎬 映画データ可視化アプリ")

df = load_data()

# 評価スコアでフィルター
score = st.slider("最低評価スコア", 0.0, 10.0, 7.0)
filtered_df = df[df["vote_average"] >= score]

st.write(f"{len(filtered_df)} 本の映画が見つかりました")
st.dataframe(filtered_df[["title", "release_date", "vote_average"]])

