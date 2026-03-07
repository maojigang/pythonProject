# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import sys

# 关键：将项目根目录加入Python路径，确保能找到爬虫模块
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

if __name__ == '__main__':
    # 获取项目的配置（如settings.py中的配置）
    settings = get_project_settings()
    # 创建爬虫进程
    process = CrawlerProcess(settings)

    # 替换成你的爬虫名称（和spiders目录下的爬虫name一致）
    spider_name = "spider_name"

    # 启动爬虫（核心：这里可以打断点调试）
    process.crawl(spider_name)
    process.start()  # 启动爬虫进程，阻塞直到爬虫结束