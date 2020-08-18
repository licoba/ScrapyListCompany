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
        last_btn_link = response.xpath('//div[@class="pagea"]/ul/a[@title="Last"]/@href').extract_first()
        if (last_btn_link):
            max_page = int(last_btn_link.split('.html')[0].split('/p')[1])
        # print('国家 :' + country_name, "，最大页数：", max_page)
        country_links = self.get_links(response.url, page_count=max_page)
        # print('country_links :', country_links)
        dictionary = {'country': country_name, 'links': country_links}
        self.all_urls.append(dictionary)
        # f = open('all_urls.json', 'w+')
        # f.write(json.dumps(self.all_urls))

        # 对每一个国家的country_links 进行访问,访问之后获取到每一个联系人的链接
        for one_page in country_links:
            req = scrapy.Request(url=one_page, callback=self.parse_one_page)
            yield req
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

    def parse_one_page(self, response):
        # print('处理单页内容')
        menber_list = response.xpath('//div[@class="the04 border01"]/div/ul/li/h4/a/@href').extract()
        for one_menber in menber_list:
            req = scrapy.Request(url=one_menber, callback=self.parse_menber_content)
            yield req
        pass

    # https://www.listcompany.org/Shenzhen_Penjoy_Technology_Co_Ltd_Info.html 处理单个人员的返回结果
    def parse_menber_content(self, response):
        # print('处理联系人详情')
        country = response.xpath(
            '/html/body/div[1]/div[3]/div/div[1]/div[1]/div[4]/ul/li[1]/span/text()').extract_first()
        address = response.xpath(
            '/html/body/div[1]/div[3]/div/div[1]/div[1]/div[4]/ul/li[2]/span/text()').extract_first()
        website = response.xpath(
            '/html/body/div[1]/div[3]/div/div[1]/div[1]/div[4]/ul/li[4]/span/text()').extract_first()

        contact_person = response.xpath(
            '/html/body/div[1]/div[3]/div/div[1]/div[1]/div[5]/ul/li[1]/span/text()').extract_first()
        job_title = response.xpath(
            '/html/body/div[1]/div[3]/div/div[1]/div[1]/div[5]/ul/li[3]/span/text()').extract_first()

        # print(country, address, website, contact_person, job_title)

        telephone_path = response.xpath('//div[@class="the09"]/ul/li/strong[contains(text(),"Telephone")]/../span/img/@src').extract_first()

        tel_link = 'https://www.listcompany.org' + str(telephone_path)
        print(contact_person, tel_link)
        pass
