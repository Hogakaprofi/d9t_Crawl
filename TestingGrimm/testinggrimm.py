import scrapy
from scrapy.http import Response
import random
from typing import Any


class GrimmSpider(scrapy.Spider):
    name = "grimm"
    allowed_domains = ["www.grimm-gastrobedarf.de"]
    start_urls = ["https://www.grimm-gastrobedarf.de/"]

    seen_urls = set()

    ignore_urls = {'https://www.grimm-gastrobedarf.de/unsere-marken.html',
                   'https://www.grimm-gastrobedarf.de/sale.html'}

    # Scrape the Main-Page (Startseite)
    def parse(self, response):
        # Get all main categorys of main-page (https://www.grimm-gastrobedarf.de/)
        all_categories = response.css('a.s360-megamenu__link.s360-megamenu__link--category')

        for category in all_categories:
            # Main Page Urls (Links)
            relative_url = category.css('a ::attr(href)').get()
            if relative_url not in self.ignore_urls:
                yield response.follow(relative_url, callback=self.parse_second_category_page)

    # Scrape the individual categories (2. Ebene)
    def parse_second_category_page(self, response):
        # Get all the individual links of the individual main page categoies
        second_categories = response.css('a.category-name')

        for second_category in second_categories:
            # Main Page Urls (Links)
            sec_relative_url = second_category.css('a ::attr(href)').get()
            yield {
                'Response lvl': response.url,
                'Second lvl': sec_relative_url.url,
            }