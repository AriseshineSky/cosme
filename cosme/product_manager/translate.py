from datetime import datetime
import os
import logging
import json
from multiprocessing.pool import ThreadPool

from em_product.product import ProductSource
from google.oauth2 import service_account
from google.cloud.translate_v2 import Client

from utils.site_product import fetch_source_ids
from cosme.product_manager.loader import CosmeElasticSearchLoder
from scrapy.utils.project import get_project_settings
from utils.translate_service import get_translator
from multiprocessing.pool import ThreadPool

# 设置日志格式
FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(file_handler)

    return logger


log_file_path = os.path.join(os.path.expanduser("~"), "logs", "translation.log")
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

logger = get_logger(__name__, log_file_path)


def translate_product_title(product, title_translator):
    if product.get("title_en"):
        return product.get("title_en")
    return title_translator(product.get("title"))


def update_product_translated_title(loader, product, title_translator):
    translated_title = translate_product_title(product, title_translator)
    logger.info(f"[SourceTitle] {product['title']} [Translated]: {translated_title}")
    loader.save_item({"_id": product["_id"], "title_en": translated_title}, action="update")


def main():
    pool = ThreadPool(10)
    service_account_path = "./gc.json"
    target_language = "en"
    translation_service = Client(
        target_language=target_language,
        credentials=service_account.Credentials.from_service_account_file(service_account_path),
    )
    product_ids = fetch_source_ids(["cosme"])

    title_translator = get_translator(translation_service, 30000, ["ja"], "title")
    loader = CosmeElasticSearchLoder(get_project_settings())

    count_total = 0
    for doc in loader.load_content("product"):
        count_total += 1
        try:
            pool.apply_async(update_product_translated_title, args=(loader, doc, title_translator))
            # update_product_translated_title(loader, doc, title_translator)
        except Exception as e:
            if "language or length does not match" in str(e):
                pass
            else:
                breakpoint()

        # pool.apply_async(update_product_translated_title, args=(loader, doc, title_translator))


    pool.close()
    pool.join()
    print(count_total)


if __name__ == "__main__":
    main()
