pip install pymongo
pip install kagglehub[pandas-datasets]

from pymongo import MongoClient
import kagglehub
from kagglehub import KaggleDatasetAdapter

mongo = MongoClient("mongodb://localhost:27017")

mongo.create_collection("users", {
    account_id: <number>,
    account_type: <string>,
    follower_count: <number>,
    posts: <
})
mongo.create_collection("creators")
mongo.create_collection("posts")



# Set the path to the file you'd like to load
file_path = "Instagram_Analytics.csv"

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "kundanbedmutha/instagram-analytics-dataset",
  file_path,
)

docs = []
for data in df.itertuples(index=False):
    docs.append({
        "": data[0],
    })
if docs:
    mongo.posts.insert_many(docs)
