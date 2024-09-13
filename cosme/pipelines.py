# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


from em_product.resources.pipelines import (
    ESCategoryPipeline,
    ESProductUrlPipeline,
    ESProductPipeline,
    ESProductRecrawlPipeline,
    ESTranslationPipeline,
    ESSeedProductPipeline,
)


class CategoryPipeline(ESCategoryPipeline):
    CATEGORY_INDEX = "cosme_categories"
    ELASTICSEARCH_INDEX = "cosme_categories"


class ProductUrlPipeline(ESProductUrlPipeline):
    CATEGORY_INDEX = "cosme_categories"
    ELASTICSEARCH_INDEX = "cosme_product_urls"


class ProductPipeline(ESProductPipeline):
    PRODUCT_URL_INDEX = "cosme_product_urls"
    PRODUCT_INDEX = "cosme_products"
    ELASTICSEARCH_INDEX = "cosme_products"


class TranslationPipeline(ESTranslationPipeline):
    TRANSLATION_INDEX = "cosme_translation"
    ELASTICSEARCH_INDEX = TRANSLATION_INDEX
