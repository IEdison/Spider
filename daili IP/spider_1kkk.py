import time

import requests
from PIL import Image


def get_image():
    for i in range(16, 300):
        print(i)
        t = time.time()
        t = int(t)
        url = "http://www.1kkk.com//image3.ashx?t=1%s" % t
        headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        }
        response = requests.get(url, headers=headers)
        image_data = response.content
        with open('./image/%s.jpg' % i, 'wb') as f:
            f.write(image_data)
        img = Image.open('./image/%s.jpg' % i)
        for j in range(4):
            x = 76
            y = 0
            screenshot = img.crop((x * j, y, x * (j + 1), x))
            screenshot.save('./image1/%s_%s.jpg' % (i, j))


def main():
    get_image()


if __name__ == '__main__':
    main()
