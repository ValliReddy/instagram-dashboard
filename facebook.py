import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import random
import json

app = dash.Dash(__name__)
app.title = "Facebook Real-Time Dashboard"

# Simulated post content
post_types = ['Status', 'Photo', 'Video', 'Link']
topics = ['🎉 Party', '📚 Study', '🏖️ Vacation', '🚰 Project', '🐶 Dog pic', '📈 Stocks', '🍔 Lunch', '🏃 Fitness']
pages = ['TechNews', 'HappyPaws', 'GlobalEvents', 'TravelNow', 'FoodieLife', 'FitnessHub']

# Tracking post IDs
post_ids_seen = set()

# Initial DataFrame
df = pd.DataFrame(columns=['PostID', 'Time', 'Page', 'PostType', 'Message', 'Likes', 'Shares', 'Comments', 'Followers'])

# Layout
app.layout = html.Div(style={'backgroundColor': '#111', 'color': 'white', 'padding': '10px'}, children=[
    html.H1("📘 Real-Time Facebook API Dashboard", style={'textAlign': 'center'}),

    dcc.Interval(id='interval', interval=1000, n_intervals=0),

    html.H3("📥 Incoming Facebook Data Feed", style={'marginTop': '20px'}),
    html.Pre(id='raw-data', style={
        'backgroundColor': '#222',
        'padding': '10px',
        'overflowY': 'scroll',
        'height': '220px',
        'borderRadius': '10px',
        'color': '#0f0',
        'fontSize': '12px'
    }),

    html.Div([
        dcc.Graph(id='likes-line', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='engagement-bar', style={'display': 'inline-block', 'width': '49%'}),
    ]),

    html.Div([
        dcc.Graph(id='followers-area', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='posttype-pie', style={'display': 'inline-block', 'width': '49%'}),
    ]),

    html.Div([
        dcc.Graph(id='posttype-bar', style={'width': '98%'})
    ])
])

@app.callback(
    Output('likes-line', 'figure'),
    Output('engagement-bar', 'figure'),
    Output('followers-area', 'figure'),
    Output('posttype-pie', 'figure'),
    Output('posttype-bar', 'figure'),
    Output('raw-data', 'children'),
    Input('interval', 'n_intervals')
)
def update_charts(n):
    global df, post_ids_seen

    while True:
        post_id = f"FB_{random.randint(10000, 99999)}"
        if post_id not in post_ids_seen:
            post_ids_seen.add(post_id)
            break

    now = datetime.datetime.now().strftime('%H:%M:%S')
    base = random.randint(10, 100)
    trend_boost = 5 if n % 10 == 0 else 1

    likes = random.randint(100, 400) + base * trend_boost
    shares = random.randint(30, 150) + base
    comments = random.randint(20, 100) + base
    followers = 5000 + n * random.randint(10, 30)

    page = random.choice(pages)
    post_type = random.choice(post_types)
    message = random.choice(topics)

    new_data = {
        'PostID': post_id,
        'Time': now,
        'Page': page,
        'PostType': post_type,
        'Message': message,
        'Likes': likes,
        'Shares': shares,
        'Comments': comments,
        'Followers': followers
    }

    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True).tail(50)

    # Likes Line Chart
    likes_fig = go.Figure()
    likes_fig.add_trace(go.Scatter(x=df['Time'], y=df['Likes'], mode='lines+markers', line=dict(color='blue'), name='Likes'))
    likes_fig.update_layout(title='👍 Likes Over Time', template='plotly_dark')

    # Engagement Bar Chart
    engagement_fig = go.Figure()
    engagement_fig.add_trace(go.Bar(x=df['Time'], y=df['Shares'], name='🔁 Shares'))
    engagement_fig.add_trace(go.Bar(x=df['Time'], y=df['Comments'], name='💬 Comments'))
    engagement_fig.update_layout(barmode='group', title='📣 Engagements', template='plotly_dark')

    # Follower Area Chart
    follower_fig = go.Figure()
    follower_fig.add_trace(go.Scatter(x=df['Time'], y=df['Followers'], fill='tozeroy', line=dict(color='green'), name='Followers'))
    follower_fig.update_layout(title='👥 Followers Growth', template='plotly_dark')

    # Post Type Pie Chart
    type_counts = df['PostType'].value_counts()
    pie_fig = go.Figure(data=[go.Pie(labels=type_counts.index, values=type_counts.values, hole=0.3)])
    pie_fig.update_layout(title='📃 Post Types Distribution', template='plotly_dark')

    # Post Type Bar Chart
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=type_counts.index, y=type_counts.values, marker_color='orange'))
    bar_fig.update_layout(title='📊 Post Type Frequency', template='plotly_dark')

    # JSON Feed
    raw_json = json.dumps(new_data, indent=4)

    return likes_fig, engagement_fig, follower_fig, pie_fig, bar_fig, raw_json

if __name__ == '__main__':
    app.run(debug=True)