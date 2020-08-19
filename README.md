# ScrapyListCompany
ListCompany的爬虫项目，用来爬取用户资料

需要爬取的网站：https://www.listcompany.org/Consumer_Electronics_Industry.html

### 入门资料
- https://zhuanlan.zhihu.com/p/21479334

入门那当然还是从scrapy开始了

- scrapy官网：https://scrapy.org/
- 官方文档：https://docs.scrapy.org/en/latest/

首先安装scrapy
```
 pip3 install scrapy
```

生成项目`scrapy startproject ListCompany`

设置python解释器为系统的python3.7的python解释器，这个解释器已经安装了scrapy的库

在settings里面设置

![](https://pic.downk.cc/item/5f3a2ede14195aa594948c18.jpg)

然后生成爬虫
```
scrapy genspider company listcompany.org
```

开始执行，首先爬取第一页的网页内容，保存到index.html(爬虫的名字叫company)
```
scrapy crawl company
```

也可以写一个脚本，用pycharm来执行
```
from scrapy.cmdline import execute

execute(['scrapy', 'crawl', 'company'])
```

执行的结果

![](https://pic.downk.cc/item/5f3a36bc14195aa59496e27d.jpg)

看一下robots https://www.listcompany.org/robots.txt

```
User-agent: *
Disallow: /ajax_check*
Disallow: /stat.php*
```
说明以上这些内容是不让爬的，当然我们也不是爬的这个，所以并不会违法犯罪，放心操作好了。


### 使用scrapy shell

python有python shell，scrapy同样也可以用命令行
```
scrapy shell https://www.listcompany.org/Consumer_Electronics_Industry.html
```

这里因为访问的网站再墙外，所以需要挂代理

![](https://pic.downk.cc/item/5f3a518c14195aa5949eb4e2.jpg)


这里引入一个新的知识点：xpath

XPath入门文档：https://www.w3school.com.cn/xpath/index.asp

> XPath 是一门在 XML 文档中查找信息的语言。XPath 可用来在 XML 文档中对元素和属性进行遍历。

可以利用Xpath来代替正则表达式，用于筛选html的元素

### 一、提取右边的链接

首先要获取右侧的所有种类链接，这里当然是Chrome浏览器的审查元素

![](https://pic.downk.cc/item/5f3a666514195aa594a4024e.jpg)

右键其中的一个标签进行检查，可以看到其中的a标签对应的源代码
![](https://pic.downk.cc/item/5f3a534714195aa5949f1fd9.jpg)


接着在shell里面对所有的a标签进行筛选
因为a标签没有明显的class类，不便于筛选，所以换一个思路：

找到它的父节点，然后去便利它的子节点，来获取所有的href

总共需要筛选5层
![](https://pic.downk.cc/item/5f3a561014195aa594a00c60.jpg)

1、选择class为 all-rgt fr 的div标签
```
response.xpath('//div[@class="all-rgt fr"]')
```

2. 选取子元素为 class = the05 border01 的div元素
```
 response.xpath('//div[@class="all-rgt fr"]//div[@class="the05 border01"]')
```
3. 筛选body的div
```
response.xpath('//div[@class="all-rgt fr"]//div[@class="the05 border01"]//div[@class="body"]')
```
4. 筛选ul标签 
```
response.xpath('//div[@class="all-rgt fr"]//div[@class="the05 border01"]//div[@class="body"]//ul')
```

5. 筛选所有的li标签
```
 response.xpath('//div[@class="all-rgt fr"]//div[@class="the05 border01"]//div[@class="body"]//ul//li')
```

最后可以看到筛选出来了一个数组

![](https://pic.downk.cc/item/5f3a57f714195aa594a0804a.jpg)

6. 然后对数组进行提取，，一个item是一个Selector对象，单个的item是这样：
```
<Selector xpath='//div[@class="all-rgt fr"]//div[@class="the05 border01"]//div[@class="body"]//ul//li' data='<li><a href="https://www.listcompany....'>
```


还没有完，再选取a标签，提取href的值：

选取用两个//，提取属性值用 @符号

7. 完整的提取所有href的值的表达式：
```
 response.xpath('//div[@class="all-rgt fr"]//div[@class="the05 border01"]//div[@class="body"]//ul//li//a/@href')

```

8. 提取之后对数据进行分割，使用extract函数来获取data的值，以下命令：
```
response.xpath('//div[@class="all-rgt fr"]/div[@class="the05 border01"]/div[@class="body"]/ul/li/a/@href').extract()
```

可以看到右边侧边栏的链接，终于出来了：


![](https://pic.downk.cc/item/5f3a597114195aa594a0ceb9.jpg)

甚是欣慰！


### 二、模拟链接访问

得到了链接之后，我们对每一个链接进行访问，并将返回的结果交给另一个parse函数进行解析处理

这里我们定义一个函数 parse_right_click 来处理点击右边的链接，获取到的返回内容

可以料想到，左边返回的肯定也是一个html，也是需要用xpath来解析，然后来得到相应的链接的


这里遇到一个问题，就是分页链接的爬取

又有一个新的知识点：CrawlSpider

这里有一篇博客，介绍了下一页、翻页的操作
https://www.jianshu.com/p/0c957c57ae10

大致思路：利用回调，获取下一页的链接，交给自己进行处理就好了。


#### 同步任务

实际上scrapy不能像js，用await来实现同步请求，例如以下这段代码：
```
for right_href in right_href_list:
    print('right href:' + right_href)
    # 生成一个request请求
    req = scrapy.Request(url=right_href, callback=self.parse_right_click_link)
    yield req
```
比如right_href_list.length = 20
 首先，程序会打印出20 个log，然后同时抛出多个(20个)请求，这里的任务是异步任务，
 这些任务会被放到一个任务栈，我们需要做成同步的
 - 将并发数量设置为1，能否保持同步？
 -->结果是虽然可以保证任务一次只执行一个，但是并不能保证执行的顺序，有可能最先执行的是最后yeild的任务，并且也不能在里面继续插入其它请求了，只能放在队尾
 所以这个方案还是行不通
 
 
 
 所以这里产生了一个想法：
 
自己维护一个列表， 首先爬取链接，将链接按照顺序放进去，这个我们是可以保证的。
 
 然后针对列表里面的链接，进行遍历，再逐个爬取每个链接对应的网页内容。
 
 在这里更好地保证任务的同步，确保有顺序、同步地访问每一个链接
 
 ### 保证yeild的执行顺序（难点）
 yeild是没有顺序的，并不是像我理解的队列执行，执行的顺序完全是随机的
 
 不过这里想了想，好像也没有必要保证顺序执行，乱序也没有什么影响的
 
 ### 分页爬取的优化
 
 其实爬取一些之后我们就能够了解到规律了，类似`/Consumer_Electronics_In_Vietnam/p2.html`的链接，我们完全可以自己构造的，
 并且如果真是去爬取的，如果有些页面有200页，300页，获取分页链接的时长太长了，我们可以直接获取页面的数值就好了，自己构造每个页面的链接

 
 ### 防盗文字的处理
 可以看到这个网站为了防止信息被爬取, 对最重要的电话号码进行了防盗处理  
 ![](https://pic.downk.cc/item/5f3c8a2714195aa59473edf2.jpg)
 号码在网站上面展示的是一个图片, 而不是文字, 所以我们首先爬取它的所有图片链接, 然后对图片进行批量下载, 最后再使用OCR进行批量的图片识别
 
 
 这样来实现图片号码转文字号码的目的
 
 ### 多线程下载图片
 
 链接我们已经爬取下来了, 接下来要做的就是访问每一个链接, 对图片进行下载, 考虑到这里的图片有三万多张 , 所以我们必须要使用多线程来加快下载的速度
 
 