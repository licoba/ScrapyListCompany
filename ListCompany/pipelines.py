import os
import csv
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# pipeline是需要注册的

class ListcompanyPipeline():

    def __init__(self):
        # csv文件的位置,无需事先创建
        store_file = os.path.dirname(__file__) + '/spiders/contacts.csv'
        # 打开(创建)文件
        self.file = open(store_file, 'w')
        # csv写法
        self.writer = csv.writer(self.file)

        self.writer.writerow(["国家/地区", "地址", "官网", "业务类型", "联系人", "职务", "电话"])

    # spiders 里面如果传出了item, 那么就会调用这里, 每个item都会走的
    def process_item(self, item, spider):
        # print('process_item')
        country = item['country']
        address = item['address']
        website = item['website']
        business_type = item['business_type']
        contact_person = item['contact_person']
        job_title = item['job_title']
        tel_link = item['tel_link']

        self.writer.writerow([country, address, website, business_type, contact_person, job_title, tel_link])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
