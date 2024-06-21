import scrapy


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["flomamo-services.de"]
    start_urls = ["https://hinweis.flomamo-services.de/Login/"]

    def parse(self, response):
        # Hier sind die Felder des Anmeldeformulars
        return scrapy.FormRequest.from_response(
            response,
            formdata={'benutzername': '*******', 'passwort': '********'},
            callback=self.after_login
        )

    def after_login(self, response):
        # Überprüfe, ob die Anmeldung erfolgreich war, indem du nach spezifischen Inhalten suchst
        if b"authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        self.logger.info(response.url)
        page_title = response.xpath('//title/text()').get()
        self.logger.info(f"Page title: {page_title}")