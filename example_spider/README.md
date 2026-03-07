pip install scrapy
scrapy startproject my_first_spider
进入项目目录
cd my_first_spider

格式：scrapy genspider 爬虫名 目标域名
scrapy genspider douban top250.douban.com
启动：
scrapy crawl douban -o douban_top250.json

//	匹配任意位置的节点（相对路径）	//div 匹配所有<div>
/	匹配直接子节点（绝对路径 / 层级）	/html/body 匹配<body>
.	匹配当前节点（嵌套提取必用）	./a 匹配当前节点下的<a>
@属性名	提取节点的属性值	//img/@src 提取图片链接
text()	提取节点的文本内容	//h1/text() 提取<h1>文本
[@属性=值]	按属性筛选节点	//a[@class="btn"]
contains()	模糊匹配属性 / 文本	//div[contains(@class,"box")]
position()	按位置筛选（如第 2 个节点）	//li[position()=2]
[1]	位置筛选条件	在前面匹配到的所有符合条件的 span 节点中，
                只取第 1 个（XPath 中位置索引从 1 开始，而非 0）。 .//span[@class='title'][1]/text()

文本提取的坑：text() 只提取直接文本，若节点内有子标签，需用 //text() 提取所有子文本，再拼接。
空值处理：优先使用 get()/getall()（Scrapy 1.5+ 推荐），替代旧的 extract_first()/extract()，
        无结果时返回 None/ 空列表，避免报错。
