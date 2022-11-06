#datetime,timedelta获取日期，更改时间格式
from datetime import date,datetime,timedelta
#wechatpy
from wechatpy import WeChatClient,WeChatClientException
from wechatpy.client.api import WeChatMessage
import os
import requests
import math
import random
#获取现在时间
nowtime =datetime.utcnow()+timedelta(hours=8)
today =datetime.strptime(str(nowtime.date()),"%Y-%m-%d")
#wechat公众号的全局唯一接口调用凭据 有效期2个小时
app_id='wx5196201b6000da13'
app_aecret='dfa742ffce59f1759b99eb80681f1290'
use_id='on4lv5-zcYoufgSf8eGhdfenh6H4'
template_id='5xd0GHLS8mf9cNcRsezymyJNAMciD2LFZ7G4jg_uBqY'
city='洛阳'
try:
    client=WeChatClient(app_id,app_aecret)
except WeChatClientException as e:
    print('微信获取token失败')
    exit(502)
wn=WeChatMessage(client)


def get_weather():
    if city is None:
        print('请设置城市')
        return None
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res=requests.get(url).json()
    if res is None:
        return None
    weather=res['data']['list']
    return weather
# 彩虹屁 接口不稳定 重复获取 直到成功
def get_words():
    words= requests.get("https://api.shadiao.pro/chp")
    if words.status_code!=200:
        return  get_words()
    return words.json()['data']['text']

if __name__=='__main__':

    weather=get_weather()
    if weather is None:
        print('获取天气错误')
        exit(422)
    date={
        "city":{
            "value":city
        },
        "date":{
            "value":today.strftime('%Y年%m月%d日')
        },
        "weather":{
            "value":weather[0]['weather']
        },
        "temp":{
            "value":math.floor(weather[0]['temp'])
        },
        "weather_t":{
            "value":weather[1]['weather']
        },
        "weather_a_t":{
            "value":weather[2]['weather']
        }
    }
    try:
        res=wn.send_template(use_id,template_id,date,'http://tianqi.moji.com/forecast15/china/henan/luoyang')
    except WeChatClientException as e:
        print('错误')
        exit(502)
    pass
