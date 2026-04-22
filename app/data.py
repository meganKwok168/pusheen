import copy
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
mongo = client["database"]

#listing genres
def listGenres():
    genres = {}
    pipeline = { "$group": { "genre": "$content_type", "count": { "$sum": 1 } } }
    aggCursor = mongo.posts.aggregate(pipeline)
    for document in aggCursor:
        genres[document["genre"]] = document["count"]-1
#listGenres()

#finding out what the engagement rate means --> metric used: impressions
def engagementRate():
    results = mongo.posts.find({},
        {
            "engagement_rate": 1,
            "follower_count": 1,
            "reach": 1,
            "impressions": 1,
            "likes": 1,
            "comments": 1,
            "shares": 1,
            "saves": 1
        })
    metrics = ["follower_count", "reach", "impressions"]
    engagements = ["likes","comments","shares","saves"]
    trueRate = document["engagement_rate"]
    bestMetric = ""
    for document in results:
        totalEngagement = 0.0
        for engagement in engagements:
            totalEngagement += document[engagement]
        engagementRate = 0.0
        for metric in metrics:
            tempRate = totalEngagement / document["metric"]
            if (abs(tempRate - trueRate) < abs(engagementRate - trueRate)):
                engagementRate = tempRate
                bestMetric = metric
        print("true: " + trueRate + " | calc'ed: " + round(engagementRate,4) + " | " + bestMetric)
#engagementRate

# return total data metric and average data metric for a certain specification
def makeGraphic(limit1, limit2, specification, metric):
    if limit != "General":
        filterType = limit1
        filter = limit2
        pipeline = [
            { "$match": { filterType: filter } },
            { "$group": { "_id": ("$"+specification), metric: { "$sum": ("$"+metric) } } }
        ]
    else:
        pipeline = [
            { "$group": { "_id": ("$"+specification), metric: { "$sum": ("$"+metric) } } }
        ]
    aggCursor = list(mongo.posts.aggregate(pipeline))
    data = list(aggCursor)
    for document in data:
        document[specification] = document.pop("_id")
        document[metric] = document.pop(metric)

    avgData = copy.deepcopy(data)
    for document in avgData:
        if limit != "General":
            count = mongo.posts.count_documents({filterType: filter, specification: document[specification]})
        else:
            count = mongo.posts.count_documents({specification: document[specification]})
        document[metric] = (document[metric] / count)

    return {"scatter": data, "avg": avgData}
# makeGraphic('General','content_category','reach')

if __name__=="__main__":
    #run file in terminal
    print("run this in flask")
