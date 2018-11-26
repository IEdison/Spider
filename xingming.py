import re

import pymysql
import requests
from bs4 import BeautifulSoup



# 取页面HTML
def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_page(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    # print(soup)
    info = soup.select('.col-xs-12 .btn')
    # print(info)
    # 连接数据库
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'names'
    port = 3306
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    cursor = db.cursor()

    for i in range(len(info)):
        try:
            for index in range(1, 11):
                xingshi = info[i].get_text().split('姓')[0]
                print(index, xingshi)
                if index == 1:
                    url = 'http:' + info[i].attrs['href']
                else:
                    url = 'http:' + info[i].attrs['href'].replace('name_list', 'name_list_%s' % index)
                # http://zhao.resgain.net/name_list.html
                # print(url)

                page_source = get_page(url)
                soup = BeautifulSoup(page_source, 'lxml')

                names = soup.select('.col-xs-12 .btn-link')
                for j in range(len(names)):
                    # url前缀
                    start_url = url.split('/name')[0]
                    # 姓名链接
                    the_name_url = start_url + names[j].attrs['href']
                    # http: // zhao.resgain.net / name / 赵凤岚.html
                    # print(the_name_url)

                    # 名字
                    the_name = names[j].get_text()
                    # print(the_name)

                    # 名字解释说明
                    page_source = get_page(the_name_url)
                    soup = BeautifulSoup(page_source, 'lxml')
                    # 五行
                    wuxing = soup.select('.panel-body .col-xs-6 blockquote')[0].get_text()
                    # 三才
                    sancai = soup.select('.panel-body .col-xs-6 blockquote')[1].get_text()
                    # 五格
                    wuge = soup.select('.panel-body .col-xs-12 blockquote')[0].get_text()
                    wuge = re.sub('\s', '', wuge)
                    # print(wuxing, sancai, wuge)
                    sql = "INSERT INTO baijia (name,wuxing,sancai,wuge,xingshi) values ('%s','%s','%s','%s','%s')" % (
                        the_name, wuxing, sancai, wuge, xingshi)
                    cursor.execute(sql)

        except:
            pass
        db.commit()
    db.close()


def main():
    url = "http://www.resgain.net/xmdq.html"
    page_source = get_page(url)
    parse_page(page_source)


if __name__ == '__main__':
    main()
