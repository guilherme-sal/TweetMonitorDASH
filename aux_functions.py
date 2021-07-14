import requests
import pandas as pd
import random
from collections import Counter


def request_all_tweets_as_df(api_url):
    try:
        json = requests.get(api_url + '/tweets').json()
        data_frame = json['Dataframe']
        df = pd.DataFrame.from_dict(data_frame, orient='index')

        return df

    except Exception as e:
        return None


def group_df_by_date(df):
    try:
        df['count'] = 1
        df_grouped_by_date = df.groupby(['date', 'username'])[['count']].sum()
        df_grouped_by_date = df_grouped_by_date.reset_index()
        return df_grouped_by_date
    except Exception as e:
        return None


def filter_df_by_date(df, start_date, end_date):
    df = df[df['date'] >= start_date]
    df = df[df['date'] <= end_date]
    return df


def filter_df_by_search_input(df, search):
    search_boolean = []
    for tweet in df['tweet']:
        if search in tweet:
            search_boolean.append(True)
        else:
            search_boolean.append(False)
    df['search'] = search_boolean
    df = df.query('search == True')
    return df


def generate_list_of_images(df):
    df = df.sort_values('nretweets', ascending=False)
    list_of_img_links = []

    for img_str in df['photos']:
        if img_str == '[]':
            pass
        else:
            img_list = img_str.replace("[", "").replace("]", "").replace("'","").split(",")
            for img in img_list:
                list_of_img_links.append(img.strip())
    return list_of_img_links


def generate_df_hashtags(df):

    size = 20

    list_of_hashtags = []

    for tweet in df['tweet']:
        hashtag_list = [i for i in tweet.split() if i.startswith("#")]
        for hashtag in hashtag_list:
            list_of_hashtags.append(hashtag)

    hashtags_dict = Counter(list_of_hashtags)
    df_hashtags = pd.DataFrame(hashtags_dict, index=[0]).T.reset_index().rename(columns={
        "index": "hashtag", 0: "count"}).sort_values('count', ascending=False).head(size)

    return df_hashtags


def generate_retweets_df(df):

    df_retweets = df[['username', 'tweet', 'nretweets', 'date']]
    df_retweets = df_retweets.sort_values('nretweets', ascending=False).head(8)
    return df_retweets


