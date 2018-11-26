import time
from urllib import parse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree

# 无头浏览器
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
browser.set_window_size(700, 700)
wait = WebDriverWait(browser, 10)


def get_page():
    url = "https://www.xiami.com/chart?spm=a1z1s.2943549.6827465.1.N09sY4"
    browser.get(url)

    time.sleep(3)
    page_source = browser.page_source
    # print(page_source)
    return page_source

# 凯撒密码
def str2url(s):
    # s = '9hFaF2FF%_Et%m4F4%538t2i%795E%3pF.265E85.%fnF9742Em33e162_36pA.t6661983%x%6%%74%2i2%22735'
    num_loc = s.find('h')
    rows = int(s[0:num_loc])
    strlen = len(s) - num_loc
    cols = int(strlen / rows)
    right_rows = strlen % rows
    new_s = list(s[num_loc:])
    output = ''
    for i in range(len(new_s)):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
        output += new_s[int(p)]
    return parse.unquote(output).replace('^', '0')


def parse_page(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    # print(soup)
    info = soup.select('#chart table tr')
    # print(info[0])
    for i in range(len(info)):
        # 歌曲名字
        song = info[i].select('.songblock .song .info p strong a')[0].get_text()
        # print(song)

        # 歌手名字
        singer = info[i].select('.artist')[0].attrs['title']
        # print(singer)

        # mp3链接
        data_mp3 = info[i].attrs['data-mp3']
        # print(data_mp3)
        result_str = str2url(data_mp3)
        # print(result_str)
        text_info = requests.get(result_str)
        # 二进制文件
        text = text_info.content
        # print(text)
        i = i+1
        try:
            with open('./music/%s-%s.mp3' % (song, singer), 'wb') as f:
                f.write(text)
                print('第%s首下载完成' % i)
        except:
            print('第%s首下载失败' % i)


def main():
    page_source = get_page()
    parse_page(page_source)


if __name__ == '__main__':
    main()
