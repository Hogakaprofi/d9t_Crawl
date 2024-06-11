import scrapy
import random


class GgmSpider(scrapy.Spider):
    name = "ggm"
    allowed_domains = ["www.ggmgastro.com"]
    start_urls = ["https://www.ggmgastro.com/de-de-eur"]

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 OPR/75.0.3969.218',
        'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36',
        'Mozilla/5.0 (Android 11; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.0 Chrome/90.0.4430.93 Mobile Safari/537.36',
        'Opera/9.80 (Android; Opera Mini/51.0.2254/190.255; U; en) Presto/2.12.423 Version/12.16'
    ]

    def parse(self, response):
        # all_category = response.xpath("//ul[@class='row wrap m0 p0 relative']/li[@class='main-menu__item
        # col-xs/div[@class='subcategory-item']/a ::attr(href)")

        # get all css-tags with the followling class
        all_category = response.css('subcategory-item')

        # Run through all css tags and get the links of the individual css tags
        for category in all_category:
            relative_url = category.css('a ::attr(href)').get()
            # Follow the individual Links and get data with the self.parse_subcategory method.
            yield response.follow(relative_url, callback=self.parse_subcategory, headers={
                "User-Agent": self.USER_AGENTS[random.randint(0, len(self.USER_AGENTS) - 1)]})

    def parse_subcategory(self, response):
        yield {
            'url': response.url,
            'sub_category': response.xpath(
                "//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        }
