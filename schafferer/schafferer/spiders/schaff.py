import scrapy


class SchaffSpider(scrapy.Spider):
    name = "schaff"
    allowed_domains = ["www.schafferer.de"]
    start_urls = ["https://www.schafferer.de/gastro/"]

    seen_urls = set()

    ignore_urls = {'https://www.schafferer.de/gastro/Marken/',
                   'https://www.schafferer.de/gastro/Themen/'}

    # Scrape the Main-Page (Startseite)
    def parse(self, response):
        # scrape the ul element in which the categories are located
        main_categories = response.xpath('//*[@id="header"]/div[2]/div[2]/div/nav/ul/li[1]/ul')

        # get all links of the first a tag in the li element
        categories = main_categories.xpath('./li/a[1]/@href').extract()

        for category in categories:

            category_url = response.urljoin(category.strip())

            if category_url not in self.ignore_urls:
                yield response.follow(category_url, callback=self.parse_subcategories)

    # Scrape subcategories
    def parse_subcategories(self, response):
        sub_categories = response.css('div.manufacturer-series div.col-md-4')

        relative_urls = sub_categories.xpath('./a[1]/@href').extract()

        for sub_category in relative_urls:
            category_url = response.urljoin(sub_category.strip())
            yield response.follow(category_url, callback=self.parse_if_subcategories)

    # check whether the following link is a filter page or a category page
    def parse_if_subcategories(self, response):

        filterbox = response.css('div.filterBox')

        if filterbox:
            yield response.follow(response.url, callback=self.parse_get_data)
        else:
            subsub_categories = response.css('div.manufacturer-series div.col-md-4')
            relative_urls = subsub_categories.xpath('./a[1]/@href').extract()
            for sub_category in relative_urls:
                category_url = response.urljoin(sub_category.strip())
                yield response.follow(category_url, callback=self.parse_get_data)

    # scrape the categories and the filter from filter page
    def parse_get_data(self, response):

        # define lists
        Title_list = []
        Category_list = []

        # Get all filter and Categories
        all_filter = response.css('div.filterItemHeader')
        all_categories = response.css('ol.breadcrumb li')

        # Filter
        for filtered in all_filter:
            Title_list.append(filtered.css('span::text').get().strip())

        # Categories
        for idx, li in enumerate(all_categories):
            if idx == len(all_categories) - 1:  # Letztes <li> Element
                # Extrahiere den Text des <span> Tags
                span_text = li.xpath('.//span/text()').get()
                if span_text:
                    Category_list.append(span_text.strip())
            else:  # Alle anderen <li> Elemente
                # Extrahiere den Text des <a> Tags
                a_text = li.xpath('.//a/text()').get()
                if a_text:
                    Category_list.append(a_text.strip())

        # Output
        yield {
            'Kategorie': Category_list,
            'Filter_namen': Title_list,
            'Third_Url': response.url,
        }
