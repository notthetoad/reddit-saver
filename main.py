import praw
import requests
import csv
import os
import sys
from pprint import pprint
from time import sleep
from tqdm import tqdm

reddit = praw.Reddit(client_id='ttCQef6TcRoexA',
										 client_secret='6JkehdkGVCfw2QipvI5xEPOvdvhLLg',
										 password='Kyrethegod321',
										 user_agent='saved-download-to-file by u/nyko_lol',
										 username='nYko_LoL')

rows = []
for item in reddit.user.me().saved(limit=None):
	if isinstance(item, praw.models.Comment):
		rows.append([item.body, 'comment', 'comment', 'comment'])
	else:
		rows.append([item.title, item.url, item.id, item.subreddit.display_name])

fields = ['Title', 'url', 'id', 'Subreddit']


set_of_ids = set()
if os.path.isfile('reddit_saved.csv'):
	with open ('reddit_saved.csv', 'r') as doc:
		reader = csv.reader(doc)
		for item in reader:
			set_of_ids.add(item[2])
else:
	with open ('reddit_saved.csv', 'a+') as f:
		writer = csv.writer(f)	
		writer.writerow(fields)


with open ('reddit_saved.csv', 'a+') as f:
	writer = csv.writer(f)
	new_additions = [x for x in rows if not x[2] in set_of_ids]
	writer.writerows(new_additions)
	
# Add progress bar
