# -*- coding: utf-8 -*-
import requests
KEY = "" #请填入自己申请的key
API = 'http://api.avatardata.cn/HuoXingWen/LookUp'


def hxw_query(query):
    try:
        response = requests.get(API, params={
            'key': KEY,
            'content': query,
            'changeType': 2
        }, timeout=1)
        json_data = response.json()
        return json_data['result']
    except:
        return '系统繁忙或出错，请重试'