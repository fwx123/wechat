#coding=utf-8
import werobot
import json
import requests
import myweather
import mydream
import mymusic
import mytrans
import mycons
import myname
import myhxw
import myhtoday
import myjoke
import datetime
from werobot.replies import ArticlesReply, Article

MYNAMES = ('樊文翔', '翔兄', '翔哥', '文翔', '老爹')
MENU = 'Hi，我是机器人小蚊香。回复以下【】内信息看看吧！\n【1】天气\n【2】翻译\n【3】点歌\n【4】段子\n【5】周公解梦' \
       '\n【6】今日运势\n【7】姓氏起源\n【8】火星文转换\n【9】历史上的今天\n【0】显示主菜单\n【#】查看快捷功能\n回复其他信息可与我进行闲聊哦~'
QUICK_MENU = '快捷功能\n———————————————\n在主菜单下，按以下格式回复可直接使用菜单内功能哦~\n参考格式：\n【命令】+【空格】+【内容】\n\n今日天气：天气 城市\n'\
             '天气预报：预报 城市\nPM查询：PM 地级市\n中到英翻译：翻译 翻译内容\n点歌：点歌 歌曲名\n段子：段子\n解梦：解梦 关键词\n火星文转换：火星 转换内容\n———————————————\n'
LANG_MENU0 = '【1】中文\n【2】英语\n【3】粤语\n【4】文言文\n【5】日语\n【6】韩语\n【7】法语\n【8】西班牙语\n【9】泰语\n'
LANG_MENU = LANG_MENU0 + '【10】阿拉伯语\n【11】俄语\n【12】葡萄牙语\n【13】德语\n【14】意大利语\n【15】希腊语\n' \
                         '【16】荷兰语\n【17】波兰语\n【18】保加利亚语\n【19】爱沙尼亚语\n【20】丹麦语\n【21】芬兰语\n' \
                         '【22】捷克语\n【23】罗马尼亚语\n【24】斯洛文尼亚语\n【25】瑞典语\n【26】匈牙利语\n' \
                         '【27】繁体中文\n【28】越南语\n'
CONS_MENU = '【1】水瓶座（1.20~2.18）\n【2】双鱼座（2.19~3.20）\n【3】白羊座（3.21~4.19）\n【4】金牛座（4.20~5.20）\n【5】双子座（5.21~6.21）\n' \
            '【6】巨蟹座（6.22~7.22）\n【7】狮子座（7.23~8.22）\n【8】处女座（8.23~9.22）\n【9】天秤座（9.23~10.23）\n【10】天蝎座（10.24~11.22）\n' \
            '【11】射手座（11.23~12.21）\n【12】摩羯座（12.22~1.19）\n'
SUB_MENU1 = '天气\n———————————————\n【1】今日天气查询\n【2】天气预报查询\n【3】PM查询\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU1_1 = '今日天气查询\n———————————————\n回复格式：城市名/区名/县名/拼音\n如：柳南\n————————————\n回复【0】返回上一级菜单'
SUB_MENU1_2 = '天气预报查询\n———————————————\n回复格式：城市名/区名/县名/拼音\n如：柳南\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU1_3 = 'PM查询\n———————————————\n回复格式：城市名/拼音\n如：南宁\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU2 = '翻译\n———————————————\n请选择目标语言：\n' + LANG_MENU0 + '———————————————\n回复【#】查看更多语言\n回复【0】返回上一级菜单'
SUB_MENU2_1 = '翻译\n———————————————\n请选择目标语言：\n' + LANG_MENU + '———————————————\n回复【0】返回上一级菜单'
SUB_MENU2_2 = '%s翻译\n———————————————\n回复格式：翻译内容(任意语言)\n如：苹果\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU3 = '点歌\n———————————————\n回复格式：歌名or歌名+歌手\n如：菊花台 周杰伦\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU4 = '段子\n———————————————\n%s\n———————————————\n回复其他信息看下一条段子\n回复【0】返回上一级菜单'
SUB_MENU5 = '周公解梦\n———————————————\n回复格式：关键词\n如：黄金\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU6 = '今日运势\n———————————————\n请选择你的星座：\n' + CONS_MENU + '———————————————\n回复【0】返回上一级菜单'
SUB_MENU7 = '姓氏起源\n———————————————\n回复格式：姓氏\n如：轩辕\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU8 = '火星文转换\n———————————————\n回复格式：转换文字（纯中文）\n———————————————\n回复【0】返回上一级菜单'
SUB_MENU9 = '历史上的今天\n———————————————\n%s———————————————\n回复【月 日】继续查询\n如：1 1\n回复【0】返回上一级菜单'


robot = werobot.WeRoBot(token='weixin')


def talks_robot(info = '你叫什么名字', source = '0'):
    api_url = 'http://www.tuling123.com/openapi/api'
    api_key = '' #请填入自己申请的key
    if len(source) > 32:
        source = source[0:33]
    data = {'key': api_key, 'info': info, 'userid': source}
    req = requests.post(api_url, data=data).text
    reply = json.loads(req)['text']
    return reply


