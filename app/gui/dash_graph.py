import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import pandas as pd

# データ
df = pd.DataFrame({
    "year": list(range(2000, 2021)),
    "score": [7 + 0.1 * i for i in range(21)],
    "count": [5 + i % 5 for i in range(21)]
})

# Dash アプリ初期化
app = dash.Dash(__name__)

# レイアウト
app.layout = html.Div([
    html.H1("📊 Dashで作るインタラクティブグラフ"),
    dcc.Graph(id='my-graph'),
    dcc.Dropdown(
        id='color-select',
        options=[
            {'label': 'Blue', 'value': 'blue'},
            {'label': 'Red', 'value': 'red'},
            {'label': 'Green', 'value': 'green'}
        ],
        value='blue',
        clearable=False
    )
])

# コールバック（動的にグラフを更新）
@app.callback(
    Output('my-graph', 'figure'),
    Input('color-select', 'value')
)
def update_graph(selected_color):
    fig = go.Figure()

    # ライン
    fig.add_trace(go.Scatter(x=df["year"], y=df["score"], mode='lines+markers', name="スコア", line=dict(color=selected_color)))
    # 本数バー
    fig.add_trace(go.Bar(x=df["year"], y=df["count"], name="本数", opacity=0.4))

    fig.update_layout(
        title="スコアと映画本数（クリックで色変わる）",
        yaxis_title="スコア",
        yaxis2=dict(title="本数", overlaying='y', side='right')
    )
    return fig

# 実行
if __name__ == '__main__':
    app.run(debug=True)

