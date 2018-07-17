# -*- coding: utf-8 -*-
'''
理论上可以获取亚马逊所有电子书信息。但是还是分成了中文电子书和英文原版电子两项分别爬取。各分别有40万左右的书籍
'''
from scrapy import Spider,Request
from amazonspider.items import AmazonspiderItem


class AmazonSpider(Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.cn/s/ref=sr_hi_2?rh=n%3A116087071%2Cn%3A%21116088071%2Cn%3A116169071&bbn=116169071&sort=price-asc-rank&unfiltered=1&ie=UTF8&qid=1530862450']

    def parse(self, response):
        # 获取35个子栏目
        books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        for book in books:
            list_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
            list_name = book.xpath('.//span/a/span/text()').extract_first()
            # print(list_href,list_name)
            # 请求 Kindle电子书下的子栏目
            yield Request(url=list_href,callback=self.parse_list,dont_filter=True,meta={"list_href":list_href,"list_name":list_name})

    def parse_list(self,response):
        list_href = response.meta.get("list_href")
        list_name = response.meta.get("list_name")
        books = response.xpath('.//ul[@class="a-unordered-list a-nostyle a-vertical s-ref-indent-two"]/div/li')
        if books:
            for book in books:
                item_href = book.xpath('.//span/a[@class="a-link-normal s-ref-text-link"]/@href').extract_first()
                item_name = book.xpath('.//span/a/span/text()').extract_first()
                #print(list_name,item_href,item_name)
                # 请求子栏目下的分栏目
                yield Request(url=item_href,callback=self.parse_item,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name})
        else:
            # print(list_href,list_name)
            # 没有分栏目，就直接请求子栏目
            yield Request(url=list_href,callback=self.parse_item,dont_filter=True,
                        meta={"list_href":list_href,"list_name":list_name})
    
    def parse_item(self,response):
        # 获取传递的变量名
        list_name = response.meta.get("list_name")
        list_href = response.meta.get("list_href")
        item_name = response.meta.get("item_name")
        item_href = response.meta.get("item_href")

        a =response.xpath('.//span[@class="pagnCur"]/text()').extract_first()
        print('正在爬取',list_name ,item_name,'第',a,'页')

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
            item['item_href'] = item_href
            item['yema'] = a+'页'

            yield item

        next_url = response.xpath('.//a[@title="下一页"]/@href').extract_first()
        
        if next_url:
            url = 'https://www.amazon.cn'+ next_url
            yield Request(url,callback=self.parse_item,dont_filter=True,
            meta={"list_href":list_href,"list_name":list_name,"item_href":item_href,"item_name":item_name})
        else:
            print('爬取完毕')
        '''
        next_url = response.xpath('.//a[@title="下一页"]/@href').extract_first()
        url = 'https://www.amazon.cn'+ next_url
        if next_url.strip():
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)
        else:
            print('爬取完毕')
        '''


# 5分钟 3650 条


        

        


