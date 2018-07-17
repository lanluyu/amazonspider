# -*- coding: utf-8 -*-
'''
进口原版电子书
'''
from scrapy import Spider,Request
from amazonspider.items import AmazonspiderItem

class ImportSpider(Spider):
    name = 'import'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.cn/b?ie=UTF8&node=116170071']

    def parse(self, response):
        # 获取34个子栏目
        books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        for book in books:    
            list_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
            list_name = book.xpath('.//span/a/span/text()').extract_first()           
            # 请求 Kindle电子书下的子栏目
            yield Request(url=list_href,callback=self.parse_list,dont_filter=True,meta={"list_href":list_href,"list_name":list_name})

    def parse_list(self,response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")

        books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        if len(books)>0: 
            for book in books:    
                item_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
                item_name = book.xpath('.//span/a/span/text()').extract_first()
                # 请求子栏目下的分栏目
                key = item_href.split('=')[-1]
                yield Request(url=item_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,'key':key})
        else:
            key = list_href.split('=')[-1]
            # 没有分栏目，就直接请求子栏目
            yield Request(url=list_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,'key':key})
        
    def parse_url(self,response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        item_name = response.meta.get("item_name")
        item_href = response.meta.get("item_href")
        key = response.meta.get("key")
        # 解析子栏页的最大页码
        ye = response.xpath('.//span[@class="pagnDisabled"]/text()').extract_first()
        if ye is None:
            print(item_name,'子栏爬取失败')
            yield Request(item_href,callback=self.parse_url,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,'key':key})   
        else:
            num = int(ye)+1
            for i in range(1, num):
                base_url = 'https://www.amazon.cn/s?ie=UTF8&page={}&rh=n%3A{}'
                url = base_url.format(i,key)
                yield Request(url,callback=self.parse_item,dont_filter=True,
                            meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,'i':i,'url':url})

    def parse_item(self, response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        item_name = response.meta.get("item_name")
        item_href = response.meta.get("item_href")
        url = response.meta.get("url")
        i = response.meta.get("i")

        a =response.xpath('.//span[@class="pagnCur"]/text()').extract_first()
        if a is None:
            print('爬取失败')
            yield Request(url,callback=self.parse_item,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name,'i':i,'url':url})   
        else:
            print('正在爬取',list_name,item_name,'第',a,'页')
        
        books = response.xpath('.//div[@class="s-item-container"]')
        for book in books:  
            item =  AmazonspiderItem()
            item['href'] = book.xpath('.//a[@title="Kindle电子书"]/@href').extract_first()
            item['name'] = book.xpath('.//div[@class="a-row a-spacing-small"]//a/h2/text()').extract_first()  #.//h2[@data-max-rows="0"]/text()
            prices = book.xpath('.//div[@class="a-row a-spacing-none"]//a/span/text()').extract()
            if len(prices) <= 1:
                item['price'] = prices[0]
            else:
                item['price'] = prices[1]
            item['time'] = book.xpath('.//span[contains(text(),"-")]/text()').extract_first()  # 出版日期
            item['author'] = book.xpath('.//div[@class="a-row a-spacing-small"]/div[2]/span/text()').extract_first()
            item['stars'] = book.xpath('.//span[@class="a-icon-alt"]/text()').extract_first()  # 星级
            comment = book.xpath('.//div[@class="a-row a-spacing-mini"]/a/text()').extract()   # 商品评论数
            if len(comment) == 1:
                item['comments'] = comment[0]   # 存在 'Kindle Unlimited 包月服务.' 选项
            elif len(comment) == 0:
                item['comments'] = book.xpath('.//div[@class="a-row a-spacing-mini"]/a/text()').extract_first()
            else:
                item['comments'] = comment[1]  
            item['list_name'] = list_name
            item['list_href'] = list_href
            item['item_name'] = item_name
            item['url'] = response.url
            item['req_url'] = url
            item['yema'] = a+'页'
            yield item
