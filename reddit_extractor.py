# ------------- IMPORTS -------------

import praw
import random

# -----------------------------------






# ------------- CREDENTIALS. PROVIDING USER INFORMATION -------------

__client_id__ = ''
__client_secret__ = ''
__user_agent__ = ''

with open('reddit_credentials.txt', 'r', encoding='utf-8') as f:
    [__client_id__, __client_secret__, __user_agent__] = f.readlines()
    f.close()

reddit = praw.Reddit(
    client_id = __client_id__[:-1],
    client_secret = __client_secret__[:-1],
    user_agent = __user_agent__[:-1]
)

# ---------------------------------------------------------------------






# ------------- GLOBAL CONTAINERS -------------

SUBREDDITS = {
    'MEMES': ['memes', 'dankmemes'],
    'JOKES': ['jokes'],
    'NEWS': ['Romania']
}

MEMES = []
JOKES = []
NEWS = []

# ---------------------------------------------






# ------------- FUNCTIONS -------------

def randomized_integer(subreddit):
    return random.randrange(0, len(SUBREDDITS[subreddit]))

# ------------------------------------





# ------------- EXTRACTORS -------------

for submission in reddit.subreddit(SUBREDDITS['MEMES'][randomized_integer('MEMES')]).hot(limit=99):
    if not ('.gif' in submission.url) and not ('comment' in submission.url):
        MEMES.append(submission.url)

for submission in reddit.subreddit(SUBREDDITS['JOKES'][randomized_integer('JOKES')]).hot(limit=99):
    if submission.edited == False:
        JOKES.append([submission.title, submission.selftext])

for submission in reddit.subreddit(SUBREDDITS['NEWS'][randomized_integer('NEWS')]).hot(limit=99):
    if submission.link_flair_text == 'Știri' and submission.url != '':
        NEWS.append([submission.title, submission.url])

# --------------------------------------

