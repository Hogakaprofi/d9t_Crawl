
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
            yield response.follow(sec_relative_url, callback=self.parse_third_category_page)

   # Scrape the individual categories of the second website (3. Ebene)
    def parse_third_category_page(self, response):
        # Check if filters are present
        categoryThere = response.css('div.card.product-box.category-body').get()

        if categoryThere:
            # Get all the individual links of the individual main page categoies
            second_categories = response.css('a.category-name')

            for second_category in second_categories:
                # Main Page Urls (Links)
                third_relative_url = second_category.css('a ::attr(href)').get()
                yield response.follow(third_relative_url, callback=self.parse_fourth_category_page)
        else:
            yield response.follow(response.url, callback=self.parse_fourth_category_page)

    # Scrape the individual Links for the products (4. Ebene)
    def parse_fourth_category_page(self, response):
        # Get all filter divs
        all_filter = response.css('div.filter-panel-item')
        Filter_list = []

        for filtered in all_filter:
            selection_filter = [item.strip() for item in filtered.css('li.filter-multi-select-list-item label::text').getall()]
            if selection_filter:   
                Filter_list.append(filtered.css('button.filter-panel-item-toggle::text').get().strip() + ": " + "; ".join(selection_filter))
            else:
                Filter_list.append(filtered.css('button.filter-panel-item-toggle::text').get().strip() + ": ---")

        yield {
            'First_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[1]/a/span/text()").get(),
            'Second_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[2]/a/span/text()").get(),
            'Third_Title': response.xpath("/html/body/main/div[2]/div/nav/ol/li[3]/a/span/text()").get() or "---",
            'Filter_namen': Filter_list,
            'Third_Url': response.url,
        }
