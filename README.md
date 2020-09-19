## Twitter Bot

By intercepting valid cookies with pypeeteer to send customerized asynchronous requests with aiohttp.
Every session can be used 180 times to query. Then, get another vaild session to continue to query.

### Input

The crawler will crawl all tweets for given keywords.
Every word in single line.

Input file located in file/keywords.csv

```
React
Trading
VDV454
ALDEA
...
```

### Run

Run commands under /twitterBot:  
`pipenv install`  
`pipenv shell`  
`python advanced_search.py`  

### Output
Output will be located in twitterBot/twitter_results.json


### Annotations

This project is only a learning and practice project, and all the consequences have nothing to do with the author.