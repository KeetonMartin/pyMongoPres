#Simplest Program

#Note, if one of these lines throws an error you probably need to pip install smth
from pymongo import MongoClient
import pprint
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

import seaborn as sns


CONNECTION_STRING = "mongodb://127.0.0.1:27017/rocket"
# client = MongoClient(CONNECTION_STRING)
client = MongoClient('localhost', 27017)

#Create a database object
hurr_db = client["hurricane"]

#Create a collection object
hurr_collection = hurr_db["Hurricane"]


#Make a new collection and put something in it
#Dictionaries represent documents
prof = {"first":"Geoffrey", "last":"Towell"}

keeton_prof_collection = hurr_db.keeton_prof_collection
keeton_prof_id = keeton_prof_collection.insert_one(prof).inserted_id
print("Inserted a prof into database with id: ", keeton_prof_id)

#Let's see if we made anything happen...
print(hurr_db.list_collection_names())
#Looks like it worked

#What about Retrieving a document?
print("\nGrabbing the first document we see: ")
pprint.pprint(keeton_prof_collection.find_one())

#What if we want to filter? Simple, like regular Mongo
print("\nAre other professors hiding in here somewhere?")
pprint.pprint(keeton_prof_collection.find_one({"first":"Chris"}))

#Of course we can also query by _id, using the var from above

print("Retrieving prof based on _id from earlier in this script run")
pprint.pprint(keeton_prof_collection.find_one({"_id":keeton_prof_id}))
#Note that an ObjectId is not the same as its string representation


#Other pythonic things you can do...
#Insert a list of dictionary objects (which will become documents)
# all at once using collection.insert_many(... list of dictionaries here ...)


#What if we want to find all the profs and put them in pandas?
prof_cursor = keeton_prof_collection.find()
list_from_cur = list(prof_cursor)
profs_df = pd.DataFrame(list_from_cur)

print("How does our DataFrame look?")
print(profs_df)


obs_df = pd.DataFrame(list(hurr_db["Observation"].find()))
print("hurricane head of data: \n", obs_df.head())

print("\nAverage MaxSustained value: ", obs_df["maxsustained"].mean(), "\n")
print("all columns: ", obs_df.columns)
# print("head var: ", obs_df["type"].head())

#You can do lots of things with Pandas Dataframes
plt.hist(obs_df["maxsustained"])
# # plt.show()
plt.savefig('windSpeeds.png')

# obs_df.to_csv("observations.csv")

feature_cols = ["latitude", "longitude", "maxsustained"]
X = obs_df.loc[:, feature_cols]

print("Type possibilities: ", obs_df["type"].unique())
y = pd.get_dummies(obs_df.type)["HU"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

predictions = logreg.predict(X_test)

score = logreg.score(X_test, y_test)
print(score)

cm = metrics.confusion_matrix(y_test, predictions)
print(cm)

plt.figure(figsize=(2,2))
sns.heatmap(cm, annot=True, fmt=".3f", linewidths=.5, square = True, cmap = 'Blues_r');
plt.ylabel('Actual label');
plt.xlabel('Predicted label');
all_sample_title = 'Accuracy Score: {0}'.format(score)
plt.title(all_sample_title, size = 15);

plt.savefig('cm.png')