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

    # Scrape the Main-Page

    def parse(self, response):
        # Get all main categorys of main-page (https://www.grimm-gastrobedarf.de/)
        all_categories = response.css('a.s360-megamenu__link.s360-megamenu__link--category')

        for category in all_categories:
            # Main Page Urls (Links)
            relative_url = category.css('a ::attr(href)').get()
            self.firstLink = relative_url
            # Main Page Urls (Title)
            ## self.category_title = category.css('a ::attr(title)').get()
            if relative_url not in self.ignore_urls:
                yield response.follow(relative_url, callback=self.parse_second_category_page)
                # headers={"User-Agent": self.USER_AGENT_LIST[random.randint(0, len(self.USER_AGENT_LIST)-1)]}

    # Scrape the individual categories
    def parse_second_category_page(self, response):
        print(f'Main_Category: {response.url}')
        # Get all the individual links of the individual main page categoies
        second_categories = response.css('a.category-name')

        for second_category in second_categories:
            # Main Page Urls (Links)
            sec_relative_url = second_category.css('a ::attr(href)').get()
            self.secondLink = sec_relative_url
            # Main Page Urls (Title)
            ##self.second_title = second_category.css('a ::attr(title)').get()
            yield response.follow(sec_relative_url, callback=self.parse_third_category_page)

    # Scrape the individual categories of the second website
    def parse_third_category_page(self, response):
        print(f'Second_Category: {response.url}')
        # Get all the individual links of the individual main page categoies
        second_categories = response.css('a.category-name')

        for second_category in second_categories:
            # Main Page Urls (Links)
            third_relative_url = second_category.css('a ::attr(href)').get()
            self.thirdLink = third_relative_url
            # Main Page Urls (Title)
            ##self.third_title = second_category.css('a ::attr(title)').get()
            yield response.follow(third_relative_url, callback=self.parse_fourth_category_page)

    # Scrape the individual Links for the products
    def parse_fourth_category_page(self, response):
        print(f'Third_Category: {response.url}')
        products = response.css('div.card-body')

        for product_data in products:
            product_url = product_data.css('div[3] a ::attr(href)').get()
            if product_url not in self.seen_urls:
                self.seen_urls.add(product_url)
                yield response.follow(product_url, callback=self.parse_fifth_category_page)

    # Scrape the individual Product Data of the individual products
    def parse_fifth_category_page(self, response):
        yield {
            'First_url': self.start_urls,
            'First_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[1]/a/span/text()").get(),
            'Second_url': self.firstLink,
            'Second_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[2]/a/span/text()").get(),
            'Third_url': self.secondLink,
            'Third_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[3]/a/span/text()").get(),
            'title': response.css('.product-detail-name-container h1::text').get(),
            'price': response.css('p.product-detail-price ::text').get(),
        }

    # For the Filter
    def parse_filter(self, response):
        print("Filter")

    # For the Sales Page
    def parse_sales(self, response):
        print("Sales webpage")
