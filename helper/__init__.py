import time
from functools import wraps
import tweepy
import logging
from .mydb import db, cursor
from .Api import ApiRequestGetter
from .request_interceptor import JsonRequestInterceptor

logging.getLogger('pyppeteer').setLevel(logging.CRITICAL)
logging.basicConfig(
    # filename=f"{__file__.split('/')[-1][:-3]}.log",
    level=logging.INFO,
    format='%(asctime)-15s %(funcName)s()-line: %(lineno)s %(pathname)s %(levelname)s---\t%(message)s')


def get_authenticated_api(get_more=True):
    # Authenticate to Twitter
    if get_more:
        auth = tweepy.AppAuthHandler("Ch7XbG8xR0gs7mP8JB0wSNLfF",
                                "ub8FZtV6QBAUbU0K17ZDUrSkDQsnb8D21dVHIOTuGA6HpmpRUa")
    else:
        auth = tweepy.OAuthHandler("Ch7XbG8xR0gs7mP8JB0wSNLfF",
                                "ub8FZtV6QBAUbU0K17ZDUrSkDQsnb8D21dVHIOTuGA6HpmpRUa")
        auth.set_access_token("1251798010033561601-LhwCCT0jgIniu6C9POTS9pD8Wgb6AK",
                            "TcnJn8Q1Q0JXxykCwlqC2fN0YQx6qP22I6AlFyZQ46RhL")

    api = tweepy.API(auth,  wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    if (not api):
        logging.error("AuthenticationError during authentication")
        sys.exit(-1)
    logging.info("Authentication passed.")
    return api

def timefn(function):
    @wraps(function)
    def count_time(*args, **kwargs):
        t1 = time.time()
        result = function(*args, **kwargs)
        t2 = time.time()
        print(str(function) + ' took ' + str(t2-t1) + ' seconds')
        return result
    return count_time

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]
