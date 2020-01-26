import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import pickle
import matplotlib.pyplot as plt



# columns = ['categoryId', 'channel_subscriberCount', 'definition', 'likeCount', 'dislikeCount', 'viewCount', 'commentCount', 'viewCount/monthOld', 'viewCount/channel_month_old', 'viewCount/video_month_old', 'viewCount/http_in_descp', 'viewCount/NoOfTags', 'viewCount/tags_in_desc', 'social_links', 'subscriberCount/videoCount', 'channelViewCount/channeVideoCount', 'channelViewCount/socialLink']
from sklearn.preprocessing import LabelEncoder

continous_name = ['video_id','trending_date','title','channel_title','category_id','publish_time','tags','views',
                  'likes','dislikes','comment_count','comments_disabled','ratings_disabled']


df = pd.read_csv("USVideos.csv")
df = df.sample(frac=1).reset_index(drop=True)

Y = df.likes
X= df[continous_name]

pipeline=  Pipeline([
                    ('clf',RandomForestRegressor())
                    ])
#
parameters={
    'clf__n_estimators':([150,200]),
    'clf__max_depth':([15,25,30]),
    'clf__min_samples_split':([5,15,10]),
    'clf__min_samples_leaf':([2,5])
}

grid_search = GridSearchCV(pipeline,parameters,n_jobs=4,verbose=1,scoring="r2")

le = LabelEncoder()
le.fit(grid_search['Sex'].astype(str))
normdf[c] = le.transform(train_X['Sex'].astype(str))
grid_search.fit(X,Y)

print("Best score:",grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()

for param_name in sorted(parameters.keys()):
    print (param_name,best_parameters[param_name])