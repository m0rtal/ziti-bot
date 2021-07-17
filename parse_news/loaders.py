from itemloaders.processors import TakeFirst, Join, MapCompose
from scrapy.loader import ItemLoader


def clear_text(text: str) -> str:
    try:
        text = text.replace("&quot;", "'").replace("&rsquo;", "'")
    except ValueError as err:
        print(err)
    return text


class GazzettaLoader(ItemLoader):
    default_item_class = dict
    foreign_id_out = TakeFirst()
    url_out = TakeFirst()
    title_in = MapCompose(clear_text)
    title_out = TakeFirst()
    image_out = TakeFirst()
    image_alt_in = MapCompose(clear_text)
    image_alt_out = TakeFirst()
    content_in = MapCompose(clear_text)
    content_out = Join(separator="\n")
