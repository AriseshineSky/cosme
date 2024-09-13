from datetime import datetime
import scrapy
from cosme.items import ProductUrlItem

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from resources.base_spider import BaseSpider


class ProductUrlSpider(BaseSpider):
    name = "product-url"
    allowed_domains = ["cosme.com"]
    start_urls = []

    custom_settings = {
        "ITEM_PIPELINES": {
            "cosme.pipelines.ProductUrlPipeline": 400,
        }
    }

    def __init__(self, *args, **kwargs):
        super(ProductUrlSpider, self).__init__(*args, **kwargs)

        self.cookies = {
            "PHPSESSID": "fhhf2q1g45dmm7jlt75pua8p35",
            "@COSME_VISITOR": "VISITOR_ID=59d16095fc626471c6d07efd0ca5eb327aee27da",
            "krt.vis": "jb9AOAAl3SujUGq",
            "_gid": "GA1.2.2101935291.1720723281",
            "TMPPPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "PPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "cto_bundle": "iLZnu19CMnJjcVVFMVhBeGtWTkdJY21qOFkyOHlDaHZjaUhpRm1XblRPRUlab3AlMkZUZEpzNTNLVW5pZSUyQk9OalFjNDZvQTd1clJ1OWNzQjdjN1ZtOEVoc1JYWHdTNU8xSnlZZW5nMG5WSGxudnpXZFpJYjZlSVhsd3RDSEJlVEpPNHBBUlhPbTJhSE9aYjJwQ05Ea3YlMkZLJTJGWDRNTXdGVmJoOFk2OEt0STBvJTJCJTJGMkVYUUJaeTIlMkJqMWRYNlNBSjlJbFdmZDUwbXklMkYzU3lxdzdzVXpwemtGMWVZTEFWYnFwRVRzQ3VuMHdYblRYbmVkNXdKb0I5S2g3NXlLYVl4R2VJMkNzbE9mNA",
            "_ga_HEKY12CWNG": "GS1.1.1720723281.1.1.1720724808.60.0.0",
            "_gat": "1",
            "_ga": "GA1.2.1385196681.1720723281",
            "_gat_commonTracker": "1",
            "GA_LINKER_PARAM": "_ga%3D2.74040657.2101935291.1720723281-1385196681.1720723281",
        }

    def start_requests(self):
        for url in ProductUrlSpider.start_urls:
            yield scrapy.Request(
                url=url,
                method="GET",
                headers=self.get_headers(),
                cookies=self.cookies,
                callback=self.parse_product_urls,
            )

    def get_request_params(self, category_id, page, per_page):
        return {
            "os": "pc",
            "apiVersion": "1.2",
            "version": "",
            "abType": "",
            "domain": "listingsearch-api.cosme.com",
            "path": "/v1.2/deal/list",
            "categoryId": category_id,
            "sort": "favorite",
            "isFreeShip": "N",
            "isTodayRelease": "",
            "isWonderShip": "",
            "isSpecialPrice": "",
            "page": page,
            "perPage": per_page,
            "showAdCategoryPick": "true",
            "q": "",
            "api_version": "",
            "per_page": "",
            "is_free_ship": "",
            "code": "",
            "uri": "",
            "total_count": "",
            "total_page": "",
            "message": "",
            "process_time": "",
        }

    def get_headers(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "http://35.192.187.156/",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }
        return headers

    def get_params(self, category_id, page):
        params = {
            "os": "pc",
            "apiVersion": "1.2",
            "version": "",
            "abType": "",
            "domain": "listingsearch-api.cosme.com",
            "path": "/v1.2/deal/list",
            "categoryId": category_id,
            "sort": "favorite",
            "isFreeShip": "N",
            "isTodayRelease": "",
            "isWonderShip": "",
            "isSpecialPrice": "",
            "page": page,
            "perPage": "99",
            "showAdCategoryPick": "true",
            "q": "",
            "api_version": "",
            "per_page": "",
            "is_free_ship": "",
            "code": "",
            "uri": "",
            "total_count": "",
            "total_page": "",
            "message": "",
            "process_time": "",
        }
        return params

    def crawl_product_urls(self, url, category_id, page):
        return scrapy.Request(
            url=new_url,
            method="GET",
            headers=self.get_headers(),
            cookies=self.cookies,
            callback=self.parse_product_urls_from_json,
        )

    def errback(self, failure):
        self.logger.error(repr(failure))

    def get_product_id(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        return query.get("product_id", [None]).pop()

    def get_next_page_number(self, response):
        response.xpath("//li[@class='pager__next']/a/@data-pageno").get()

    def get_next_page_url(self, url, new_pageno):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params["pageno"] = [str(new_pageno)]

        new_query_string = urlencode(query_params, doseq=True)

        new_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query_string,
                parsed_url.fragment,
            )
        )

        return new_url

    def parse_product_urls(self, response):
        self.update_cookies(response)
        urls = response.xpath("//div[contains(@class, 'product product--thumb')]/a/@href").getall()
        for url in urls:
            item = ProductUrlItem()
            item["id"] = self.get_product_id(url)
            item["url"] = response.urljoin(url)
            item["created_at"] = datetime.now().replace(microsecond=0).isoformat()
            yield item

        next_page_num = self.get_next_page_number(response)
        if next_page_num:
            next_page_url = self.get_next_page_url(response.url, next_page_num)

            yield scrapy.Request(
                url=next_page_url,
                method="GET",
                headers=self.get_headers(),
                cookies=self.cookies,
                callback=self.parse_product_urls,
            )
