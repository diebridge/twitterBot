from pyppeteer_stealth import stealth
import random
from pyppeteer import launch
import json
import pyppeteer
import logging
from typing import List

agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:34.0) Gecko/20100101 Firefox/34.0",
    # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    # "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
]


async def initialize_browser(headless=False):
    # * important: Those args can bypass linkedin detection.
    # * See: https://gist.github.com/tegansnyder/c3aeae4d57768c58247ae6c4e5acd3d1
    browser = await launch({"headless": headless,
                            "ignoreHTTPSErrors": True,
                            'dumpio':True,
                            # "userDataDir": './tmp',
                            "args": [
                                '--no-sandbox',
                                '--disable-setuid-sandbox',
                                '--disable-infobars',
                                '--window-position=0,0',
                                '--ignore-certifcate-errors',
                                '--ignore-certifcate-errors-spki-list',
                            ]
                            })
    # disable_timeout_pyppeteer()
    logging.info('Browser initializing...')
    return browser

# May important for page.goto(). Solving the issue of websocket.
# See 'https://github.com/pyppeteer/pyppeteer2/issues/6'
def disable_timeout_pyppeteer():
    import pyppeteer.connection
    original_method = pyppeteer.connection.websockets.client.connect
    def new_method(*args, **kwargs):
        kwargs['ping_interval'] = None
        kwargs['ping_timeout'] = None
        return original_method(*args, **kwargs)

    pyppeteer.connection.websockets.client.connect = new_method

async def open_page(browser, url, cookies: dict = None):
    page = await browser.newPage()
    await stealth(page)
    if cookies:
        for cookie in cookies:
            await page.setCookie(cookie)
    await page.setUserAgent(random.choice(agents))
    await page.setExtraHTTPHeaders({'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'})
    await page.setViewport({
        "width": 1920,
        "height": 1080
    })
    try:
        await page.goto(url,
                        # waitUntil='networkidle0'
                        )
        logging.info(f'Page <{url}> loaded successfully. ')
    except Exception:
        logging.error(f'Catch error when open_page {url}', exc_info=True)
    return page