@robot.text
def text(message, session):
    msg = message.content
    # if str == '1':
    #     reply = ArticlesReply(message=message)
    #     article = Article(
    #         title="WeRoBot",
    #         description="WeRoBot是一个微信机器人框架",
    #         img="https://mmbiz.qpic.cn/mmbiz_jpg/PB39TB41pd3D0Uy4mlvxO6stn2LoUkRy82cBYwo6qGWuqCJ8YfBU2IfmWFPoJa9Fic9LpJy3Lz2cO7yaE2yJaqQ/0?wx_fmt=jpeg",
    #         url="https://github.com/whtsky/WeRoBot"
    #     )
    #     reply.add_article(article)
    #     return reply
    if 'last' in session:
        if session['last'] == '1':
            if 'weather' in session and session['weather'] != '':
                if msg == '0':
                    session['weather'] = ''
                    return SUB_MENU1
                else:
                    num = int(session['weather'])
                    if num == 1:
                        return myweather.weather_today(msg) + '\n回复查询内容继续查询\n回复【0】返回上一级菜单'
                    if num == 2:
                        return myweather.weather_forecast(msg) + '\n回复查询内容继续查询\n回复【0】返回上一级菜单'
                    if num == 3:
                        return myweather.weather_pm(msg) + '\n回复查询内容继续查询\n回复【0】返回上一级菜单'
                    return
            else:
                if msg == '0':
                    session['last'] = 0
                    return MENU
                if msg.isdigit():
                    num = int(msg)
                    if 1 <= num <= 3:
                        session['weather'] = str(num)
                        if num == 1:
                            return SUB_MENU1_1
                        if num == 2:
                            return SUB_MENU1_2
                        if num == 3:
                            return SUB_MENU1_3
                    return
                else:
                    return
        if session['last'] == '2':
            if 'trans' in session and session['trans'] != '':
                if msg == '0':
                    session['trans'] = ''
                    return SUB_MENU2
                else:
                    return mytrans.get_trans(session['trans'], msg)
            else:
                if msg == '0':
                    session['last'] = 0
                    return MENU
                if msg == '#':
                    return SUB_MENU2_1
                if msg.isdigit():
                    num = int(msg)
                    if 1 <= num <= 28:
                        session['trans'] = str(num)
                        return SUB_MENU2_2 % mytrans.get_lang(num)
                    return
                else:
                    return
        if session['last'] == '3':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                music_data = mymusic.get_music(msg)
                if music_data[0] == '0':
                    return '很抱歉，未能找到相关搜索结果'
                else:
                    return [
                        music_data[1],
                        music_data[2],
                        music_data[3]
                    ]
        if session['last'] == '4':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                return SUB_MENU4 % myjoke.joke_query()
        if session['last'] == '5':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                return mydream.dream_query(msg) + '\n回复查询内容继续查询\n回复【0】返回上一级菜单'
        if session['last'] == '6':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                if msg.isdigit():
                    num = int(msg)
                    if 1 <= num <= 12:
                        return mycons.cons_query(num)
                return
        if session['last'] == '7':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                return myname.name_query(msg)
        if session['last'] == '8':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                return myhxw.hxw_query(msg)
        if session['last'] == '9':
            if msg == '0':
                session['last'] = 0
                return MENU
            else:
                try:
                    a, b = msg.split()
                    if a.isdigit() and b.isdigit():
                        return SUB_MENU9 % myhtoday.htoday_query(a, b)
                    else:
                        return '输入格式错误'
                except:
                    return '输入格式错误'
    session['last'] = msg;
    if msg == '1':
        return SUB_MENU1
    elif msg == '2':
        return SUB_MENU2
    elif msg == '3':
        return SUB_MENU3
    elif msg == '4':
        return SUB_MENU4 % myjoke.joke_query()
    elif msg == '5':
        return SUB_MENU5
    elif msg == '6':
        return SUB_MENU6
    elif msg == '7':
        return SUB_MENU7
    elif msg == '8':
        return SUB_MENU8
    elif msg == '9':
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        return SUB_MENU9 % myhtoday.htoday_query(m, d)
    elif msg == '#':
        session['last'] = '0'
        return QUICK_MENU
    elif msg == '0' or 'msg' == '菜单':
        session['last'] = '0'
        return MENU

    sub_str = msg[:3]
    if sub_str == '天气 ':
        return myweather.weather_today(msg[3:])
    if sub_str == '预报 ':
        return myweather.weather_forecast(msg[3:])
    if sub_str == 'PM ' or sub_str == 'pm ':
        return myweather.weather_pm(msg[3:])
    if sub_str == '翻译 ':
        return mytrans.get_trans('2', msg[3:])
    if sub_str == '点歌 ':
        music_data = mymusic.get_music(msg[3:])
        if music_data[0] == '0':
            return '很抱歉，未能找到相关搜索结果'
        else:
            return [
                music_data[1],
                music_data[2],
                music_data[3]
            ]
    if sub_str[:2] == '段子':
        return myjoke.joke_query()
    if sub_str == '解梦 ':
        return mydream.dream_query(msg[3:])
    if sub_str == '火星 ':
        return myhxw.hxw_query(msg[3:])

    for name in MYNAMES:
        if msg.find(name) >= 0:
            msg = msg.replace(name, '你')
    reply = talks_robot(msg, message.source)
    return reply


@robot.subscribe
def subscribe(message):
    return MENU


@robot.image
def image(message):
    return '收到一张图片\n图片查看：' + message.img


@robot.voice
def voice(message):
    return '收到一条语音\n识别结果：' + message.recognition


@robot.link
def link(message):
    return '收到一条链接\n标题：\n' + message.title + '\n描述：\n' + message.description + '\n地址：\n' + message.url


@robot.location
def location(message):
    location_x = str(round(message.location[0], 3))
    location_y = str(round(message.location[1], 3))
    location = location_x + ',' + location_y
    return myweather.weather_today(location)


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 12233
robot.run()
