import unicodedata

import scrapy
import json

from database import models
from database.database import Database
from parse_news.loaders import GazzettaLoader

# orm_database = Database("postgresql://postgres:@192.168.1.11/test")
orm_database = Database("sqlite:///database.sqlite")


class GazzettaSpider(scrapy.Spider):
    name = 'gazzetta'
    allowed_domains = ["components2.gazzettaobjects.it", "gazzetta.it"]
    start_urls = ['https://components2.gazzettaobjects.it/rcs_gaz_searchapi/v1/latest.json']

    def parse(self, response):
        articles = response.json()["response"]["docs"]
        parsed_urls = (el.crawled_url for el in orm_database.get_crawled())
        for article in articles:
            section = " ".join(article["section"]).lower()
            if "calcio" in section and article["type"] != "video":
                follow_url = article.get("json", None)
                if follow_url and follow_url not in parsed_urls:
                    yield response.follow(article["json"], callback=self.parse_article)

    def parse_article(self, response):
        loader = GazzettaLoader(response=response)
        rawtext = unicodedata.normalize("NFKD", response.text).encode("ascii", "ignore").decode("utf8")
        json_load = json.loads(rawtext)
        article = {
            "foreign_id": json_load["id"],
            "url": json_load["url"],
            "title": json_load.get("headline", None),
            "image": json_load.get("featureImage", None).get("content", None),
            "image_alt": json_load.get("featureImage", None).get("caption", None),
            "content": (item["content"] for item in json_load["contentBody"] if
                        item["type"] == "paragraph" or item["type"] == "headline")
        }
        for key, value in article.items():
            loader.add_value(key, value)
        article = loader.load_item()

        if article["content"]:
            orm_database.add_record(article, models.GazzettaArticle, "foreign_id")
            orm_database.add_record({"crawled_url": response.url}, models.CrawledUrls, "crawled_url")
