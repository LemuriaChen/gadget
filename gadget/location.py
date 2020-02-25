
import urllib.request
import json
import time

from numba.tests.dummy_module import function
import socket
import requests
import re


def timer(func: function) -> function:
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{round(end - start, 4)} seconds used.')
        return result
    return wrapper


# 获取公网ip地址
@timer
def get_public_ip(method: int) -> str:
    """
    :param method:
        method = 0 -> http://ip.42.pl,
        method = 1 -> http://jsonip.com,
        method = 2 -> http://httpbin.org,
        method = 3 -> https://api.ipify.org,
    :return:
    """
    ip = ''
    if method == 0:
        try:
            ip = urllib.request.urlopen('http://ip.42.pl/raw').read().decode()
        except Exception as e:
            print(e)
    elif method == 1:
        try:
            ip = json.load(urllib.request.urlopen('http://jsonip.com')).get('ip')
        except Exception as e:
            print(e)
    elif method == 2:
        try:
            ip = json.load(urllib.request.urlopen('http://httpbin.org/ip')).get('origin')
        except Exception as e:
            print(e)
    elif method == 3:
        try:
            ip = json.load(urllib.request.urlopen('https://api.ipify.org/?format=json')).get('ip')
        except Exception as e:
            print(e)
    else:
        assert method in [0, 1, 2, 3], 'method should be in [0, 1, 2, 3]'
    return ip


# 获取内网ip地址
@timer
def get_host_ip():
    ip = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        print(e)
    finally:
        s.close()
    return ip


# 获取地址
@timer
def get_location():

    url = 'https://www.ip.cn/'
    headers = {
        'content-type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    }
    location = ''

    try:
        html = requests.get(url=url, headers=headers).text
        location = re.search(
            u"<p>所在地理位置：<code>(.*?)</code></p>", html
        ).group(1).split()[0].strip()
    except Exception as e:
        print(f'fail to connect to < {url} > . {e}')

    return location


if __name__ == '__main__':

    # 获取公网地址
    print(get_public_ip(method=0))
    # 获取内网地址
    print(get_host_ip())
    # 获取位置
    print(get_location())
