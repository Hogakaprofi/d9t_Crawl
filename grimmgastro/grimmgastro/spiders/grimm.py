import scrapy


class GrimmSpider(scrapy.Spider):
    name = "grimm"
    allowed_domains = ["www.grimm-gastrobedarf.de"]
    start_urls = ["https://www.grimm-gastrobedarf.de/"]

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()


