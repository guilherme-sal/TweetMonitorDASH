import configparser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from aux_functions import request_all_tweets_as_df, group_df_by_date, filter_df_by_date, filter_df_by_search_input, \
    filter_df_by_language
from div_generator import generate_photo_gallery, generate_date_graph_figure_dict, generate_hashtag_graph_figure_dict, \
    generate_tweet_cards_group

config = configparser.ConfigParser()
config.read('config')
ui_url = config['UI']['url']
api_url = config['API']['url']

# APP INIT
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'TweetMonitor - Dashboard'
server = app.server

# APP LAYOUT
colors = {'bg': '#212529', 'green': '#198754', 'white': '#e0dcdb'}

# GLOBAL VAR
df_base = request_all_tweets_as_df(api_url)
df_base = df_base.drop_duplicates(subset=['id'])
df_base['date'] = [str(i).split(' ')[0].strip() for i in df_base['date']]

app.layout = html.Div(
    style={'position': 'absolute', 'top': '0px', 'right': '0px', 'left': '0px',
           'background-color': colors['bg'], 'border': '1px solid', 'border-color': colors['green']},
    children=[

        # Navbar
        html.Div(children=[
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(children=[dbc.NavLink("UI", href=ui_url)]),
                ],

                brand="Tweet Monitor - Dashboard",
                color=colors['green'],
                dark=True, )]),

        dbc.Row(style={'width': '100%', 'margin': '20px', 'padding': '20px', 'border': '1px solid'},
                children=[
                    html.Div(style={'color': colors['green'], 'padding': '5px', 'margin-top': '20px'},
                             children=[dcc.DatePickerRange(
                                 id='my-date-picker-range',
                                 min_date_allowed=df_base['date'].min(),
                                 max_date_allowed=df_base['date'].max(),
                                 start_date=df_base['date'].min(),
                                 end_date=df_base['date'].max(),
                                 start_date_placeholder_text=df_base['date'].min(),
                                 end_date_placeholder_text=df_base['date'].max(), ),

                                 dbc.Input(style={'color': colors['green'], 'margin-top': '10px'},
                                           id="search_input", type="text", placeholder="#Amazônia", debounce=False),

                                 dcc.RadioItems(style={'color': colors['green'], 'margin-top': '10px', 'padding': '1px'},
                                                id='language_selector',
                                                options=[
                                                    {'label': 'All languages  ', 'value': 'None'},
                                                    {'label': 'Portuguese  ', 'value': 'pt'},
                                                    {'label': 'English  ', 'value': 'en'},
                                                ],
                                                value='None',
                                                labelStyle={'display': 'inline-block'},
                                                inputStyle={'margin-left': '3px'},
                                                )
                             ]),
                    # Photo gallery
                    html.Div(style={'margin': '20px', 'padding': '2px', 'border': '1px solid',
                                    'border-color': colors['bg'], 'display': 'inline-block'},
                             id='photo_gallery'
                             )

                ]),
        ### SECOND ROW
        dbc.Row(style={'width': '100%', 'margin': '20px', 'padding': '20px', 'border': '1px solid'},
                children=[
                    # Date graph
                    html.Div(style={'height': '30%', 'width': '47%', 'margin': '20px', 'padding': '2px',
                                    'border': '1px solid',
                                    'border-color': colors['bg']},
                             children=[
                                 dcc.Graph(style={'background-color': colors['bg']},
                                           id='date_graph'),
                             ]),
                    # Hashtag graph
                    html.Div(style={'height': '30%', 'width': '47%', 'margin': '20px', 'padding': '1px',
                                    'border': '1px solid',
                                    'border-color': colors['bg'], 'display': 'inline-block'},
                             children=[
                                 dcc.Graph(style={'background-color': colors['bg']},
                                           id='hashtag_graph'),
                             ]),
                ]),

        ### THIRD ROW
        dbc.Row(style={'width': '100%', 'margin': '20px', 'padding': '20px', 'border': '1px solid'},
                children=[
                    # Tweet Cards
                    html.Div(style={'margin': '20px', 'padding': '2px', 'border': '1px solid',
                                    'border-color': colors['bg'], 'display': 'inline-block'},
                             id='tweet_cards', ),

                ]),

    ])


# APP CALLBACK
@app.callback(
    [Output('photo_gallery', 'children'),
     Output('date_graph', 'figure'),
     Output('hashtag_graph', 'figure'),
     Output('tweet_cards', 'children'),
     ],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date'),
     Input('search_input', 'value'),
     Input('language_selector', 'value')
     ])
def update_output(start_date, end_date, search_input=None, language_selector='None'):
    df = filter_df_by_date(df_base, start_date, end_date)
    if search_input:
        df = filter_df_by_search_input(df, search_input)

    if language_selector != 'None':
        df = filter_df_by_language(df, language_selector)

    df_grouped = group_df_by_date(df)

    # PHOTO GALLERY
    img_list = generate_photo_gallery(df)

    # DATE GRAPH
    date_graph_figure_dict = generate_date_graph_figure_dict(df_grouped)

    # HASHTAG GRAPH
    hashtag_graph_figure_dict = generate_hashtag_graph_figure_dict(df)

    # TWEETS CARD
    card_group = generate_tweet_cards_group(df)

    return img_list, date_graph_figure_dict, hashtag_graph_figure_dict, card_group


# APP RUN
if __name__ == "__main__":
    app.run_server(debug=True)
