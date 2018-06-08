# -*- coding: UTF-8 -*-
import hashlib
import random
import requests

appid = '' #请填入自己申请的appid
secretKey = '' #请填入自己申请的key
TRANS_API = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
LANG = ('zh', 'en', 'yue', 'wyw', 'jp', 'kor', 'fra', 'spa', 'th', 'ara', 'ru', 'pt', 'de', 'it', 'el', 'nl', 'pl',
        'bul', 'est', 'dan', 'fin', 'cs', 'rom', 'slo', 'swe', 'hu', 'cht', 'vie')
LANG_LIST = ('中文', '英语', '粤语', '文言文', '日语', '韩语', '法语', '西班牙语', '泰语', '阿拉伯语', '俄语',
             '葡萄牙语', '德语', '意大利语', '希腊语', '荷兰语', '波兰语', '保加利亚语', '爱沙尼亚语', '丹麦语',
             '芬兰语', '捷克语', '罗马尼亚语', '斯洛文尼亚语', '瑞典语', '匈牙利语', '繁体中文', '越南语')
LANG_DICT = {'zh': '中文', 'en': '英语', 'yue': '粤语', 'wyw': '文言文', 'jp': '日语', 'kor': '韩语', 'fra': '法语',
             'spa': '西班牙语', 'th': '泰语', 'ara': '阿拉伯语', 'ru': '俄语', 'pt': '葡萄牙语', 'de': '德语',
             'it': '意大利语', 'el': '希腊语', 'nl': '荷兰语', 'pl': '波兰语', 'bul': '保加利亚语', 'est': '爱沙尼亚语',
             'dan': '丹麦语', 'fin': '芬兰语', 'cs': '捷克语', 'rom': '罗马尼亚语', 'slo': '斯洛文尼亚语',
             'swe': '瑞典语', 'hu': '匈牙利语', 'cht': '繁体中文', 'vie': '越南语'}


def get_lang(index):
    return LANG_LIST[index - 1]

def get_trans(lang_index, query):
    toLang = LANG[int(lang_index) - 1]
    salt = random.randint(32768, 65536)
    sign = appid+query+str(salt)+secretKey
    sign = hashlib.md5(sign.encode(encoding='UTF-8')).hexdigest()

    try:
        response = requests.get(TRANS_API, params={
            'appid': appid,
            'q': query,
            'from': 'auto',
            'to': toLang,
            'salt': salt,
            'sign': sign
        }, timeout=1)
        json_data = response.json()
        # from_lang = LANG_DICT[json_data['from']]
        # to_lang = LANG_DICT[json_data['to']]
        # result = '%s翻译：' % get_lang(int(lang_index)) + from_lang + ' to ' + to_lang + '\n'
        # result += '——————————————————\n'
        result = json_data['trans_result'][0]['dst']
        # result += '——————————————————\n'
        # result += '回复查询内容继续查询\n回复【0】返回上一级菜单'
        return result
    except:
        return '系统繁忙或出错，请重试'