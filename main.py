import praw
import csv
import os
import sys
import yaml
from pprint import pprint

def load_config():
	with open ('config.yml', 'r') as f:
		config = yaml.load(f, Loader=yaml.Loader)
	return config


def init_reddit(client_id, client_secret, password, user_agent, username):
	reddit = praw.Reddit(client_id=client_id,
											client_secret=client_secret,
											password=password,
											user_agent=user_agent,
											username=username)
	return reddit

def get_saved(reddit):
	rows = []
	for item in reddit.user.me().saved(limit=None):
		if isinstance(item, praw.models.Comment):
			rows.append([item.body, 'comment', 'comment', 'comment'])
		else:
			rows.append([item.title, item.url, item.id, item.subreddit.display_name])
	return rows

def check_file():
	set_of_ids = set()
	fields = ['Title', 'url', 'id', 'Subreddit']
	if os.path.isfile('reddit_saved.csv'):
		with open ('reddit_saved.csv', 'r') as doc:
			reader = csv.reader(doc)
			for item in reader:
				set_of_ids.add(item[2])
	else:
		with open ('reddit_saved.csv', 'a+') as f:
			writer = csv.writer(f)	
			writer.writerow(fields)
	return set_of_ids

def append_to_file(rows, set_of_ids):
	with open ('reddit_saved.csv', 'a+') as f:
		writer = csv.writer(f)
		new_additions = [x for x in rows if not x[2] in set_of_ids]
		writer.writerows(new_additions)
	
def main():
	config = load_config()
	reddit = init_reddit(**config['reddit_config'])
	saved = get_saved(reddit)
	set_of_ids = check_file()
	append_to_file(saved, set_of_ids)

if __name__ == '__main__':
	main()