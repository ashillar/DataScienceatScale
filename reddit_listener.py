from datetime import datetime,timezone
import json
import socket
import praw
import csv

with open("config.json", "r") as jsonfile:
    data = json.load(jsonfile) # Reading the config file
    print("Config data read successful",data)
    

reddit = praw.Reddit(
        client_id = data["client_id"],
        client_secret = data["client_secret"],
        user_agent= data["user_agent"])

stream = reddit.subreddit("AskUK+AskAnAmerican").stream

with open('redditdata.csv','a') as f:
    headers = ['Author', 'ID', 'Submission', 'Body', 'Subreddit','Created_UTC', 'Collected_UTC']
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for comments in stream.comments(skip_existing=True):
        now_utc = datetime.now(timezone.utc)
        created_utc = datetime.utcfromtimestamp(comments.created_utc)
        data = {'Author': comments.author , 'ID': comments.id, 'Submission': comments.submission, 'Body': comments.body, 'Subreddit': comments.subreddit, 'Created_UTC': created_utc, 'Collected_UTC': now_utc}
        writer.writerow(data)
