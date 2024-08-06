import scrapy


class HinscheSpider(scrapy.Spider):
    name = "hinsche"
    allowed_domains = ["www.hinsche-onlineshop.de"]
    start_urls = ["https://www.hinsche-onlineshop.de/produkte/"]

    def parse(self, response):
        # Check for filters
        all_filter = response.css('div.product-filter-accordian:first-of-type')
        # Check if filter is there (Yes: Get all data ; No: Get more Links and go to parse)
        if all_filter:
            # self.logger.info('Beginne das Scrapen der Seite: %s', response.url)
            # Get the Title of Categoies
            category_list = []
            all_categories = response.css('div.breadcrumbs li:not(:first-child)')
            for category in all_categories:
                category_list.append(category.css('a::text').get())

            # Get Filter
            filter_list = []
            allfilter = all_filter.css('a.product-filter-down')
            ultags = all_filter.css('ul.sub-category')
            # print(len(allfilter))
            # print(len(ultags))

            if len(allfilter) == len(ultags):
                for filters, sub_filter in zip(allfilter, ultags):
                    a_text = filters.css('span:nth-of-type(2)::text').get() + ': '
                    li_texts = sub_filter.css('li a span:nth-of-type(1)::text').getall()

                    result = a_text + ", ".join(li_texts)
                    filter_list.append(result)
            else:
                self.log("Geht nicht!")

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
            allcategories = response.css('div.white-databox')
            categories = allcategories.css('div.service-box')
            for category in categories:
                # Extract Urls
                relative_url = category.css('p.service-links a::attr(href)').get()

                if relative_url:
                    # Follow the link to the next category page and call the same parse method
                    yield response.follow(relative_url, callback=self.parse)
