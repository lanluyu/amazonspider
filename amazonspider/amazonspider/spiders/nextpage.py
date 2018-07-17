# -*- coding: utf-8 -*-
'''
翻页处理,获取所有的父栏目、子栏目及分栏目和它们的页数及数量，总共660项
'''
from scrapy import Spider,Request
from amazonspider.items import AmazonspiderItem

class NextpageSpider(Spider):
    name = 'nextpage'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.cn/s/ref=sr_hi_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071&bbn=116169071&sort=price-asc-rank&unfiltered=1&ie=UTF8&qid=1530862450']

    def parse(self, response):
        # 获取35个父栏目
        list_books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        list_num = len(list_books)
        for book in list_books:    
            list_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
            list_name = book.xpath('.//span/a/span/text()').extract_first()           
            # 请求 Kindle电子书下的父栏目
            yield Request(url=list_href,callback=self.parse_list,dont_filter=True,
                            meta={"list_href":list_href,"list_name":list_name,"list_num":list_num})

    def parse_list(self,response):
        # 获取传递的变量值
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        list_num = response.meta.get("list_num")
        # 获取父栏目的子栏目
        item_books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        item_num = len(item_books)
        # 先判断有无 子栏目
        if item_num >0:
            for book in item_books:    
                item_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
                item_name = book.xpath('.//span/a/span/text()').extract_first()
                # 请求子栏目下的分栏目
                yield Request(url=item_href,callback=self.parse_fen,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,"list_num":list_num,"item_num":item_num})
            
        else:
            # 没有子栏目，就直接请求父栏目
            yield Request(url=list_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"list_num":list_num}) 

    def parse_fen(self,response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        item_name = response.meta.get("item_name")
        item_href = response.meta.get("item_href")
        list_num = response.meta.get("list_num")
        item_num = response.meta.get("item_num")
        # 获取子栏目的分栏目
        fen_books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        fen_num = len(fen_books)
        # 先判断有无分栏目
        if fen_num >0:
            for book in fen_books:  
                fen_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
                fen_name = book.xpath('.//span/a/span/text()').extract_first()
                yield Request(url=fen_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,"fen_href":fen_href,"fen_name":fen_name,"list_num":list_num,"item_num":item_num,"fen_num":fen_num})

        else:
            # 没有分栏目，就直接请求子栏目
            yield Request(url=list_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,"list_num":list_num,"item_num":item_num})

    def parse_url(self,response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        item_href = response.meta.get("item_href")
        item_name = response.meta.get("item_name")    
        fen_href = response.meta.get("fen_href")
        fen_name = response.meta.get("fen_name")
        list_num = response.meta.get("list_num")
        item_num = response.meta.get("item_num")
        fen_num = response.meta.get("fen_num")
        # 解析响应
        ye = response.xpath('.//span[@class="pagnDisabled"]/text()').extract_first()
        zongshu = response.xpath('.//span[@id="s-result-count"]/text()').extract_first()
        # 存入数据库
        item =  AmazonspiderItem()  
        item['list_href'] = list_href
        item['list_name'] = list_name
        item['item_href'] = item_href
        item['item_name'] = item_name
        item['fen_href'] = fen_href
        item['fen_name'] = fen_name
        item['list_num'] = list_num
        item['item_num'] = item_num
        item['fen_num'] = fen_num
        item['zongshu'] = zongshu
        item['ye'] = ye
        print(item)
        yield item

# 最多显示 400 页 6400 条  超过部分不予显示

    