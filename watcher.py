from creds import secret, client_id, password, username, pasteBinKey, pasteBinUserKey
from datetime import datetime
import time
from datetime import timedelta
import praw
from amabot import scanThread

reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     password=password,
                     user_agent='amabot by /u/Thravia',
                     username=username)

ageLimitDays = 7
watching = []

subreddit = reddit.subreddit('iAMA')

while True:

    for submission in subreddit.new(limit=10):
        print(submission.title[:15])
        if submission.locked == True:
            continue
        scanThread(submission)
        time.sleep(5)
        print("I woke after 5")
        # do something with submission
        ##if get_date(submission) < datetime.today() - timedelta(days=ageLimitDays):

    time.sleep(10)
    print("i woke after 10")


def get_date(submission):
	time = submission.created
	return datetime.datetime.fromtimestamp(time)