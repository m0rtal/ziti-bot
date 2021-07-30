from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from database.database import Database
from parse_news.spiders.gazzetta import GazzettaSpider
from translate.translate_module import add_auto_translation, drop_to_excel

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("parse_news.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(GazzettaSpider)
    crawler_process.start()
    # orm_database = Database("postgresql://postgres:@192.168.1.11/test")
    orm_database = Database("sqlite:///database.sqlite")
    add_auto_translation(orm_database)
    drop_to_excel(orm_database)
    orm_database.import_translated()

