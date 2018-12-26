import urllib.request
import sys
from bs4 import BeautifulSoup

def Web_scraping():
#路線指定の時はtrain_url3を繋げて、個別路線ページを抽出

    train_url1 = 'https://transit.yahoo.co.jp/traininfo/'
    train_url2 = 'area/4/'
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


def web_main(rosen_name):
    text_return = ""
    for info in Web_scraping():
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