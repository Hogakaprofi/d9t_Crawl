import scrapy


class EdgarSpider(scrapy.Spider):
    name = "edgar"
    allowed_domains = ["www.shop.edgarfuchs.com"]
    start_urls = ["https://www.shop.edgarfuchs.com/"]

    def parse(self, response):
        pass
