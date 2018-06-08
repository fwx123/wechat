# -*- coding: utf-8 -*-
import requests
import random
KEY = "" #请填入自己申请的key
API = 'http://api.avatardata.cn/Joke/NewstJoke'


def joke_query():
    try:
        response = requests.get(API, params={
            'key': KEY,
            'page': str(random.randint(1, 50000)),
            'rows': 1
        }, timeout=1)
        json_data = response.json()
        return json_data['result'][0]['content']
    except:
        return '系统繁忙或出错，请重试'