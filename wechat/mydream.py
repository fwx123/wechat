# -*- coding: utf-8 -*-
import requests
DREAM_KEY = "" #请填入自己申请的key
DREAM_API = 'http://v.juhe.cn/dream/query?'


# 解梦查询
def dream_query(query):
    try:
        response = requests.get(DREAM_API, params={
            'key': DREAM_KEY,
            'q': query,
            'full': 1
        }, timeout=1)
        json_data = response.json()
        if json_data['error_code'] == 0:
            if json_data['result'] == 'null' or json_data['result'] is None:
                result = '这个周公我也不知道'
            else:
                result = '周公解梦之' + json_data['result'][0]['title'] + '\n'
                result += '———————————————\n'
                list = json_data['result'][0]['list']
                length = len(list)
                if length > 1 :
                    length = length - 1
                for i in range(length):
                    result += '[' + str(i + 1) + ']' + list[i] + '\n'
                result += '———————————————'
            return result
        else:
            return json_data['reason']
    except:
        return '系统繁忙或出错，请重试'