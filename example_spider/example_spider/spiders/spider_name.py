import scrapy
from ..items import ExampleSpiderItem
class SpiderNameSpider(scrapy.Spider):
    name = "spider_name"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response):
        """解析每页的电影信息"""
        # 1. 提取当前页所有电影节点
        movie_list = response.xpath("//ol[@class='grid_view']/li")

        for movie in movie_list:
            # 2. 提取字段（XPath定位，适配豆瓣页面结构）
            item = ExampleSpiderItem()
            # 电影名
            item["title"] = movie.xpath(".//span[@class='title'][1]/text()").extract_first()
            # 评分
            item["score"] = movie.xpath(".//span[@class='rating_num']/text()").extract_first()
            # 简介（处理空值）
            intro = movie.xpath(".//span[@class='inq']/text()").extract_first()
            item["intro"] = intro if intro else "无简介"

            # 3. 输出数据（交给管道/导出）
            yield item

        # 4. 爬取下一页（分页逻辑）
        next_page = response.xpath("//span[@class='next']/a/@href").extract_first()
        if next_page:
            # 拼接完整URL，继续爬取
            next_url = "https://movie.douban.com/top250" + next_page
            yield scrapy.Request(url=next_url, callback=self.parse)
