import time

import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from lxml import etree

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)

browser.set_window_size(900, 700)
wait = WebDriverWait(browser, 10)
KEYWORD = '零食'


def get_page(page):
    if page == 1:
        url = "https://search.jd.com/Search?keyword=%s&enc=utf-8" % quote(KEYWORD)
        browser.get(url)
        print(page)

    if page > 1:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#J_bottomPage .p-skip input')))
        input.clear()
        input.send_keys(page)
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage .p-skip a')))
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#J_topPage span.fp-text b'), str(page)))
        print(page)

    for i in range(10):
        str_js = ' var step = document.body.scrollHeight/10; window.scrollTo(0, step * %d)' % i
        browser.execute_script(str_js)
        time.sleep(1)
    time.sleep(5)
    page_souce = browser.page_source
    return page_souce


def save_db(shop_id, shop_title, shop_img, shop_link, shop_price, shop_name):
    host = '127.0.0.1'
    user = 'root'
    password = '123456'
    database = 'jd'
    port = 3306
    db = pymysql.connect(host, user, password, database, charset='utf8', port=port)
    cursor = db.cursor()
    sql = "INSERT INTO shop (s_id,title,img,link,price,s_name) values ('%s','%s','%s','%s','%s','%s')" % (
    shop_id, shop_title, shop_img, shop_link, shop_price, shop_name)

    cursor.execute(sql)
    db.commit()
    db.close()


def parse_page(page_source):
    etree_html = etree.HTML(page_source)
    print(etree_html)

    products = etree_html.xpath('//div[@class="gl-i-wrap"]')

    for product in products:
        # 商品ID
        shop_ids = product.xpath('//div[@class="p-price"]/strong/@class')

        # 图片
        shop_imgs = product.xpath('//div[@class="p-img"]/a/img/@src')
        # 链接
        shop_links = product.xpath('//div[@class="p-img"]/a/@href')
        # 价格
        shop_prices = product.xpath('//div[@class="p-price"]/strong/i/text()')
        # 标题
        shop_titles = product.xpath('//div[@class="p-name p-name-type-2"]/a/em/text()')
        # 商品名称
        shop_names = product.xpath('//div[@class="p-shop"]/span/a/text()')

    print(len(products))
    for i in range(len(products)):
        try:
            shop_id = shop_ids[i].split('_')[1]
            shop_img = shop_imgs[i]
            shop_link = shop_links[i]
            shop_price = shop_prices[i]
            shop_title = shop_titles[i]
            shop_name = shop_names[i]
            print(i + 1, shop_id, shop_title, shop_price, shop_img, shop_link, shop_name)
            save_db(shop_id, shop_title, shop_img, shop_link, shop_price, shop_name)
        except:
            pass

def main():
    for page in range(100):
        page_source = get_page(page + 1)
        parse_page(page_source)


if __name__ == '__main__':
    main()
