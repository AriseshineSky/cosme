from cosme.pipelines import TranslationPipeline
from cosme.spiders.product import ProductSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.test import get_crawler

from cosme.product_manager.loader import CosmeElasticSearchLoder
from cosme.settings import (
    ELASTICSEARCH_SERVERS,
    ELASTICSEARCH_USERNAME,
    ELASTICSEARCH_PASSWORD,
)


def main():
    settings = get_project_settings()
    crawler = get_crawler(ProductSpider)
    translation_pipeline = TranslationPipeline(settings)
    spider = crawler._create_spider()
    translation_pipeline.open_spider(spider)

    filterd_settings = {
        "ELASTICSEARCH_SERVERS": ELASTICSEARCH_SERVERS,
        "ELASTICSEARCH_USERNAME": ELASTICSEARCH_USERNAME,
        "ELASTICSEARCH_PASSWORD": ELASTICSEARCH_PASSWORD,
    }

    loader = CosmeElasticSearchLoder(filterd_settings, "product_id")

    for doc in loader.load_content(type="product", query=None):
        if "title_en" not in doc or not doc["title_en"] or "title" not in doc or not doc["title"]:
            continue

        translation = {
            "id": str(doc["_id"]),
            "title": doc["title"],
            "title_en": doc["title_en"],
        }

        translation_pipeline.process_item(translation, spider)
    translation_pipeline.close_spider(spider)


if __name__ == "__main__":
    main()
