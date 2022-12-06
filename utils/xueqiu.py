import requests
import orjson as json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
cookies = {'xq_a_token': '25916c3bfec27272745f6070d664a48d4b10d322'}


def quick_ratio(ticker: str, latest: bool = True, period: int = -1):
    if latest: period = -1
    country = 'us'  # default, unless some other pattern is detected below
    if ticker.endswith('.HK'):
        ticker = '0' + ticker.split('.')[0]
        country = 'hk'
    elif ticker.endswith('.SZ'):
        ticker = 'SZ' + ticker.split('.')[0]
        country = 'cn'
    elif ticker.endswith('.SS'):
        ticker = 'SH' + ticker.split('.')[0]
        country = 'cn'
    ticker = ticker.split('.')[0]  # try as some of them are also listed in US then can use data from xueqiu
    url = f'https://stock.xueqiu.com/v5/stock/finance/{country}/indicator.json?symbol={ticker}&type=Q4&is_detail=true&count=4'
    r = requests.get(url, headers=headers, cookies=cookies).text
    r = json.loads(r)
    lst = list(reversed(r['data']['list']))
    r = lst[period]['quick_ratio'][0]  # json will make the field None if it's not available
    if r:
        return r/100  # convert from % to abs
    else:
        return None
