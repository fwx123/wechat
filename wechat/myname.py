# -*- coding: utf-8 -*-
import requests
KEY = "" #请填入自己申请的key
API = 'http://api.avatardata.cn/XingShiQiYuan/LookUp'


def name_query(query):
    try:
        response = requests.get(API, params={
            'key': KEY,
            'xingshi': query,
        }, timeout=1)
        json_data = response.json()
        mydata = json_data['result']
        # return mydata
        if mydata is None:
            result = '未找到该姓氏\n'
            result += '———————————————\n'
            result += '回复姓氏继续查询\n回复【0】返回上一级菜单'
            return result
        result = '姓氏起源——%s\n' % mydata['xing']
        result += '———————————————\n'
        info = mydata['intro']
        info = info.replace(' ', '')
        info = info.replace('<BR>', '\n')
        info = info.replace('&nbsp;', '')
        info = info.replace('<P>', '')
        info = info.replace('</P>', '')
        info = info.replace('</B>', '')
        info = info.replace('<B>', '')
        info = info.replace(u'\u3000', u'')
        info = info[5:]
        p1 = info.find('聚集地')
        p2 = info.find('历史名人')
        p3 = info.find('家乘谱牒')
        p4 = info.find('二、迁徙分布')
        p5 = info.find('堂号')
        if p1 == -1 and p2 == -1 and p3 == -1 and p4 == -1 and p5 == -1:
            result += info
        else:
            if p1 == -1:
                p1 = 10000
            if p2 == -1:
                p2 = 10000
            if p3 == -1:
                p3 = 10000
            if p4 == -1:
                p4 = 10000
            if p5 == -1:
                p5 = 10000
            p = min(p1, p2, p3, p4, p5)
            info = info[:p].strip()
            info = info.replace('\n', '\n\n')
            result += info
        result += '\n'
        result += '———————————————\n'
        result += '回复查询内容继续查询\n回复【0】返回上一级菜单'
        return result
    except:
        return '系统繁忙或出错，请重试'