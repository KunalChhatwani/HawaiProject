import scrapy

class HealthSpider(scrapy.Spider):
    name = "health"
    allowed_domains = ["health.hawaii.gov"]

    def start_requests(self):
        urls = ['https://health.hawaii.gov/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Extract the main text content
        main_text = response.xpath('//text()').getall()
        main_text = ' '.join(main_text).strip()

        # Save the main text to a .txt file
        filename = 'healthinfo.txt'
        with open(filename, 'a') as f:
            f.write(main_text + '\n')
        self.log('Saved file %s' % filename)

        # Follow links to other pages
        for href in response.css('a::attr(href)').getall():
            url = response.urljoin(href)
            if 'health.hawaii.gov' in url:
                yield scrapy.Request(url, self.parse)
