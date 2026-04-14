import csv
from decimal import Decimal
import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

#listing genres
def listGenres():
    genres = {}
    with open('static/insta.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            genre = row['content_category']
            print(genre)
            if genre not in genres:
                genres[genre] = 0
            genres[genre] += 1
    print(genres)
#listGenres()

#finding out what the engagement rate means --> metric used: impressions
def engagementRate():
    with open('static/insta.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trueRate = Decimal(row['engagement_rate'])
            metrics = ['follower_count', 'reach', 'impressions']
            engagements = ['likes','comments','shares','saves']
            totalEngagement = 0.0
            engagementRate = 5
            whichOne = ''
            for e in engagements:
                totalEngagement += int(row[e])
            for m in metrics:
                metric = int(row[m])
                temp = Decimal(totalEngagement/metric)
                if (abs(temp-trueRate) < abs(engagementRate-trueRate)):
                    engagementRate = temp
                    whichOne = m
            print("true: "+str(trueRate)+" | calc'ed: "+str(round(engagementRate,4))+" | "+whichOne)
# engagementRate()

def makeGraphic(limit, specification, metric):   
    df = pd.read_csv('static/insta.csv')
    if limit != "General":
        big=limit.split('/')[0]
        small=limit.split('/')[1]
        mylist = []
        filtered_df = df[df[big]==small]
        df = filtered_df
    fig = px.scatter(df,x=specification,y=metric, title=limit)
    avg_df = df.groupby(specification)[metric].mean().reset_index()
    avgFig = px.scatter(avg_df,x=specification,y=metric, title=f'{limit} Average')
    return (fig.to_html(full_html=False) + avgFig.to_html(full_html=False))
# makeGraphic('reach','content_category')

if __name__=="__main__":
    #run file in terminal
    print("run this in flask")