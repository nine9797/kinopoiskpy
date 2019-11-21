# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import request
import random

class Request(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.1.8) Gecko/20100214 Linux Mint/8 (Helena) Firefox/'
                      '3.5.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Encoding': 'deflate',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '300',
        'Connection': 'keep-alive',
        'Referer': 'http://www.kinopoisk.ru/',
        'Cookie': 'users_info[check_sh_bool]=none; search_last_date=2010-02-19; search_last_month=2010-02;'
                  '                                        PHPSESSID=b6df76a958983da150476d9cfa0aab18',
    }

    def __init__(self):
        import requests
        self.session = requests.Session()

    # def get(self, *args, **kwargs):
    #     kwargs['headers'] = self.headers
    #     response = self.session.get(*args, **kwargs)
    #     response.connection.close()
    #     return response

    def get(self, *args, **kwargs):
        with open('/app/proxy_list.txt') as f:
            lines = f.read().splitlines()
        kwargs['headers'] = self.headers
        # proxy = os.environ['89.40.58.44:3128']
        kwargs['proxies'] = {
            'http': 'socks4://{}'.format(random.choice(lines))
        }
        response = self.session.get(*args, **kwargs, timeout=5)
        response.connection.close()
        return response

    def get_content(self, *args, **kwargs):
        response = self.get(*args, **kwargs)
        content = response.content.decode(response.encoding)
        self.raise_for_errors(content)
        return content

    def raise_for_errors(self, content):
        if 'captcha' in content:
            raise ValueError('Kinopoisk block this IP. Too many requests')
