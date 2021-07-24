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
        for article in articles:
            section = " ".join(article["section"]).lower()
            if "calcio" in section and article["type"] != "video":
                follow_url = article.get("json", None)
                if follow_url: # and follow_url not in parsed_urls:
                    yield response.follow(article["json"], callback=self.parse_article)

    def parse_article(self, response):
        loader = GazzettaLoader(response=response)

        valid_json = " ".join(response.text.split()).replace(", , ", ", ")
        json_load = json.loads(valid_json)
        img_url, img_alt = None, None

        if json_load.get("featureImage").get("content") and json_load.get("featureImage").get("caption"):
            img_url = json_load.get("featureImage").get("content")
            img_alt = json_load.get("featureImage").get("caption")
        else:
            for item in json_load["contentBody"]:
                if item["type"] == "image-reference":
                    img_url = item["content"]
                    img_alt = item["caption"]

        article = {
            "foreign_id": json_load["id"],
            "url": json_load["url"],
            "title": json_load.get("headline", None),
            "image": img_url,
            "image_alt": img_alt,
            "content": (item["content"] for item in json_load["contentBody"] if
                        item["type"] == "paragraph" or item["type"] == "headline")
        }
        for key, value in article.items():
            loader.add_value(key, value)
        article = loader.load_item()

        if article["content"]:
            orm_database.add_unique_record(article, models.GazzettaArticle, "foreign_id")
