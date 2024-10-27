import praw


class RedditAPI:
    def __init__(self, client_id, client_secret, user_agent, subreddit="stocks"):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)
        self.subreddit = subreddit

    def fetch_posts(self, query, limit=50):
        """Fetch posts from the specified subreddit."""
        posts = []
        subreddit = self.reddit.subreddit(self.subreddit)
        for submission in subreddit.search(query, limit=limit):
            posts.append(submission.title + " " + submission.selftext)
        return posts
