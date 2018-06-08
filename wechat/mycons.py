# -*- coding: utf-8 -*-
import requests
KEY = "" #请填入自己申请的key
API = 'http://api.avatardata.cn/Constellation/Query'
CONS = ('水瓶座', '双鱼座', '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座')


def cons_query(index):
    try:
        index = int(index)
        response = requests.get(API, params={
            'key': KEY,
            'consName': CONS[index - 1],
            'type': 'today'
        }, timeout=1)
        json_data = response.json()
        mydata = json_data['result1']
        result = '今日运势\n'
        result += '———————————————\n'
        result += mydata['datetime'] + '\n'
        result += mydata['name'] + '运势\n'
        result += '综合指数：' + mydata['all'] + '\n'
        result += '幸运色：' + mydata['color'] + '\n'
        result += '健康指数：' + mydata['health'] + '\n'
        result += '爱情指数：' + mydata['love'] + '\n'
        result += '财运指数：' + mydata['money'] + '\n'
        result += '工作指数：' + mydata['work'] + '\n'
        result += '幸运数字：' + mydata['number'] + '\n'
        result += '速配星座：' + mydata['QFriend'] + '\n'
        result += '今日概述：\n'
        result += mydata['summary'] + '\n'
        result += '———————————————\n'
        result += '回复【1】~【12】继续查询\n回复【0】返回上一级菜单'
        return result
    except:
        return '系统繁忙或出错，请重试'