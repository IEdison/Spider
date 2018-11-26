import pymysql
import requests
from lxml import etree
import json


def get_one_page(url):
    # https://list.mogujie.com/search?callback=jQuery21104136356236323091_1540360560429&_version=8193&ratio=3%3A4&cKey=43&sort=pop&page=3&q=%25E5%258F%25A3%25E7%25BA%25A2&minPrice=&maxPrice=&ppath=&cpc_offset=&ptp=1.5y18ub.0.0.21UKqvNk&_=1540360560430
    # https://list.mogujie.com/search?callback=jQuery21104292950771104478_1540351839098&_version=8193&ratio=3%3A4&cKey=43&sort=pop&page=2&q=%25E5%258F%25A3%25E7%25BA%25A2&minPrice=&maxPrice=&ppath=&cpc_offset=&ptp=1.5y18ub.0.0.XCrd3QOw&_=1540351839099
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        text = response.content.decode('utf-8')

        return text
    return None


def get_real_content(html):
    if html and len(html) > 128:
        num = html.index('(')
        # print(num)
        html1 = html[45:]
        html2 = html1.replace(');', '')
        return html2
    return None


def save_db(title, orgprice, price, img):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'mogujie'
    port = 3306
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    cursor = db.cursor()

    sql = "INSERT INTO mogujie (title, orgprice, price, img) values ('%s','%s','%s','%s')" % (
    title, orgprice, price, img)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        pass
    db.close()


def main():
    for index in range(1, 10000):
        url = "https://list.mogujie.com/search?callback=jQuery21103694060337436651_1540349690563&_version=8193&ratio=3%3A4&cKey=43&sort=pop&" + 'page=%s' % index + "&q=%25E5%258F%25A3%25E7%25BA%25A2&minPrice=&maxPrice=&ppath=&cpc_offset=&ptp=1.5y18ub.0.0.pJRh5Qwf&_=1540349690564"

        html = get_one_page(url)
        print(html)
        html_content = get_real_content(html)
        # print(html_content)
        result = json.loads(html_content)
        # print(result)
        # print(result['status'])
        info = result['result']['wall']['docs']
        is_end = result['result']['wall']['isEnd']
        # print(info)
        print('正在爬取第%s页' % index)
        for i in range(len(info)):
            # 标题
            title = info[i]['title']
            # 图片
            img = info[i]['img']
            # 原价
            orgprice = info[i]['orgPrice']
            # 现价
            price = info[i]['price']
            # 收藏

            # print(title, img, orgprice, price)
            save_db(title, orgprice, price, img)
        print('第%s页爬取完成' % index)

        if is_end == True:
            break


if __name__ == '__main__':
    main()
