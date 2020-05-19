from .page_operation import open_page, initialize_browser
import dataclasses
import logging
import asyncio
from .Api import ApiRequestGetter
import re
import json

@dataclasses.dataclass
class JsonRequestInterceptor(object):
    """Catch API which contains multiple desired items.

    Constructor:
        url: the web/html url (e.g https://twitter.com/search-advanced) in which the real request was sent.
        json_containing_key: An common key in the desired json. To match the needed json. e.g. 'full_text' in every tweets.
        matched_times: Default is 5. If this key occurs 5 times than the Api will be recorded.

    """
    inspect_url: str
    json_containing_key:str = None
    matched_times: int = 5

    async def __aenter__(self):
        self.browser = await initialize_browser(headless = True)

    async def filter_json(self, response):
        try:
            if 'application/json' in response.headers['content-type']:
                response_as_json = await response.json()
                return response_as_json
        except KeyError:
            pass
        except UnicodeDecodeError as e:
            logging.info('UnicodeDecodeError of utf-8')
        except json.decoder.JSONDecodeError:
            logging.info('json.decoder.JSONDecodeError')
        except pyppeteer.errors.NetworkError:
            logging.info('pyppeteer.errors.NetworkError')
        except Exception as e:
            logging.error(f'{e}')

    async def intercept_response(self, response):
        response_as_json = await self.filter_json(response)
        post_data = p if (p:= response.request.postData) else None
        if not self.json_containing_key:
            return ApiRequestGetter(response.request.url,
                            response.request.headers, response.request.method, post_data)
        matched_kw_list = r if (r:=re.findall(
                                r'{}'.format(self.json_containing_key),
                                str(response_as_json))) else []
        if response.request and len(matched_kw_list) >= self.matched_times:
            api = ApiRequestGetter(response.request.url,
                            response.request.headers, response.request.method, post_data)

    async def parse_url(self):
        async with self:
            page = await open_page(self.browser, self.inspect_url)
            page.on('response', self.intercept_response)
    
    async def __aexit__(self, exc_type, exc, tb):
        logging.info('Got session and quit browser.')
        await asyncio.sleep(5)
        await self.browser.close()