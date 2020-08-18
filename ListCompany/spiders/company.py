import scrapy
import json


class CompanySpider(scrapy.Spider):
    # python爬虫的名称
    name = 'company'
    # 能够将不在这个列表中的url剔除掉，等于是白名单把，如果这里不配置好，后面的scrapy.Request 将直接返回失败
    allowed_domains = ['listcompany.org']
    # 初始的url s 这里是总表
    start_urls = ['https://www.listcompany.org/Consumer_Electronics_Industry.html']
    all_urls = []

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
            req = scrapy.Request(url=right_href, callback=self.parse_right_click_link, priority=index + 1)
            # 生成一个任务？（-------这里还是没有理解，后面再弄）
            # 同时抛出多个请求，这里的任务是异步任务，我们需要做成同步的，将并发数量设置为1，能否保持同步？
            # 可以看到这里还是不行的
            yield req

        pass

    # 处理点击右边的按钮，返回的结果：有分页的递归处理，没有分页的，交给deal content去处理（废弃）
    # 这个函数只进行多页链接的获取
    def parse_right_click_link(self, response):
        country_name = response.xpath('//div[@class="all-posi"]/h3/a[1]/text()').extract_first()
        max_page = 1  # 最大的页码数

        # response.xpath('//div[@class="pagea"]/ul/b/text()').extract_first() 只有一页的时候可以用这个获取
        # 下一页的链接是一个分链接 '/Consumer_Electronics_In_Germany/p2.html'
        # 如果没有下一页的链接，会返回空
        next_btn_link = response.xpath('//div[@class="pagea"]/ul/a[@title="Next"]/@href').extract_first()
        if (next_btn_link):
            max_page = int(response.xpath('//div[@class="pagea"]/ul/a[last()-2]/text()').extract_first())
        print('国家 :' + country_name, "，最大页数：", max_page)
        country_links = self.get_links(response.url, page_count=max_page)
        # print('country_links :', country_links)
        dictionary = {'country': country_name, 'links': country_links}
        self.all_urls.append(dictionary)

        f = open('all_urls.json', 'w+')
        f.write(json.dumps(self.all_urls))
        # print(self.all_urls)

        pass

    # get all links
    def get_links(self, first_link, page_count):
        link_list = [first_link]
        if page_count < 2:
            return link_list
        for index in range(page_count - 1):
            every_link = first_link.split('.html')[0] + '/p' + str(index + 2) + '.html'
            link_list.append(every_link)
        return link_list

    def parse_right_click_content(self, response):
        print('处理内容结果 content:-)')
        pass
