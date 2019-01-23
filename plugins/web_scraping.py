import urllib.request
import sys
from bs4 import BeautifulSoup

def Web_scraping(area_id):
#路線指定の時はtrain_url3を繋げて、個別路線ページを抽出

    train_url1 = 'https://transit.yahoo.co.jp/traininfo/'
    train_url2 = 'area/' + area_id
    train_url3 = ''
    train_url_all = train_url1 + train_url2

#路線指定かエリア指定かの判定が必要
#要素の抽出
    req = urllib.request.urlopen(train_url_all)
    soup = BeautifulSoup(req, "lxml")

    for table in soup.select("table"):
        for tr in table.find_all("tr"):
            info = [td.get_text() for td in tr.find_all("td")]
            if info:
                yield info

def web_area_main(area_name, area_message):
    if area_message == "北海道":
        area_id = "2/"
    elif area_message == "東北":
        area_id = "3/"
    elif area_message == "関東":
        area_id = "4/"
    elif area_message == "近畿":
        area_id = "6/"
    elif area_message == "東海":
        area_id = "5/"
    elif area_message == "四国":
        area_id = "9/"
    elif area_message == "九州":
        area_id = "7/"
    elif area_message == "中部":
        area_id = "5/"
    elif area_message == "中国":
        area_id = "8/"

    area_name_search = area_name["name"]
    for name_info in area_name_search:
        text_return = text_return + web_main(name_info, area_id)

    return text_return

def web_main(rosen_name, area_id):
    text_return = ""
    for info in Web_scraping(area_id):
        rosen = info[0]
        jokyo = info[1]
        joho = info[2]

        if rosen_name in rosen:
            text = "-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n" + \
                    rosen + "は" + jokyo + "です。\n" + \
                    "詳細：" + joho + "\n"
            text_return = text_return + text
    if text_return == "":
        text_return = "検索結果無し"
    elif len(text_return) >= 10000:
        text_return = "検索結果が多すぎます"
    return text_return 

if __name__ == "__main__":
    pass

#mysqlを使う。
#遅延　のみで東京駅からの路線遅延状況
#遅延　エリア　で関東、関西などエリア情報
#遅延　路線　で路線名の遅延情報
#遅延　show でユーザごとの遅延情報
#遅延　add　路線名　でユーザに遅延情報追加
#遅延　del 路線名　でユーザの遅延情報削除