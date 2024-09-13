from resources.product_manager.loader import ElasticSearchLoder


class CosmeElasticSearchLoder(ElasticSearchLoder):
    ELASTICSEARCH_BUFFER_LENGTH = 1
    ELASTICSEARCH_INDEX = "cosme_products"
    PRODUCT_INDEX = "cosme_products"
