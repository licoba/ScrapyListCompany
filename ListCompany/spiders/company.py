import scrapy

class CompanySpider(scrapy.Spider):
    # python爬虫的名称
    name = 'company'
    # 能够将不在这个列表中的url剔除掉，等于是白名单把，如果这里不配置好，后面的scrapy.Request 将直接返回失败
    allowed_domains = ['listcompany.org']
    # 初始的url  这里是总表
    start_urls = ['https://www.listcompany.org/Consumer_Electronics_Industry.html']

    def parse(self, response):
        # 获取右边的所有链接
        right_href_list = response.xpath(
            '//div[@class="all-rgt fr"]/div[@class="the05 border01"]/div[@class="body"]/ul/li/a/@href').extract()
        for right_href in right_href_list:
            print('right href:' + right_href)
            # 生成一个request请求
            req = scrapy.Request(url=right_href, callback=self.parse_right_click)
            # # 生成一个任务？（-------这里还是没有理解，后面再弄）
            yield req
        pass

    # 处理点击右边的按钮，返回的结果
    def parse_right_click(self, response):
        print('处理右边链接的返回结果:-)')
        pass
