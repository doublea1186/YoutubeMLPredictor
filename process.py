import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Process():
    def __init__(self, filename):
        continous_name = ['trending_date', 'title', 'channel_title', 'publish_time', 'tags', 'description',
                          'views', 'likes', 'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled']

        self.videos = pd.read_csv(filename)
        self.videos = self.videos[continous_name]

    def encode_categorical(self):
        cat_list = ['trending_date', 'title', 'tags', 'channel_title', 'description', 'publish_time',
                    'comments_disabled', 'ratings_disabled']
        for i in cat_list:
            self.videos[i] = self.videos[i].astype('category')

        keys = [dict(enumerate(self.videos[i].cat.categories)) for i in cat_list]

        for i in keys:
            i = dict(map(reversed, i.items()))

        self.trending_date = keys[0]
        self.title = keys[1]
        self.tags = keys[2]
        self.channel_title = keys[3]
        self.description = keys[4]
        self.publish_time = keys[5]
        self.comments_disabled = keys[6]
        self.ratings_disabled = keys[7]

        cat_columns = self.videos.select_dtypes(['category']).columns
        self.videos[cat_columns] = self.videos[cat_columns].apply(lambda x: x.cat.codes)

    def decode(self, videos):
        videos['trending_date'] = videos['trending_date'].apply(lambda x: self.trending_date.get(x))
        videos['title'] = videos['title'].apply(lambda x: self.title.get(x))
        videos['tags'] = videos['tags'].apply(lambda x: self.tags.get(x))
        videos['channel_title'] = videos['channel_title'].apply(lambda x: self.channel_title.get(x))
        videos['description'] = videos['description'].apply(lambda x: self.description.get(x))
        videos['publish_time'] = videos['publish_time'].apply(lambda x: self.publish_time.get(x))
        videos['comments_disabled'] = videos['comments_disabled'].apply(lambda x: self.comments_disabled.get(x))
        videos['ratings_disabled'] = videos['ratings_disabled'].apply(lambda x: self.ratings_disabled.get(x))

        return videos

    def visualize(self):
        continous_name = ['trending_date', 'title', 'channel_title', 'publish_time', 'tags', 'description',
                          'views', 'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled']

        for x in continous_name:
            figure = plt.figure
            sns.scatterplot(x=self.videos[x], y=self.videos['likes'])
            plt.show()

if __name__ == "__main__":
    x = Process()
    x.__init__()
    x.encode_categorical()
    x.visualize()
