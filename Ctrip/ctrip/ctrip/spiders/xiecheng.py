# -*- coding: utf-8 -*-
import scrapy
from ctrip.items import CtripItem

class XiechengSpider(scrapy.Spider):
    name = 'xiecheng'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://hotels.ctrip.com/hotel/chengdu28#ctm_ref=hod_hp_sb_lst']

    def parse(self, response):
        results = response.xpath('//div[@class="hotel_new_list J_HotelListBaseCell"]/ul[@class="hotel_item"]')
        for hotel in results:
            ctrip_item = CtripItem()
            ctrip_item['hotel_name'] = hotel.xpath('.//h2[@class="hotel_name"]/a/@title').extract_first()

            yield ctrip_item