import scrapy


class HogakaSpider(scrapy.Spider):
    name = "hogaka"
    allowed_domains = ["shop.hogakaprofi.de"]
    start_urls = ["https://shop.hogakaprofi.de/"]

    def parse(self, response):
        pass
