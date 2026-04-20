#import csv
#from decimal import Decimal
import pandas as pd

instaCSV = pd.read_csv('static/insta.csv')

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
mongo = client["database"]

#listing genres
#def listGenres():
#    genres = {}
#    with open('static/insta.csv', newline='') as f:
#        reader = csv.DictReader(f)
#       for row in reader:
#            genre = row['content_category']
#            print(genre)
#            if genre not in genres:
#                genres[genre] = 0
#            genres[genre] += 1
#    print(genres)
#listGenres()

def listGenres():
    genres = {}
    pipeline = { "$group": { "genre": "$content_type", "count": { "$sum": 1 } } }
    aggCursor = mongo.posts.aggregate(pipeline)
    for document in aggCursor:
        genres[document["genre"]] = document["count"]-1
#listGenres()

#finding out what the engagement rate means --> metric used: impressions
# def engagementRate():
#     with open('static/insta.csv', newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             trueRate = Decimal(row['engagement_rate'])
#             metrics = ['follower_count', 'reach', 'impressions']
#             engagements = ['likes','comments','shares','saves']
#             totalEngagement = 0.0
#             engagementRate = 5
#             whichOne = ''
#             for e in engagements:
#                 totalEngagement += int(row[e])
#             for m in metrics:
#                 metric = int(row[m])
#                 temp = Decimal(totalEngagement/metric)
#                 if (abs(temp-trueRate) < abs(engagementRate-trueRate)):
#                     engagementRate = temp
#                     whichOne = m
#             print("true: "+str(trueRate)+" | calc'ed: "+str(round(engagementRate,4))+" | "+whichOne)
#engagementRate()

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

def makeGraphic(limit, specification, metric):   
    global instaCSV
    df = instaCSV.copy()
    if limit != "General":
        big=limit.split('/')[0]
        small=limit.split('/')[1]
        mylist = []
        filtered_df = df[df[big]==small]
        df = filtered_df
#    fig = px.scatter(df,x=specification,y=metric, title=limit)
#    avg_df = df.groupby(specification)[metric].mean().reset_index()
#    avgFig = px.scatter(avg_df,x=specification,y=metric, title=f'{limit} Average')
#    return (fig.to_html(full_html=False) + avgFig.to_html(full_html=False))
    scatter = df[[specification, metric]].dropna().to_dict(orient='records')
    avg = df.groupby(specification)[metric].mean().reset_index()
    avg_data = avg.to_dict(orient='records')
    
    return {"scatter": scatter, "avg": avg_data}
# makeGraphic('reach','content_category')

if __name__=="__main__":
    #run file in terminal
    print("run this in flask")
