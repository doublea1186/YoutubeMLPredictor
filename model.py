import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, cross_val_score
import time

# Custom import
from process import Process

start_time = time.time()
process = Process("USVideos.csv")
process1 = Process("CAvideos.csv")
process.encode_categorical()
process1.encode_categorical()
df = process.videos
df1 = process1.videos
df = df.sample(frac=1).reset_index(drop=True)
df1 = df1.sample(frac=1).reset_index(drop=True)
continous_name = ['trending_date', 'title', 'channel_title', 'publish_time', 'tags', 'description',
                  'views', 'dislikes', 'comment_count', 'comments_disabled', 'ratings_disabled']

# Making the training and test set
X = df[continous_name]
X1 = df1[continous_name]
print("Training Set Shape", X.shape)
Y = df[['likes']].values.flatten()
Y1 = df1[['likes']].values.flatten()
print("Testing Set Shape", Y.shape)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)  # create the training set and the testing set
print("Training in progress.....")
# parameters
n_estimators = 200
max_depth = 25
min_samples_split = 15
min_samples_leaf = 2

# # Random forest classifier
clf = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, min_samples_split=min_samples_split,
                            min_samples_leaf=min_samples_leaf)

# # It is trained of 2 Epochs
x_train = np.concatenate((X, X), axis=0)
y_train = np.concatenate((Y, Y), axis=0)
clf.fit(x_train, y_train)

like_estimate = clf.predict(x_train)  # switch x_train with X1 to predict for the CA videos data
feature_imp = pd.Series(clf.feature_importances_, index=continous_name).sort_values(ascending=False)

np.set_printoptions(suppress=True)
pred = np.ceil(clf.predict(X1))
org = np.array(y_test).astype("float32")

print("R^2 Score : ", 100 * clf.score(x_train, y_train))
print(feature_imp)
print("--- %s seconds ---" % (time.time() - start_time))