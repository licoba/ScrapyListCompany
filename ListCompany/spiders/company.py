import scrapy


class CompanySpider(scrapy.Spider):
    # python爬虫的名称
    name = 'company'
    # 能够将不在这个列表中的url剔除掉，等于是白名单把，如果这里不配置好，后面的scrapy.Request 将直接返回失败
    allowed_domains = ['listcompany.org']
    # 初始的url s 这里是总表
    start_urls = ['https://www.listcompany.org/Consumer_Electronics_Industry.html']
    all_urls = ['https://www.listcompany.org/Consumer_Electronics_Industry.html']

    def parse(self, response):
        # 获取右边的所有链接
        right_href_list = response.xpath(
            '//div[@class="all-rgt fr"]/div[@class="the05 border01"]/div[@class="body"]/ul/li/a/@href').extract()
        right_country_list = response.xpath(
            '//div[@class="all-rgt fr"]/div[@class="the05 border01"]/div[@class="body"]/ul/li/a/text()').extract()
        for index, right_href in enumerate(right_href_list):
            # print('right country:' + right_country_list[index])
            # print('right href:' + right_href)
            # 生成一个request请求
            req = scrapy.Request(url=right_href, callback=self.parse_right_click_link, priority=index+1)
            # 生成一个任务？（-------这里还是没有理解，后面再弄）
            # 同时抛出多个请求，这里的任务是异步任务，我们需要做成同步的，将并发数量设置为1，能否保持同步？
            # 可以看到这里还是不行的
            yield req
        pass

    # 处理点击右边的按钮，返回的结果：有分页的递归处理，没有分页的，交给deal content去处理（废弃）
    # 这个函数只进行多页链接的获取
    def parse_right_click_link(self, response):
        print('处理右边链接的返回结果link :-)')
        # parse_right_click_content
        # 下一页的链接是一个分链接 '/Consumer_Electronics_In_Germany/p2.html'
        # 如果没有下一页的链接，会返回空
        next_btn_link = response.xpath('//div[@class="pagea"]/ul/a[@title="Next"]/@href').extract_first()
        if (next_btn_link):
            print('下一页链接：' + next_btn_link)
        pass

    def parse_right_click_content(self, response):
        print('处理内容结果 content:-)')
        pass
