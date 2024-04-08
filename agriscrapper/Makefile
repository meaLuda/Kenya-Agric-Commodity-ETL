run_scrapper:
	scrapy crawl kemis_commodities_scrapper

build_image:
	docker build -t agriscrapper .

run_image:
	docker run -p 4000:4000 agriscrapper