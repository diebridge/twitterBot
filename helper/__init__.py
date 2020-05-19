import time
from functools import wraps
import logging
from .Api import ApiRequestGetter
from .request_interceptor import JsonRequestInterceptor

logging.getLogger('pyppeteer').setLevel(logging.CRITICAL)
logging.basicConfig(
    # filename=f"{__file__.split('/')[-1][:-3]}.log",
    level=logging.INFO,
    format='%(levelname)s %(asctime)-15s %(funcName)s()-line: %(lineno)s %(pathname)s >>>>>>>>> %(message)s')

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
