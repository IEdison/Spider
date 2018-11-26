import json

import requests
import re


def get_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # 汉字乱码:response.content.decode('utf-8')
    return None


def parse_page(html):
    # 名称
    name = re.compile('movieId.*?>.*?<img.*?<img.*?alt="(.*?)" class.*?', re.S)
    name_items = re.findall(name, html)

    # 主演
    star = re.compile('<p class="star">(.*?)</p>', re.S)
    actor_items = re.findall(star, html)

    # 上映时间
    date = re.compile('<p class="releasetime">(.*?)</p>', re.S)
    date_items = re.findall(date, html)

    # 图片
    image = re.compile('movieId.*?>.*?<img.*?<img.*?src="(.*?)"', re.S)
    image_items = re.findall(image, html)

    # 排行
    rank = re.compile('<i class="board-index board-index-.*">(.*?)</i>')
    rank_items = re.findall(rank, html)

    movies = []
    for i in range(len(name_items)):

        one_movie = {}

        one_movie['rank'] = rank_items[i]
        one_movie['name'] = name_items[i]
        one_movie['date'] = date_items[i]
        one_movie['actor'] = actor_items[i].split()[0]
        one_movie['image'] = image_items[i].split('@')[0]
        movies.append(one_movie)
    return movies


def write_img(url):
    filename = url.split('@')[0].split('/')[-1]
    with open('./images/%s' % filename, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)


def main():
    for i in range(10):
        d = i * 10
        url = "https://maoyan.com/board/4?offset=%d" % d
        html = get_page(url)
        movies = parse_page(html)

        str = json.dumps(movies, ensure_ascii=False)
        with open('info.json', 'a', encoding='utf-8')as f:
            f.write(str)
        print(movies)

        # for item in items:
        #     print(item)
        # write_img(item.strip())
    # print(html)
    # print(items)


if __name__ == '__main__':
    main()
