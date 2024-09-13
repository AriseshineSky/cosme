from em_product.resources.product_manager.loader import ElasticSearchLoder


class CosmeElasticSearchLoder(ElasticSearchLoder):
    ELASTICSEARCH_INDEX = "cosme_products"
    PRODUCT_INDEX = "cosme_products"


class TranslationElasticSearchLoder(ElasticSearchLoder):
    TRANSLATION_INDEX = "cosme_translation"
    ELASTICSEARCH_INDEX = "cosme_translation"
