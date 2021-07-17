from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parse_news.spiders.gazzetta import GazzettaSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("parse_news.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(GazzettaSpider)
    crawler_process.start()
