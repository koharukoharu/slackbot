# -*- coding: utf-8 -*-

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.bot import default_reply
from libs import my_functions
import json
import xml.etree.ElementTree as ET
import urllib.request
import datetime
import lxml

from plugins.web_scraping import web_main, Web_scraping
from plugins.train_sql import Train_search_area, Train_search_name

#今日の日時を教えてくれる機能
@respond_to('時間')
def mention_time_func(message):
    time = datetime.datetime.now()
    time_text = '今は' + str(time) + 'だよ！（整形する気なし）'
    message.send(time_text) 

#今の電車遅延状況を教えてくれる機能
@respond_to(r'^遅延\s+\S.*')
def mention_station_func(message):
    text = message.body['text']
    temp, message_name = text.split(None, 1)
    if message_name == "北海道" or message_name == "東北" or message_name == "関東" or message_name == "近畿"\
     or message_name == "東海" or message_name == "四国" or message_name == "九州" or message_name == "中部" or message_name == "中国":
        text = Train_search_area(message_name)
    else:
        text = Train_search_name(message_name)
        scraping_text = web_main(text)
    message.send(scraping_text)

#指定地域の天気情報を教えてくれる機能
@respond_to(r'^天気\s+\S.*')
def mention_wether_func(message):
    text = message.body['text']
    temp, city_name = text.split(None, 1)
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city='
    city_id = city_search(city_name)
    html = urllib.request.urlopen(url + city_id)
    jsonfile = json.loads(html.read().decode('utf-8'))
    title = jsonfile['title'] 
    telop = jsonfile['forecasts'][0]['telop']
    link = jsonfile['link']
    city_text = jsonfile['description']['text']

#今日の天気で気温が--になっている場合はパスする
    max_celsius = '不明'
    min_celsius = '不明'
    try:
        max_celsius = jsonfile['forecasts'][0]['temperature']['max']['celsius']
        min_celsius = jsonfile['forecasts'][0]['temperature']['min']['celsius']
    except TypeError:
        pass

#アイコン設定
    telop_icon = ''
    if telop.find('雪') > -1:    
        telop_icon = ':showman:'
    elif telop.find('雷') > -1:
        telop_icon = ':thinder_cloud_and_rain:'
    elif telop.find('晴') > -1:
        if telop.find('曇') > -1:
            telop_icon = ':partly_sunny:'
        elif telop.find('雨') > -1:
            telop_icon = ':partly_sunny_rain:'
        else:
            telop_icon = ':sunny:'
    elif telop.find('雨') > -1:
        telop_icon = ':umbrella:'
    elif telop.find('曇') > -1:
        telop_icon = ':cloud:'
    else:
        telop_icon = ':fire:'

#送信メッセージ成型
    text =  '*' + title + "：　" + telop + telop_icon + '*' + '\n' + '最高気温：' + max_celsius + '℃' + '\n' + '最低気温：'\
     + min_celsius + '℃' + '\n' + city_text + '\n' + link

    message.send(text)

#地域コードの検索処理
def city_search(city_name):
    city_url = 'http://weather.livedoor.com/forecast/rss/primary_area.xml'
    req = urllib.request.Request(city_url)
#xmlをURLから取得
    with urllib.request.urlopen(req) as response:
        XmlData = response.read()
    elem = ET.fromstring(XmlData)
    for e in elem.getiterator("city"):
        if e.get("title") in city_name:
            rt =  e.get("id")
            break
        else:
            rt = '130010'
    return rt
