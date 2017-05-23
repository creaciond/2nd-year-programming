import tweepy
from creditentials import *
import html


def prettify_tweets(tweet_file):
    with open(tweet_file, 'r', encoding='utf-8') as f_read:
        tweets = [html.unescape(line.strip('\n')) for line in f_read.readlines()]
    with open(tweet_file, 'w', encoding='utf-8') as f_write:
        f_write.write('\n'.join(tweets))


def get_tweets(api):
    username = 'creacion_D'
    tweet_count = api.get_user(username).statuses_count
    # tweets = api.user_timeline(screen_name=username, count=tweet_count)
    tweets_clean = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(tweet_count):
        tweets_clean.append(tweet.text.replace('\n', ' '))
    with open('mytweets.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join([tweet for tweet in tweets_clean]))


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    get_tweets(api)
    prettify_tweets('mytweets.txt')


if __name__ == '__main__':
    main()