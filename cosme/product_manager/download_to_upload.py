from datetime import datetime
import json
from multiprocessing.pool import ThreadPool
import re

from peewee import *

from em_product.product import StandardProduct
from pymongo import MongoClient


from cosme.settings import MONGO_URI
from utils.price_calculator import PriceCalculator
from utils.site_product import fetch_source_ids
from .formatter import to_upload
from .loader import CosmeElasticSearchLoder
from scrapy.utils.project import get_project_settings



def main():
    price_rules = {"roi": 0.3, "ad_cost": 5, "transfer_cost": 15}
    price_calculator = PriceCalculator(price_rules)
    loader = CosmeElasticSearchLoder(get_project_settings())
    product_ids = fetch_source_ids(["cosme"])
    count_total = 0
    count_exists = 0
    with open("cosme_0723.txt", "w+") as file:
        for doc in loader.load_content("product"):
            count_total += 1

            try:
                doc["sku"] = doc["product_id"]
                standard_product = StandardProduct(**doc)
                upload_product = to_upload(standard_product.model_dump(), price_calculator, "X13")
                upload_product["shipping_days_min"] = None
                upload_product["shipping_days_max"] = None
                json.dump(upload_product, file, ensure_ascii=False)
                file.write("\n")
            except Exception as e:
                pass

    print(count_total)


if __name__ == "__main__":
    main()
