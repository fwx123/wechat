import requests
import datetime
WEATHER_KEY = '' #请填入自己申请的key
WEATHER_API1 = 'https://free-api.heweather.com/s6/weather?' #天气集合
WEATHER_API2 = 'https://free-api.heweather.com/s6/weather/forecast?' #3天天气
WEATHER_API3 = 'https://free-api.heweather.com/s6/air/now?' #空气质量
DICT_TYPE = {'comf': '舒适度指数', 'cw': '洗车指数', 'drsg': '穿衣指数', 'flu': '感冒指数', 'sport': '运动指数',
             'trav': '旅游指数', 'uv': '紫外线指数', 'air': '空气污染扩散条件指数'}
WEEKARR = ('周一', '周二', '周三', '周四', '周五', '周六', '周日')


def weather_today(location):
    try:
        response = requests.get(WEATHER_API1, params={
            'key': WEATHER_KEY,
            'location': location
        }, timeout=1)
        json_data = response.json()
        city = ''
        arr = json_data['HeWeather6'][0]
        if arr["status"] != "ok":
            return_str = ''
            if arr['status'] == 'unknown city':
                return_str = '未知或错误城市/地区'
            if arr['status'] == 'no data for this location':
                return_str = '该城市/地区没有你所请求的数据'
            if arr['status'] == 'no more requests':
                return_str = '超过访问次数，需要等到当月最后一天24点后进行访问次数的重置或升级你的访问量'
            if return_str == '':
                return_str = '其他错误，请联系管理员'
            return return_str
        if 'parent_city' not in arr['basic'] or arr['basic']['parent_city'] == arr['basic']['location']:
            loc = arr['basic']['location']
            city = loc
        else:
            loc = arr['basic']['parent_city'] + arr['basic']['location']
            city = arr['basic']['parent_city']
        result = '%s今日天气\n' % loc
        result += '———————————————\n'
        forcast_arr = arr['daily_forecast'][0]
        result += '温度：%s℃～%s℃(实况:%s℃)\n' % (forcast_arr['tmp_max'], forcast_arr['tmp_min'], arr['now']['tmp'])
        if forcast_arr['cond_txt_d'] == forcast_arr['cond_txt_n']:
            result += '天气：%s(实况:%s)\n' % (forcast_arr['cond_txt_d'], arr['now']['cond_txt'])
        else:
            result += '天气：%s转%s\n(实况:%s)\n' % (forcast_arr['cond_txt_d'], forcast_arr['cond_txt_n'], arr['now']['cond_txt'])
        result += '风向：%s\n风力：%s\n' % (forcast_arr['wind_dir'], forcast_arr['wind_sc'])
        result += '相对湿度：%s%%\n降水概率：%s%%\n' % (forcast_arr['hum'], forcast_arr['pop'])
        result += '紫外线强度指数：%s\n' % forcast_arr['uv_index']

        response = requests.get(WEATHER_API3, params={
            'key': WEATHER_KEY,
            'location': city
        }, timeout=1)
        json_data = response.json()
        if json_data['HeWeather6'][0]['status'] == 'ok':
            air = json_data['HeWeather6'][0]['air_now_city']['qlty']
            result += '空气质量：%s\n' % air

        if 'lifestyle' in arr:
            result += '\n生活指数\n'
            for i in range(7):
                type = DICT_TYPE[arr['lifestyle'][i]['type']]
                result += '%s：%s\n' % (type, arr['lifestyle'][i]['brf'])
        result += '———————————————'
        return result
    except:
        return '系统繁忙或出错，请重试'


def weather_forecast(location):
    try:
        response = requests.get(WEATHER_API2, params={
            'key': WEATHER_KEY,
            'location': location
        }, timeout=1)
        json_data = response.json()
        arr = json_data['HeWeather6'][0]
        if arr["status"] != "ok":
            return_str = ''
            if arr['status'] == 'unknown city':
                return_str = '未知或错误城市/地区'
            if arr['status'] == 'no data for this location':
                return_str = '该城市/地区没有你所请求的数据'
            if arr['status'] == 'no more requests':
                return_str = '超过访问次数，需要等到当月最后一天24点后进行访问次数的重置或升级你的访问量'
            if return_str == '':
                return_str = '其他错误，请联系管理员'
            return return_str
        if 'parent_city' not in arr['basic'] or arr['basic']['parent_city'] == arr['basic']['location']:
            loc = arr['basic']['location']
        else:
            loc = arr['basic']['parent_city'] + arr['basic']['location']
        result = '%s未来两日天气预报\n' % loc
        result += '———————————————\n'
        weekday = datetime.datetime.now().weekday()
        for i in [1, 2]:
            forcast_arr = arr['daily_forecast'][i]
            weekday = (weekday + 1) % 7
            date_str = forcast_arr['date'][5:7] + '月' + forcast_arr['date'][8:10] + '日'
            result += '%s %s：\n' % (date_str, WEEKARR[weekday])
            result += '温度：%s℃～%s℃\n' % (forcast_arr['tmp_max'], forcast_arr['tmp_min'])
            if forcast_arr['cond_txt_d'] == forcast_arr['cond_txt_n']:
                result += '天气：%s\n' % forcast_arr['cond_txt_d']
            else:
                result += '天气：%s转%s\n' % (forcast_arr['cond_txt_d'], forcast_arr['cond_txt_n'])
            result += '风向：%s\n风力：%s\n' % (forcast_arr['wind_dir'], forcast_arr['wind_sc'])
            result += '相对湿度：%s%%\n降水概率：%s%%\n' % (forcast_arr['hum'], forcast_arr['pop'])
            result += '紫外线强度指数：%s\n' % forcast_arr['uv_index']
            if i == 1:
                result += '\n'
        result += '———————————————'
        return result
    except:
        return '系统繁忙或出错，请重试'


def weather_pm(location):
    try:
        response = requests.get(WEATHER_API3, params={
            'key': WEATHER_KEY,
            'location': location
        }, timeout=1)
        json_data = response.json()
        arr = json_data['HeWeather6'][0]
        if arr["status"] != "ok":
            return_str = ''
            if arr['status'] == 'unknown city':
                return_str = '未知或错误城市/地区'
            if arr['status'] == 'no data for this location':
                return_str = '该城市/地区没有你所请求的数据'
            if arr['status'] == 'no more requests':
                return_str = '超过访问次数，需要等到当月最后一天24点后进行访问次数的重置或升级你的访问量'
            if return_str == '':
                return_str = '查询失败，查询PM请回复地级市'
            return return_str
        result = '%s空气质量\n' % arr['basic']['location']
        result += '———————————————\n'
        result += '空气质量指数：%s\n' % arr['air_now_city']['aqi']
        result += '主要污染物：%s\n' % arr['air_now_city']['main']
        result += '空气质量：%s\n' % arr['air_now_city']['qlty']
        result += 'PM10：%s\n' % arr['air_now_city']['pm10']
        result += 'PM25：%s\n' % arr['air_now_city']['pm25']
        result += 'NO2：%s\n' % arr['air_now_city']['no2']
        result += 'SO2：%s\n' % arr['air_now_city']['so2']
        result += 'CO：%s\n' % arr['air_now_city']['co']
        result += '03：%s\n' % arr['air_now_city']['o3']
        result += '更新时间：%s\n' % arr['air_now_city']['pub_time']
        result += '———————————————'
        return result
    except:
        return '系统繁忙或出错，请重试'