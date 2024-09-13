from datetime import datetime
import scrapy
from cosme.items import CategoryUrlItem

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from resources.base_spider import BaseSpider


class CategorySpider(BaseSpider):
    name = "category-url"
    allowed_domains = ["cosme.com"]
    start_urls = ["https://www.cosme.com"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "cosme.pipelines.CategoryPipeline": 400,
        }
    }

    def get_cookies(self):
        self.cookies = {
            "PHPSESSID": "fhhf2q1g45dmm7jlt75pua8p35",
            "@COSME_VISITOR": "VISITOR_ID=59d16095fc626471c6d07efd0ca5eb327aee27da",
            "krt.vis": "jb9AOAAl3SujUGq",
            "_gid": "GA1.2.2101935291.1720723281",
            "TMPPPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "PPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "GA_LINKER_PARAM": "_ga%3D2.241437889.2101935291.1720723281-1385196681.1720723281",
            "_ga_HEKY12CWNG": "GS1.1.1720723281.1.1.1720723335.6.0.0",
            "_ga": "GA1.1.1385196681.1720723281",
            "cto_bundle": "WhOOJ19CMnJjcVVFMVhBeGtWTkdJY21qOFk3Z2hjY3d6YzhzYldaejZUJTJGbVdPWVpvS0olMkJySkhhYVVsJTJGajhoNGlUdlNvV2owZUFURmxBVUlUWkhXZlBZWXlIazlVMkhJeFVWUUpVcG43M2l2UUxHS1pFb0hYZDMwSTJpZ2s3R0lEeGpEb0Mwam8xS296Z3clMkZQWjhnOGRZQXhFZWIxRmlMdHgwaTE5R1NxTFRHUW80N1lzWjZYZzBVV0xhY0M0QmslMkZ5NktQbmc4TzJFbWVxcVU0eGtUcTR6V01KaHFKcG02cSUyRjFKWXdNZ25XaFRBQmptc05UeFBuV29rQ1lOTCUyRjBDMEpOOEI",
        }
        return self.cookies

    def get_headers(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        }

        return headers

    def start_requests(self):
        for url in CategorySpider.start_urls:
            yield scrapy.Request(
                url,
                method="GET",
                headers=self.get_headers(),
                cookies=self.get_cookies(),
                errback=self.errback,
                callback=self.parse_category_urls,
            )

    def errback(self, failure):
        self.logger.error(repr(failure))

    def get_cat_name(self, cat):
        return cat.xpath("./a/span//text()").extract_first()

    def get_cat_url(self, cat):
        return cat.xpath("./a/@href").extract_first()

    def get_cat_id(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        return query.get("category_id", [None]).pop()

    def parse_category_urls(self, response):
        self.update_cookies(response)
        cat_urls = response.xpath(
            '//ul[@class="header-nav-item__large-menu-list"]/li/a/@href'
        ).getall()
        for url in cat_urls:
            item = CategoryUrlItem()
            item["id"] = self.get_cat_id(url)
            item["url"] = response.urljoin(url)
            item["created_at"] = datetime.now().replace(microsecond=0).isoformat()
            yield item
