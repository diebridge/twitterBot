import requests

def get_response(url, method, q, payload=None, headers=None):
    if payload is None:
        payload = {}
    if headers is None:
        headers = {}
    url = url.replace('q=%22iphone%2011%22',f'q={q}').replace('count=20', 'count=100')
    response = requests.request(method, url, headers=headers, data=payload)
    if response:
        logging.info(f'Get response from  {url}')
        return response.json()
    else:
        logging.warning(f'No response from  {url}')
        logging.warning(response)
        return None

def sync_fetch():
    """Deprecated."""
    api = get_session()
    for keyword in kws:
        response = get_response(
                                api.api_url,
                                api.method,
                                keyword,
                                api.post_data,
                                api.headers
                                )
        if not response:  # <status code = 429> Too many requests.
            asyncio.run(jsi.parse_url())
            api = ApiRequestGetter.ApiRequestGetters_list[-1]
            response = get_response(
                                api.api_url,
                                api.method,
                                keyword,
                                api.post_data,
                                api.headers
                                )
        with open('r.json', 'a') as f:
            json.dump(response, f)
            f.write('\n')