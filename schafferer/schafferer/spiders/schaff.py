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
        # Get all main categorys of main-page
        main_categories = response.xpath('//*[@id="header"]/div[2]/div[2]/div/nav/ul/li[1]/ul')

        # Verwende XPath innerhalb des ausgewählten `ul`-Elements, um das `a`-Tag direkt nach dem `li`-Tag zu scrapen
        categories = main_categories.xpath('./li/a[1]/@href').extract()

        for category in categories:

            category_url = response.urljoin(category.strip())

            if category_url not in self.ignore_urls:
                yield response.follow(category_url, callback=self.parse_subcategories)

    def parse_subcategories(self, response):
        sub_categories = response.css('div.manufacturer-series div.col-md-4')

        relative_urls = sub_categories.xpath('./a[1]/@href').extract()

        for sub_category in relative_urls:
            category_url = response.urljoin(sub_category.strip())
            yield response.follow(category_url, callback=self.parse_if_subcategories)

    def parse_if_subcategories(self, response):

        # Schauen ob ein besimmtes html tag oder css usw. gibt und dann entscheiden
        # Wen das tag oder was auch immer da ist, dann mache das gleiche wie parse_subcategories
        # Andernfalls geb den link weiter an parse_get_data!

        filterbox = response.css('div.filterBox')

        if filterbox:
            yield response.follow(response.url, callback=self.parse_get_data)

        else:
            subsub_categories = response.css('div.manufacturer-series div.col-md-4')

            relative_urls = subsub_categories.xpath('./a[1]/@href').extract()

            for sub_category in relative_urls:
                category_url = response.urljoin(sub_category.strip())
                yield response.follow(category_url, callback=self.parse_if_subcategories)

    def parse_get_data(self, response):

        # Get all filter
        all_filter = response.css('div.filterItemHeader')
        Title_list = []

        for filtered in all_filter:
            Title_list.append(filtered.css('span::text').get().strip())

        yield {
            'Kategorie': response.xpath("/html/body/div[2]/div[1]/div/div/div/div[1]/ol/li[2]/a/text()").get(),
            'Unter-Kategorie': response.xpath("/html/body/div[2]/div[1]/div/div/div/div[1]/ol/li[3]/span/text()").get(),
            'Filter_namen': Title_list,
            'Third_Url': response.url,
        }
