#pip install pymongo
#pip install kagglehub[pandas-datasets]

from pymongo import MongoClient
import kagglehub
from kagglehub import KaggleDatasetAdapter

client = MongoClient("mongodb://localhost:27017")
mongo = client["database"]

mongo.drop_collection("users")
mongo.drop_collection("creators")
mongo.drop_collection("posts")

mongo.create_collection("users")
mongo.create_collection("creators")
mongo.create_collection("posts")



# Set the path to the file you'd like to load
file_path = "Instagram_Analytics.csv"

# Load the latest version
df = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "kundanbedmutha/instagram-analytics-dataset",
  file_path,
)

for data in df.itertuples(index=False):
    mongo.creators.update_one(
        { "_id": data[1] },
        {
            "$push": { "posts": data[0] },
            "$setOnInsert": {
                "_id": data[1],
                "account_type": data[2],
                "follower_count": data[3]
            }
        },
        upsert=True
    )

    mongo.posts.insert_one(
        {
            "_id": data[0],
            "account_id": data[1],
            "media_type": data[4],
            "content_category": data[5],
            "traffic_source": data[6],
            "has_call_to_action": data[7],
            "likes": data[12],
            "comments": data[13],
            "shares": data[14],
            "saves": data[15],
            "reach": data[16],
            "impressions": data[17],
            "engagement_rate": data[18],
            "followers_gained": data[19],
            "caption_length": data[20],
            "hashtags_count": data[21],
            "performace_bucket": data[22],
            "post_datetime": data[8],
            "post_date": data[9],
            "post_hour": data[10],
            "day_of_week": data[11]
        }
    )
