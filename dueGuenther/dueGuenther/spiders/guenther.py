import scrapy


class GuentherSpider(scrapy.Spider):
    name = "guenther"
    allowed_domains = ["shop.due-guenther.de"]
    start_urls = ["https://shop.due-guenther.de/produkte/"]

    def parse(self, response):
        # Check for filters
        all_filter = response.css('div.product-filter-accordian')
        # Check if filter is there (Yes: Get all data ; No: Get more Links and go to parse)
        if all_filter:
            self.logger.info('Beginne das Scrapen der Seite: %s', response.url)
            # Get the Title of Categoies
            category_list = []
            all_categories = response.css('div.breadcrumbs li:not(:first-child)')
            for category in all_categories:
                category_list.append(category.css('a::text').get())

            # Get Filter
            filter_list = []
            for filters in all_filter:
                items = filters.css('ul.sub-category')
                selection_str = ''
                for item in items:
                    selection_str += item.css('span:nth-of-type(1)::text').get().strip() + ", "

                filter_list.append(
                    filters.css(
                        'a.product-filter-down span:nth-of-type(2)::text').get().strip() + ': ' + selection_str)

            # Get more data
            data_list = []
            more_data = response.css('div.service-box')
            for data in more_data:
                data_list.append(data.css('p.service-links a::attr(title)').get())
            # Output in json file
            yield {
                'Url': response.url,
                'Title': category_list,
                'Filter': filter_list,
                'Data': data_list
            }
        #
        else:
            print(response.url)
            # Get all Links of categories from the current page
            categories = response.css('ul.level0.clearfix')
            for category in categories:
                # Extract Urls
                relative_url = category.css('p.service-links a::attr(href)').get()

                if relative_url:
                    # Follow the link to the next category page and call the same parse method
                    yield response.follow(relative_url, callback=self.parse)
