import scrapy

class TtableSpider(scrapy.Spider):
    name = "ttable"
    allowed_domains = ["www.top-table.gmbh"]
    start_urls = ["https://www.top-table.gmbh/"]

    seen_urls = set()
    ignore_urls = {'https://www.top-table.gmbh/Besteck/Steakbesteck'}

    other_urls = {'https://www.top-table.gmbh/Kochmesser//'}
    test_urls = {'https://www.top-table.gmbh/Servieren-Transportieren//', 'https://www.top-table.gmbh/Buffet//',
                 'https://www.top-table.gmbh/Kueche//', 'https://www.top-table.gmbh/Desinfektion-Hygiene//'}

    # Scrape the Main-Page (Startseite)c
    def parse(self, response):
        # Get all main categorys of main-page (https://www.grimm-gastrobedarf.de/)
        main_categories = response.css('a.main-navigation-link')

        for main_category in main_categories:
            # Main Page Urls (Links)
            relative_url = main_category.css('a ::attr(href)').get()
            if relative_url in self.other_urls:
                yield response.follow(relative_url, callback=self.parse_other_category_page)
            elif relative_url in self.test_urls:
                yield response.follow(relative_url, callback=self.parse_second_category_page)
            else:
                yield response.follow(relative_url, callback=self.parse_test_category_page)

    # Second
    def parse_second_category_page(self, response):
        Title_list = []
        Filter_list = []

        all_categories = response.css('ul.category-navigation.level-1 li.category-navigation-entry')
        all_filter = response.css('div.filter-multi-select')

        # Categories
        for category in all_categories:
            Title_list.append(category.css('a::text').get().strip())

        # Filter
        for filtered in all_filter:
            items = filtered.css('label.filter-multi-select-item-label')
            selection_str = ''
            for item in items:
                selection_str += item.css('label.filter-multi-select-item-label::text').get().strip() + ", "

            Filter_list.append(
                filtered.css('button.filter-panel-item-toggle::text').get().strip() + ': ' + selection_str)

        yield {
            'Url': response.url,
            'Title': Title_list,
            'Filter': Filter_list
        }

    def parse_test_category_page(self, response):
        more_categories = response.css('div.cms-element-image')

        for more_category in more_categories:
            # Main Page Urls (Links)
            sub_relative_url = more_category.css('a ::attr(href)').get()
            if sub_relative_url:
                yield response.follow(sub_relative_url, callback=self.parse_second_category_page)
            else:
                pass

    # Scrape the other pages
    def parse_other_category_page(self, response):

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
            'Url': response.url,
            'Title': 'Kochmesser',
            'Filter_namen': Filter_list,
        }