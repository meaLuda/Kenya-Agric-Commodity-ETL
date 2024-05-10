import scrapy
import logging
import requests
from agriscrapper.items import AgriscrapperItem
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def is_valid_url(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False

def url_list():
    url_list = []
    for product_number in range(1,7000):
        url = f'https://amis.co.ke/index.php/site/market?product={product_number}&per_page=3000'
        if is_valid_url(url):
            url_list.append(url)
    
    return url_list

# log file
# logging.basicConfig(filename='kemis_commodities_scrapper.log', level=logging.INFO)

class KemisCommoditiesScrapperSpider(scrapy.Spider):
    name = "kemis_commodities_scrapper"
    allowed_domains = ["amis.co.ke"]
    url = 'https://amis.co.ke/index.php/site/market?product={}&per_page=3000'
    
    def start_requests(self):
        for product_number in range(1, 600):
            yield scrapy.Request(url=self.url.format(product_number), callback=self.parse)

    def parse(self, response):
        # Extract items from the current page

        rows = response.xpath('//table[@class="table table-bordered table-condensed"]/tbody/tr')
        item = AgriscrapperItem()
        # Loop through each row in the table from the response
        for row in rows:
            # Extract data from each cell in the row
            item['commodity'] = row.xpath('td[1]/text()').get()
            item['classification'] = row.xpath('td[2]/text()').get()
            item['grade'] = row.xpath('td[3]/text()').get()
            item['sex'] = row.xpath('td[4]/text()').get()
            item['market'] = row.xpath('td[5]/text()').get()
            item['wholesale'] = row.xpath('td[6]/text()').get()
            item['retail'] = row.xpath('td[7]/text()').get()
            item['supply_volume'] = row.xpath('td[8]/text()').get()
            item['county'] = row.xpath('td[9]/text()').get()
            item['date'] = row.xpath('td[10]/text()').get()

            yield item


        # pagination = response.css('.pagination ::attr(href)').getall()
        # # log items in pagination
        # logging.info(pagination)
        # if pagination:
        #     for url in pagination:
        #         # check if its a valid url
        #         if is_valid_url(url):
        #             yield response.follow(url, callback=self.parse)
                