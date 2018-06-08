# -*- coding: utf-8 -*-
import requests
KEY = "" #请填入自己申请的key
API = 'http://api.avatardata.cn/HistoryToday/LookUp'


def htoday_query(month, day):
    try:
        month = int(month)
        day = int(day)
        response = requests.get(API, params={
            'key': KEY,
            'yue': month,
            'ri': day,
            'type': 2
        }, timeout=1)
        json_data = response.json()
        mydata = json_data['result']
        if mydata is None:
            result = '未找到该日期的事件\n'
            return result
        result = ''
        for item in mydata:
            result += str(item['year']) + '年' + str(item['month']) + '月' + str(item['day']) + '日：\n'
            result += item['title'] + '\n'
        return result
    except:
        return '系统繁忙或出错，请重试'