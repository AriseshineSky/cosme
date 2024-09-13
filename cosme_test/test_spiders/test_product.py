import json
import unittest
from scrapy.utils.test import get_crawler
from scrapy.http import Request, Response, HtmlResponse
from well.spiders.product import ProductSpider


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.crawler = get_crawler(ProductSpider)
        self.spider = self.crawler._create_spider()

    # check available product
    def test_available_product_1(self):
        url = "https://well.ca/products/the-scented-market-soy-wax-candle_309152.html"
        body = None
        with open(
            "well_test/pages/the-scented-market-soy-wax-candle_309152.html",
            "rb",
        ) as file:
            body = file.read()

        response = HtmlResponse(
            url=url,
            body=body,
            encoding="utf-8",
        )
        result = list(self.spider.parse(response))
        self.assertEqual(len(result), 1)
        product = result[0]
        target_product = {
            "sku": "Product1",
            "price": 19.97,
            "available_qty": None,
            "date": "2024-09-06T15:12:26",
            "url": "https://well.ca/products/the-scented-market-soy-wax-candle_309152.html",
            "source": "well_ca",
            "images": "https://dr9wvh6oz7mzp.cloudfront.net/i/6a51e8d5bf4e7a063836d9deb8b5bedf_ra.png",
            "product_id": "309152",
            "existence": True,
            "title": "The Scented Market Soy Wax Candle Hello Pumpkin",
            "title_en": None,
            "description": '<div itemprop="description" class="itempropWrap">\n    <div style="margin-bottom: 25px;"><p>HELLO PUMPKIN is the popular Pumpkin Spice scent with a new name! That smell of a freshly baked pumpkin pie coming out of the oven with a dash of cinnamon and nutmeg.\xa0</p><p>Before you light your candle, trim all wicks to 1/4 inch. Light all wicks and let the candle burn until there is an even layer of melted wax across the top. This sets a memory in your wax to always burn to the outer edges of the candle (as opposed to straight down the wick). When you\'re done burning the candle, always use a candle snuffer to extinguish the flame. You must re-trim the wick / remove the bud before each re-light.\xa0</p><p>Never leave your candle unattended. Burn within sight, away from flammable objects, children and pets. Burn on a heat-safe surface. Avoid drafts. For best results, burn until wax melts evenly across, do not exceed 4 hours. Keep the wax pool free of debris. Keep wick centered and trim each time the candle is lit. Stop the candle when half the wax remains. Do not move or touch while hot.</p></div>\n                        <p>\n            <strong>Highlights</strong>\n            <br>\n                                            <img src="//d2i6p126yvrgeu.cloudfront.net/images/product_flags/icon-canadian.svg" data-toggle="tooltip" data-placement="top" alt="Canadian product" class="img-highlight" title="Canadian" data-original-title="Canadian">\n                    </p>\n    </div><div itemprop="features" class="itempropWrap itempropWrap--nopadding">\n    <ul><li>Renewable and sustainable</li><li>Phthalate-free</li><li>Dye Free/li&gt;</li><li>Soot Free</li><li>Gluten-Free</li><li>Vegan Friendly</li></ul></div><div itemprop="features" class="itempropWrap">\n        <div>\n            <p>100% Soy Wax &amp; Premium Oil Fragrance (Phthalate &amp; Paraben Free).</p>        </div>\n            </div>',
            "description_en": None,
            "summary": None,
            "upc": None,
            "brand": "The Scented Market",
            "specifications": None,
            "categories": "Home & Lifestyle>Home Decor>Candles & Home Fragrance",
            "videos": None,
            "options": None,
            "variants": None,
            "returnable": None,
            "reviews": None,
            "rating": None,
            "sold_count": None,
            "shipping_fee": 1.0,
            "shipping_days_min": None,
            "shipping_days_max": None,
            "weight": None,
            "width": None,
            "height": None,
            "length": None,
            "has_only_default_variant": True,
            "currency": "USD",
            "price_retail": None,
        }
        for key in target_product:
            if key in ["date", "description"]:
                continue
            self.assertEqual(product[key], target_product[key])

    # check available product
    def test_options(self):
        url = "https://well.ca/products/pure-anada-lavish-natural-lipstick_186608.html"
        body = None
        with open(
            "well_test/pages/pure-anada-lavish-natural-lipstick_186608.html",
            "rb",
        ) as file:
            body = file.read()

        response = HtmlResponse(
            url=url,
            body=body,
            encoding="utf-8",
        )
        result = list(self.spider.parse(response))
        self.assertEqual(len(result), 1)
        product = result[0]
        target_product = {
            "sku": "Product1",
            "price": 10.06,
            "available_qty": None,
            "date": "2024-09-06T15:29:57",
            "url": "https://well.ca/products/pure-anada-lavish-natural-lipstick_186608.html",
            "source": "well_ca",
            "images": "https://dr9wvh6oz7mzp.cloudfront.net/i/c43b91e9c3ad4837aa21b064f16cdd68_ra.jpg",
            "product_id": "186608",
            "existence": True,
            "title": "Pure Anada Lavish Natural Lipstick",
            "title_en": None,
            "description": '<div itemprop="description" class="itempropWrap">\n    <div style="margin-bottom: 25px;"><div>All natural, creamy pigments will lavish your lips with colour. No silicone, dyes or artificial flavours, simply fabulous moisture and colour from nature!</div><div><br></div>The Lavish Natural Lipstick line is made with organic ingredients and is cruelty-free. However, this line is not vegan in that the formulation contains both beeswax and carmine. <br><br><b>Features:</b><br><ul><li>Certified Organic Ingredients </li><li>Cruelty Free </li><li>No Silicone </li><li>No Petroleum Dyes </li><li>No Artificial Flavour </li></ul><br><b>Directions: </b>Apply directly to lips.Take care not to store it in direct heat. During application, twist up the bullet so just the tip is exposed to prevent unnecessary strain.<br><br><b>Ingredients:</b> Ricinus Communis (Castor) Seed Oil, Butyrospermum Parkii (Shea) Butter, Simmondsia Chinensis (Jojoba) Seed Oil, Limnanthes Alba (Meadowfoam) Seed Oil, Euphorbia Cerifera (Candelilla) Wax, Prunus Avium (Cherry) Kernel Oil, Rosa Canina (Rosehip) Oil, Cera Flava (Beeswax), Copernicia Cerifera (Carnauba) Wax, Oryza Sativa (Rice Bran) Wax, Tocopherol (Vitamin E), Aroma (Flavour), May Contain: CI 77891 (Titanium Dioxide), CI 75470 (Carmine), CI 77491 (Red Iron Oxide), CI 77742 (Manganese Violet), CI 77499 (Black Iron Oxide)\xa0\xa0 \xa0\xa0\xa0\xa0 <br></div>\n                        <p>\n            <strong>Highlights</strong>\n            <br>\n                                            <img src="//d2i6p126yvrgeu.cloudfront.net/images/product_flags/icon-natural.svg" data-toggle="tooltip" data-placement="top" alt="Natural product" class="img-highlight" title="Natural" data-original-title="Natural">\n                                            <img src="//d2i6p126yvrgeu.cloudfront.net/images/product_flags/icon-organic.svg" data-toggle="tooltip" data-placement="top" alt="Organic product" class="img-highlight" title="Organic" data-original-title="Organic">\n <img src="//d2i6p126yvrgeu.cloudfront.net/images/product_flags/icon-non-gmo.svg" data-toggle="tooltip" data-placement="top" alt="Non-GMO product" class="img-highlight" title="Non-GMO" data-original-title="Non-GMO">\n                                            <img src="//d2i6p126yvrgeu.cloudfront.net/images/product_flags/icon-canadian.svg" data-toggle="tooltip" data-placement="top" alt="Canadian product" class="img-highlight" title="Canadian" data-original-title="Canadian">\n                    </p>\n    </div><div itemprop="features" class="itempropWrap itempropWrap--nopadding">\n    <ul><li>Certified Organic Ingredients </li><li>Cruelty Free </li><li>No Silicone </li><li>No Petroleum Dyes </li><li>No Artificial Flavour </li></ul></div><div itemprop="features" class="itempropWrap">\n        <div>\n            Ricinus Communis (Castor) Seed Oil, Butyrospermum Parkii (Shea) Butter, Simmondsia Chinensis (Jojoba) Seed Oil, Limnanthes Alba (Meadowfoam) Seed Oil, Euphorbia Cerifera (Candelilla) Wax, Prunus Avium (Cherry) Kernel Oil, Rosa Canina (Rosehip) Oil, Cera Flava (Beeswax), Copernicia Cerifera (Carnauba) Wax, Oryza Sativa (Rice Bran) Wax, Tocopherol (Vitamin E), Aroma (Flavour), May Contain: CI 77891 (Titanium Dioxide), CI 75470 (Carmine), CI 77491 (Red Iron Oxide), CI 77742 (Manganese Violet), CI 77499 (Black Iron Oxide)\t\t        </div>\n            </div>',
            "description_en": None,
            "summary": None,
            "upc": None,
            "brand": "Pure Anada",
            "specifications": None,
            "categories": "Beauty & Skin Care>Makeup>Lipsticks & Lip Balm>Lipsticks",
            "videos": None,
            "options": None,
            "variants": None,
            "returnable": None,
            "reviews": None,
            "rating": None,
            "sold_count": None,
            "shipping_fee": 1.0,
            "shipping_days_min": None,
            "shipping_days_max": None,
            "weight": None,
            "width": None,
            "height": None,
            "length": None,
            "has_only_default_variant": True,
            "currency": "USD",
            "price_retail": None,
        }
        for key in target_product:
            if key in ["date", "description"]:
                continue
            self.assertEqual(product[key], target_product[key])


if __name__ == "__main__":
    unittest.main()
