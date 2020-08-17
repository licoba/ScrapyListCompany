from scrapy.cmdline import execute

# execute(['scrapy', 'crawl', 'company'])
execute(('scrapy crawl company').split())
