# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# pipeline是需要注册的

class ListcompanyPipeline():
    # spiders 里面如果传出了item, 那么就会调用这里, 每个item都会走的
    def process_item(self, item, spider):
        print('process_item')
        country = item['country']
        address = item['address']
        website = item['website']
        contact_person = item['contact_person']
        job_title = item['job_title']
        tel_link = item['tel_link']

        return item
