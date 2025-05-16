import dash
from dash import dcc, html, Output, Input
import plotly.graph_objects as go
import pandas as pd

df = pd.DataFrame({
    "year": list(range(2000, 2021)),
    "score": [7 + 0.1 * i for i in range(21)],
    "count": [5 + i % 5 for i in range(21)]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("🎨 Dash クリックでハイライト"),
    dcc.Graph(id='highlight-graph'),
    dcc.Dropdown(
        id='highlight-select',
        options=[
            {'label': 'スコア', 'value': 'score'},
            {'label': '本数', 'value': 'count'}
        ],
        value='score',
        clearable=False
    )
])

@app.callback(
    Output('highlight-graph', 'figure'),
    Input('highlight-select', 'value')
)
def update_graph(highlight_target):
    fig = go.Figure()

    # スコアライン（強調 or グレー）
    line_color = 'blue' if highlight_target == 'score' else 'lightgray'
    fig.add_trace(go.Scatter(x=df["year"], y=df["score"], mode='lines+markers', name="スコア", line=dict(color=line_color)))

    # 本数バー（強調 or グレー）
    bar_color = 'salmon' if highlight_target == 'count' else 'lightgray'
    fig.add_trace(go.Bar(x=df["year"], y=df["count"], name="本数", opacity=0.4, marker_color=bar_color))

    fig.update_layout(
        title="クリックで強調ハイライト切り替え",
        hovermode="x unified"
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)

