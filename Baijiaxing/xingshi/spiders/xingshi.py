import re

import scrapy

from xingshi.items import XingshiItem


class XingshiSpider(scrapy.Spider):
    name = 'xingshi'
    # allowed_domains = ['www.resgain.net/xmdq.html']
    start_urls = ['http://www.resgain.net/xmdq.html']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }

        yield scrapy.Request(url='http://www.resgain.net/xmdq.html',
                             headers=headers,
                             method='GET',
                             callback=self.parse,
                             )

    def parse(self, response):

        name_urls = response.xpath('//a[@class="btn btn2"]/@href').extract()
        # print(name_urls)
        # '//zhao.resgain.net/name_list.html'

        for n_item in name_urls:
            for index in range(1, 11):
                if index == 1:
                    url = 'http:' + n_item
                else:
                    url = 'http:' + n_item.replace('name_list', 'name_list_%s' % index)
                print(index, url)
                yield scrapy.Request(url=url,
                                     callback=self.parse_name,
                                     )

    def parse_name(self, response):

        names = response.xpath('//div[@class="col-xs-12"]/a[@class="btn btn-link"]')
        # print(names)
        xingshi = response.xpath('//a[@class="navbar-brand"]/div/text()').extract_first().split('姓')[0]
        print('123123' + xingshi)
        for n_item in names:
            print('*******************************')
            # url前缀
            s_url = response.url

            s = n_item.xpath('./@href').extract()[0]

            start_url = s_url.split('/name')[0]
            # 姓名链接
            the_name_url = start_url + s
            # http: // zhao.resgain.net / name / 赵凤岚.html
            print(the_name_url)

            # 名字
            the_name = n_item.xpath('./text()').extract()
            print(the_name[0])
            s_item = XingshiItem()
            s_item['name'] = the_name[0]
            s_item['xingshi'] = xingshi
            yield scrapy.Request(url=the_name_url,
                                 meta={'info': s_item},
                                 callback=self.parse_every,
                                 )

    def parse_every(self, response):

        # 名字解释说明
        # 五行
        wuxing = response.xpath('//div[@class="panel-body"]/div[@class="col-xs-6"]/blockquote/text()').extract()[
            0]

        print(wuxing)
        # 三才
        sancai = response.xpath('//div[@class="panel-body"]/div[@class="col-xs-6"]/blockquote/text()').extract()[
            1]
        print(sancai)

        s_item = response.meta['info']
        s_item['wuxing'] = wuxing
        s_item['sancai'] = sancai
        yield s_item
