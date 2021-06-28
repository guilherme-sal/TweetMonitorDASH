import random
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from aux_functions import generate_list_of_images, generate_df_hashtags, generate_retweets_df

# APP LAYOUT
colors = {'bg': '#212529', 'green': '#198754', 'white': '#e0dcdb'}


def generate_photo_gallery(df):
    list_of_images = generate_list_of_images(df)
    img_html_list = []

    link_unique_values = []
    for link in list_of_images:
        if link not in link_unique_values:
            link_unique_values.append(link)

    for link in link_unique_values[:10]:
        html_comp = html.A(href=f"{link}", children=html.Img(src=f"{link}:thumb"))
        img_html_list.append(html_comp)

    return img_html_list


def generate_date_graph_figure_dict(df):
    date_graph_linetraces = []
    for username in df['username'].unique():
        df_by_username = df[df['username'] == username]
        date_graph_linetraces.append(go.Scatter(
            x=df_by_username['date'],
            y=df_by_username['count'],
            text=df_by_username['username'],
            mode='markers',
            opacity=0.7,
            marker={'size': 15},
            name=username
        ))

    figure_dict = {
        'data': date_graph_linetraces,
        'layout': go.Layout(
            xaxis={'title': ''},
            yaxis={'title': ''},
            hovermode='closest',
            plot_bgcolor=colors['bg'],
            paper_bgcolor=colors['bg'],
            font={'color': colors['white'],
                  'size': 15},
            title_text=''
        )
    }

    return figure_dict


def generate_hashtag_graph_figure_dict(df):

    df_hashtag = generate_df_hashtags(df)

    traces_hashtag = go.Scatter(
        x=df_hashtag['X'],
        y=df_hashtag['Y'],
        text=df_hashtag['hashtag'],
        mode='markers+text',
        hoverinfo='text',
        opacity=1,
        marker={'size': df_hashtag['count'],
                'color': random.sample(range(0, 10, 1), 10),
                'colorscale': 'rainbow',
                'sizeref': max(df_hashtag['count'])/100},

    )

    hashtag_graph_figure_dict = {
        'data': [traces_hashtag],
        'layout': go.Layout(
            xaxis={'title': '',
                   'visible': False},
            yaxis={'title': '',
                   'visible': False},
            hovermode='closest',
            plot_bgcolor=colors['bg'],
            paper_bgcolor=colors['bg'],
            font={'color': colors['white'],
                  'size': 20},
            title_text='',


        )}
    return hashtag_graph_figure_dict

def generate_tweet_cards_group(df):

    df_tweets = generate_retweets_df(df)

    lista_de_tweets = []
    for tweet in df_tweets.iterrows():
        card = dbc.Card([dbc.CardHeader(children=[str(tweet[1]['date'])[:10],
                                                  dbc.Badge(tweet[1]['nretweets'], color="light", className="ml-1")]),
                dbc.CardBody(
                    [
                        html.H5(tweet[1]['username'], className="card-title"),
                        html.P(
                            tweet[1]['tweet'],
                            className="card-text",
                        )
                    ]
                )], color=colors['bg'], inverse=True,)
        lista_de_tweets.append(card)
    card_group = dbc.CardGroup(lista_de_tweets)

    return card_group
