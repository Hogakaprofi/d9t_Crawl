import scrapy

class TtableSpider(scrapy.Spider):
    name = "ttable"
    allowed_domains = ["www.top-table.gmbh"]
    start_urls = ["https://www.top-table.gmbh/"]

    seen_urls = set()

    ignore_urls = {'https://www.top-table.gmbh/Kochmesser//'}

    # Scrape the Main-Page (Startseite)
    def parse(self, response):
        # Get all main categorys of main-page (https://www.grimm-gastrobedarf.de/)
        main_categories = response.css('a.main-navigation-link')

        for main_category in main_categories:
            # Main Page Urls (Links)
            relative_url = main_category.css('a ::attr(href)').get()
            if relative_url not in self.ignore_urls:
                yield response.follow(relative_url, callback=self.parse_second_category_page)
            else:
                yield response.follow(relative_url, callback=self.parse_ignore_category_page)

    # Second
    def parse_second_category_page(self, response):
        pass

    # Scrape the ignore pages
    def parse_ignore_category_page(self, response):

        Filter_list = []
        all_filter = response.css('div.filter-multi-select')

        for filtered in all_filter:
            items = filtered.css('label.filter-multi-select-item-label')
            selection_str = ''
            for item in items:
                selection_str += item.css('label.filter-multi-select-item-label::text').get().strip() + ", "

            Filter_list.append(
                filtered.css('button.filter-panel-item-toggle::text').get().strip() + ': ' + selection_str)

        yield {
            'Filter_namen': Filter_list,
            'Url': response.url,
        }
