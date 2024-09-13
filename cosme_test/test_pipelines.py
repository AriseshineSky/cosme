from datetime import datetime
import json
import unittest
from well.pipelines import ProductPipeline, ProductUrlPipeline, CategoryPipeline
from well.items import ProductUrlItem, CategoryUrlItem

from well.spiders.product import ProductSpider
from well.spiders.category import CategorySpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.test import get_crawler
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


class TestPipelines(unittest.TestCase):
    def setUp(self):
        settings = get_project_settings()
        crawler = get_crawler(CategorySpider)
        self.product_pipeline = ProductPipeline(settings)
        self.product_url_pipeline = ProductUrlPipeline(settings)
        self.category_pipeline = CategoryPipeline(settings)
        self.spider = crawler._create_spider()

    def tearDown(self):
        self.category_pipeline.close_spider(self.spider)
        self.product_pipeline.close_spider(self.spider)

    # def test_product_pipeline(self):
    #     path = "well_test/pages/products.json"
    #     with open(path, "r", encoding="utf-8") as file:
    #         products = json.load(file)
    #         for product in products:
    #             self.product_pipeline.process_item(product, self.spider)

    def get_cat_id_from_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.path

    def category_filter(self, category):
        keywords = ["electric", "sexual", "shirt"]
        for keyword in keywords:
            if keyword in category.lower():
                return True

    def get_product_id_from_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.path.split(".").pop(0).split("_")[-1]

    # def test_category_url_pipeline(self):
    #     path = "well_test/pages/categories.xml"
    #     with open(path, "r", encoding="utf-8") as file:
    #         tree = ET.parse(file)
    #         root = tree.getroot()
    #
    #         namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    #         loc_elements = root.findall(".//ns:loc", namespace)
    #         loc_values = [loc.text for loc in loc_elements]
    #
    #         # 打印 loc 元素的内容
    #         for loc in loc_values:
    #             if self.category_filter(loc):
    #                 continue
    #             url_item = CategoryUrlItem()
    #             url_item["id"] = self.get_cat_id_from_url(loc)
    #             url_item["url"] = loc
    #             url_item["date"] = datetime.now().replace(microsecond=0).isoformat()
    #             self.category_pipeline.process_item(url_item, self.spider)

    def test_product_url_pipeline(self):
        pathes = [
            "well_test/pages/products.xml",
        ]
        for path in pathes:
            with open(path, "r", encoding="utf-8") as file:
                tree = ET.parse(file)
                root = tree.getroot()

                namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                loc_elements = root.findall(".//ns:loc", namespace)
                loc_values = [loc.text for loc in loc_elements]

                # 打印 loc 元素的内容
                for loc in loc_values:
                    url_item = ProductUrlItem()
                    url_item["id"] = self.get_product_id_from_url(loc)
                    url_item["url"] = loc
                    url_item["date"] = datetime.now().replace(microsecond=0).isoformat()
                    self.product_url_pipeline.process_item(url_item, self.spider)

    # def test_product_url_pipeline_2(self):
    #     path = "well_test/product_urls.txt"
    #     with open(path, "r", encoding="utf-8") as file:
    #         for line in file:
    #             url_item = ProductUrlItem()
    #             url_item["id"] = self.get_product_id_from_url(line)
    #             url_item["url"] = line
    #             url_item["date"] = datetime.now().replace(microsecond=0).isoformat()
    #             self.product_url_pipeline.process_item(url_item, self.spider)


if __name__ == "__main__":
    unittest.main()
