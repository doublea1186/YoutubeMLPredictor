import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import isodate
import numpy as np
import pickle
import requests
import time


def read_and_clean():

    #remove columns with no apparent use
    continous_name = ['trending_date', 'title', 'channel_title', 'publish_time', 'tags',
                      'views', 'likes', 'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled']

    df = pd.read_csv("USVideos.csv")
    df = df.sample(frac=1).reset_index(drop=True)

    my_data = df[continous_name]

    #Get rid of data without ratings
    my_data = my_data[my_data.ratings_disabled != True]

    my_data["duration"] = my_data.duration.apply(lambda x: isodate.parse_duration(x).total_seconds())

    return my_data


# Proves more views = more likes therefore is a good indicator of video popularity
def compare_likes_and_views(videos):
    corrolation_list = ['views', 'likes', 'dislikes', 'comment_count']
    data = videos[corrolation_list].corr()
    sns.scatterplot(x=videos['views'], y=videos['likes'])
    plt.show()
    # to get a closer look at the scatterplot for likes/views

# Simple standard recommendation system only by popularity. Used as a benchmark
def recommend_by_popularity(videos):
    popular = videos.sort_values('likes', ascending=False)
    grouped_videos = popular.groupby('title')['likes'].mean().sort_values(ascending=False)
    grouped_videos = pd.DataFrame({'title': grouped_videos.index, 'likes': grouped_videos.values})

    return grouped_videos['title'].head(10)


if __name__ == "__main__":
    data = read_and_clean()
    # popular = compare_likes_and_views(data)
