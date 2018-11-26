import requests
from bs4 import BeautifulSoup


def get_one_page():
    url = "https://cd.lianjia.com/zufang/"
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_soul(html):
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    info = soup.select('#house-lst li .info-panel h2 a')
    print(info)
    info1 = soup.select('.price .num')
    print(info1)
    homes = []

    for a in info:
        home = {}
        print(a.string)
        home['name'] = a.string
        print(a.attrs['href'])
        home['link'] = a['href']
        homes.append(home)
    print(homes)
    for b in info1:
        print(b.string + '元')


def main():
    html = get_one_page()
    # print(html)
    parse_soul(html)


if __name__ == '__main__':
    main()
