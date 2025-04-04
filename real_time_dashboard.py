import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
import random
import json

# Initialize app
app = dash.Dash(__name__)
app.title = "Instagram Real-Time Dashboard"

# Content pools
content_types = [
    'Photo', 'Video', 'Reel', 'Story', 'Carousel', 'Live', 'IGTV', 'Clip'
]

hashtag_combos = [
    "#travel #sunset", "#foodie #delicious", "#fashion #ootd", "#gym #fitlife",
    "#music #vibes", "#nature #hike", "#pets #doglover", "#selfie #me", "#tech #coding",
    "#coffee #morning", "#beachlife #waves", "#wanderlust #explore", "#art #creative",
    "#motivation #goals", "#love #life", "#happy #smile", "#friends #fun", "#weekend #vibes",
    "#adventure #outdoors", "#style #inspo", "#design #minimal", "#codinglife #developer",
    "#gaming #streamer", "#education #learning", "#startup #hustle", "#photooftheday",
    "#memes #funny", "#quotes #mindset", "#books #reading", "#family #bond",
    "#health #wellness", "#cars #drive", "#citylife #urban", "#fitness #lifestyle"
]

caption_prefixes = [
    "Enjoying", "Loving", "Working on", "Excited about", "Spending time with", "Can't get enough of",
    "Here's to", "A little throwback to", "Currently obsessed with", "In love with",
    "My favorite moment from", "Look what I found in", "So proud of", "Chasing", "Sharing my day at"
]

caption_subjects = [
    "this view 🌄", "my new setup 💻", "delicious lunch 🍝", "sunset drive 🚗", "coding session ☕",
    "friends and laughs 🎉", "a moment of peace 🧘", "my fur baby 🐶", "street vibes 🏙️",
    "bookworm mode 📚", "fitness grind 🏋️", "random thoughts 🤯", "cozy vibes 🛋️", "travel snaps ✈️",
    "mountain air ⛰️", "beach breeze 🌊", "crazy weekend 🎊", "new drip 👟", "the process 🛠️",
    "late night grind 🌙", "minimalist goals 🎯", "this design 🎨", "good energy 💫"
]

fake_usernames = [
    "user_zeno", "cam_travels", "fit_n_fab", "coffee_addict", "urban_journals", "hacker_daily",
    "theartsytype", "bookaholic88", "explorer_max", "vibes_only", "daily.dev", "doggydaze", "humor_hub"
]

post_ids_seen = set()

# Empty dataframe
df = pd.DataFrame(columns=[
    'PostID', 'Username', 'Time', 'Caption', 'Likes', 'Comments',
    'Shares', 'Followers', 'ContentType', 'Hashtag'
])

# Layout
app.layout = html.Div(style={'backgroundColor': '#111', 'color': 'white', 'padding': '10px'}, children=[
    dcc.Interval(id='interval', interval=1000, n_intervals=0),

    html.Div([
        dcc.Graph(id='likes-line', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='engagement-bar', style={'display': 'inline-block', 'width': '49%'}),
    ]),

    html.Div([
        dcc.Graph(id='follower-area', style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(id='content-pie', style={'display': 'inline-block', 'width': '49%'}),
    ]),

    html.H3("📥 Incoming Instagram Data Feed", style={'marginTop': '40px'}),
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
        dcc.Graph(id='hashtag-bar', style={'display': 'inline-block', 'width': '98%'})
    ])
])

@app.callback(
    Output('likes-line', 'figure'),
    Output('engagement-bar', 'figure'),
    Output('follower-area', 'figure'),
    Output('content-pie', 'figure'),
    Output('hashtag-bar', 'figure'),
    Output('raw-data', 'children'),
    Input('interval', 'n_intervals')
)
def update_charts(n):
    global df, post_ids_seen

    # Unique post ID
    while True:
        post_id = f"IG_{random.randint(10000, 99999)}"
        if post_id not in post_ids_seen:
            post_ids_seen.add(post_id)
            break

    username = random.choice(fake_usernames)
    now = datetime.datetime.now().strftime('%H:%M:%S')
    minute = datetime.datetime.now().minute
    base = random.randint(1, 5)
    trend_boost = 5 if minute % 5 == 0 else 1

    new_likes = random.randint(100, 300) + base * trend_boost
    new_comments = random.randint(30, 100) + base
    new_shares = random.randint(10, 60) + base
    followers = 10000 + n * random.randint(20, 50) + base * 5
    hashtag = random.choice(hashtag_combos)
    caption = f"{random.choice(caption_prefixes)} {random.choice(caption_subjects)}"
    content = random.choice(content_types)

    new_data = {
        'PostID': post_id,
        'Username': username,
        'Time': now,
        'Caption': caption,
        'Likes': new_likes,
        'Comments': new_comments,
        'Shares': new_shares,
        'Followers': followers,
        'ContentType': content,
        'Hashtag': hashtag
    }

    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True).tail(40)

    # Likes Line Chart
    likes_fig = go.Figure()
    likes_fig.add_trace(go.Scatter(
        x=df['Time'], y=df['Likes'], mode='lines+markers',
        line=dict(color='red'), name='Likes'
    ))
    likes_fig.update_layout(title='❤️ Likes Over Time', template='plotly_dark')

    # Engagement Bar Chart (last 10 posts)
    engagement_fig = go.Figure()
    recent_df = df.tail(10)
    engagement_fig.add_trace(go.Bar(x=recent_df['Time'], y=recent_df['Comments'], name='💬 Comments'))
    engagement_fig.add_trace(go.Bar(x=recent_df['Time'], y=recent_df['Shares'], name='🔁 Shares'))
    engagement_fig.update_layout(barmode='group', title='📣 Engagements ', template='plotly_dark')

    # Followers Area Chart
    follower_fig = go.Figure()
    follower_fig.add_trace(go.Scatter(
        x=df['Time'], y=df['Followers'], fill='tozeroy',
        line=dict(color='green'), name='Followers'
    ))
    follower_fig.update_layout(title='👥 Follower Growth', template='plotly_dark')

    # Content Type Pie Chart
    content_counts = df['ContentType'].value_counts()
    pie_fig = go.Figure(data=[go.Pie(labels=content_counts.index, values=content_counts.values, hole=0.3)])
    pie_fig.update_layout(title='📂 Content Types', template='plotly_dark')

    # Hashtag Bar Chart (Top 7)
    hashtag_counts = df['Hashtag'].value_counts().nlargest(7)
    hashtag_fig = go.Figure()
    hashtag_fig.add_trace(go.Bar(x=hashtag_counts.index, y=hashtag_counts.values, marker_color='violet'))
    hashtag_fig.update_layout(title='🏷️ Hashtag Frequency', template='plotly_dark')

    # Show latest new data in JSON format
    raw_json = json.dumps(new_data, indent=4)

    return likes_fig, engagement_fig, follower_fig, pie_fig, hashtag_fig, raw_json

# Run app
if __name__ == '__main__':
    app.run(debug=True)
