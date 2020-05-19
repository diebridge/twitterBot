from helper import get_authenticated_api, timefn, db, cursor
import logging
from pprint import pprint
import tweepy
from pathlib import Path
import sqlite3
import time
import datetime


BASEPATH = Path(__file__).parent
api = get_authenticated_api(get_more=True) 


def get_all_tweets(q=None, start = None, end=None):
    logging.info(f'Searching {q}')
    for tweet in tweepy.Cursor(api.search, q=f"{q} -filter:retweets",
                               tweet_mode='extended', count=20, until=end
                               # geocode="48.137154,11.576124,5000km"
                               ).items(20):
        yield tweet


with open(BASEPATH/'files/keywords.csv', 'r') as f:
    kws = [kw.strip('\n') for kw in f.readlines()]


def search_keyword(db, kw):
    start_date = datetime.date.today()-datetime.timedelta(days=2)
    end_date = datetime.date.today()
    try:
        results = list(get_all_tweets(q=kw, start=start_date, end=end_date))
        [db.cursor().execute('''INSERT OR IGNORE INTO MyTable3(keyword,
                            name,
                            geo,
                            image,
                            source,
                            timestamp,
                            text,
                            rt) VALUES(?,?,?,?,?,?,?,?)''',
                            (kw,
                            tweet.user.screen_name,
                            str(tweet.geo),
                            tweet.user.profile_image_url,
                            tweet.source,
                            tweet.created_at,
                            tweet.full_text,
                            tweet.retweet_count))
            for tweet in results if results]
    except Exception as e:
        logging.info(e)
    except KeyboardInterrupt:
        db.commit()
        db.close()

def search_keywords(db):
    for idx, kw in enumerate(kws):
        search_keyword(db, kw)
    else:
        db.commit()
        db.close()

@timefn
def main():
    for _ in range(1000):
        db = sqlite3.connect(f'{Path(__file__).parent}/files/tweets.db')
        search_keywords(db)
        time.sleep(900)
        print(f'Running {_} times. ')
    

if __name__ == '__main__':
    main()
