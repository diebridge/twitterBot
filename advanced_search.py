from helper import ApiRequestGetter, JsonRequestInterceptor, chunks
import json
import pyppeteer
import logging
import asyncio
import re
from pathlib import Path
import aiohttp
import urllib
import datetime

with open(Path(__file__).parent/'files/keywords.csv', 'r') as f:
    kws = [kw.strip('\n') for kw in f.readlines()]

rejected_kws = []

async def get_session():
    """Generate a new session to send request.

    Returns:
        [api] -- [Request Class with url, headers, params]
    """
    jsi = JsonRequestInterceptor('https://twitter.com/search?q=%22iphone%2011%22&src=typed_query', 'full_text')
    await jsi.parse_url()
    api = ApiRequestGetter.ApiRequestGetters_list[-1]
    return api

async def async_get_response(url, method, q, payload=None, headers=None):
    # await semaphore.acquire()
    if payload is None:
        payload = {}
    if headers is None:
        headers = {}
    the_day_before_yesterday = datetime.date.today()-datetime.timedelta(days=2)
    the_day_before_yesterday = the_day_before_yesterday.strftime('%Y-%m-%d')
    q_ = '\"'+q+'\" since:{}'.format(the_day_before_yesterday)
    url = url.replace('q=%22iphone%2011%22',f'q={urllib.parse.quote(q_)}').replace('count=20', 'count=100')
    async with aiohttp.request(method, url, headers=headers, data=payload) as response:
        if response.status == 200:
            logging.info(f'Get response with {q}')
            response = await response.json()
            # semaphore.release()
            if q in rejected_kws:
                rejected_kws.remove(q)
            return response
        else:
            logging.warning(f'No response from  {q} and added to rejected_kws')
            rejected_kws.append(q)
            # semaphore.release()
            return None

        
def _refine_json(results):
    results = sum(results, [])  # flatten 
    for result in results:
        if not result:
            continue
        d = {}
        tweets_dict = result['globalObjects']['tweets']
        keys = tweets_dict.keys()
        users_dict = result['globalObjects']['users']
        for key in keys:
            tweet = tweets_dict[key]
            d['tweet_id'] = key
            # * the url of this tweet is: https://twitter.com/i/web/status/{tweet_id}
            d['user_id'] = tweet['user_id']
            d['geo'] = tweet['geo']
            d['coordinates'] = tweet['coordinates']
            d['place'] = tweet['place']
            d['lang'] = tweet['lang']
            d['created_at'] = tweet['created_at']
            d['full_text'] = tweet['full_text']
            d['lang'] = tweet['lang']
            d['retweet_count'] = tweet['retweet_count']
            user_profile = {}
            user_info = users_dict[str(d['user_id'])]
            user_profile['name'] = user_info['name']
            user_profile['screen_name'] = user_info['screen_name']
            user_profile['followers_count'] = user_info['followers_count']
            d['user'] = user_profile
            yield d

def write_jsonl(data, output):
    for item in data:
        with open(output, 'a') as f:
            json.dump(item, f)
            f.write('\n')

async def handle_rejected_kws(collected_responses):
    api = await get_session()
    while rejected_kws:
        tasks = [async_get_response(api.api_url,
                                    api.method,
                                    kw,
                                    api.post_data,
                                    api.headers) for kw in rejected_kws]
        responses = await asyncio.gather(*tasks)
        collected_responses.append(responses)
    return collected_responses

async def parse_chunks():
    results = []
    kw_chunks = list(chunks(kws, 180))
    # semaphore = asyncio.Semaphore(2)
    for kw_chunk in kw_chunks:
        api = await get_session()
        tasks = [async_get_response(api.api_url,
                                    api.method,
                                    kw,
                                    api.post_data,
                                    api.headers) for kw in kw_chunk]
        responses = await asyncio.gather(*tasks)
        results.append(responses)
    return results

async def async_fetch():
    results = await parse_chunks()
    results = await handle_rejected_kws(results)
    results = _refine_json(results)
    write_jsonl(results, f'{Path(__file__).parent}/twitter_results.json')

if __name__ == "__main__":
    asyncio.run(async_fetch())