import unittest

from scrapy.utils.test import get_crawler
from scrapy.http import HtmlResponse

from cosme.spiders.product import ProductSpider


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.crawler = get_crawler(ProductSpider)
        self.spider = self.crawler._create_spider()

    def test_available_product_1(self):
        url = "https://www.cosme.com/products/detail.php?product_id=338794"
        body = None
        with open(
            "338794.html",
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
            "url": "https://www.cosme.com/products/detail.php?product_id=338794",
            "product_id": "338794",
            "existence": True,
            "title": "色鮮やかなリキッドアイカラー。ひときわ輝くスパークルEYE。",
            "sku": "4969527504636",
            "upc": "4969527504636",
            "brand": "アナ スイ / ANNA SUI",
            "specifications": [
                {
                    "name": "タイプ",
                    "value": "本体"
                },
                {
                    "name": "カラー",
                    "value": "600"
                },
                {
                    "name": "サイズ",
                    "value": "2.5g"
                }
            ],
            "categories": "メイクアップ > アイシャドウ > リキッドアイシャドウ",
            "images": "https://www.cosme.com/upload/save_image/product/00/33/87/93/338793_1_800.jpg;https://www.cosme.com/upload/save_image/product/00/33/87/93/338793_2_800.jpg;https://www.cosme.com/upload/save_image/product/00/33/87/93/338793_3_800.jpg",
            "price": 17.93,
            "available_qty": None,
            "reviews": 9,
            "rating": 4.00,
            "shipping_fee": 2.08,
            "weight": 0.01
        }
        for key in target_product:
            self.assertEqual(product[key], target_product[key])

    def test_available_product_2(self):
        url = "https://www.cosme.com/products/detail.php?product_id=341692"
        body = None
        with open(
            "341692.html",
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
            "url": "https://www.cosme.com/products/detail.php?product_id=341692",
            "product_id": "341692",
            "existence": True,
            "title": "アイ & フェイスカラー パレット / 本体 / 01 / 6g",
            "sku": "4969527505411",
            "upc": "4969527505411",
            "brand": "アナ スイ / ANNA SUI",
            "specifications": [
                {
                    "name": "タイプ",
                    "value": "本体"
                },
                {
                    "name": "カラー",
                    "value": "01"
                },
                {
                    "name": "サイズ",
                    "value": "6g"
                }
            ],
            "categories": "メイクアップ > アイシャドウ > パウダーアイシャドウ",
            "images": "https://www.cosme.com/upload/save_image/product/00/34/16/91/341691_1_800.jpg;https://www.cosme.com/upload/save_image/product/00/34/16/91/341691_2_800.jpg;https://www.cosme.com/upload/save_image/product/00/34/16/91/341691_3_800.jpg;https://www.cosme.com/upload/save_image/product/00/34/16/91/341691_4_800.jpg",
            "price": 25.82,
            "available_qty": None,
            "reviews": 4,
            "rating": 3.07,
            "shipping_fee": 0.00,
            "weight": 0.01
        }
        for key in target_product:
            self.assertEqual(product[key], target_product[key])

    def test_available_product_3(self):
        url = "https://www.cosme.com/products/detail.php?product_id=303287"
        body = None
        with open(
            "303287.html",
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
            "url": "https://www.cosme.com/products/detail.php?product_id=303287",
            "product_id": "303287",
            "existence": True,
            "title": "アルティム8∞ スブリム ビューティ クレンジング オイルn / 本体 / 150mL",
            "sku": "4936968814372",
            "upc": "4936968814372",
            "brand": "シュウ ウエムラ / shu uemura",
            "specifications": [
                {
                    "name": "タイプ",
                    "value": "本体"
                },
                {
                    "name": "サイズ",
                    "value": "150mL"
                }
            ],
            "categories": "スキンケア・基礎化粧品 > クレンジング > クレンジングオイル",
            "images": "https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_1_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_2_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_3_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_4_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_5_800.jpg",
            "price": 37.30,
            "available_qty": None,
            "reviews": 3460,
            "rating": 4.29,
            "shipping_fee": 0.00,
            "weight": 0.33
        }
        for key in target_product:
            self.assertEqual(product[key], target_product[key])

    def test_unavailable_product(self):
        url = "https://www.cosme.com/products/detail.php?product_id=347482"
        body = None
        with open(
            "347482.html",
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
            "url": "https://www.cosme.com/products/detail.php?product_id=347482",
            "product_id": "347482",
            "existence": False,
            "title": "夏のベタつく肌に。限定ミントセージの香りで爽快クレンジング",
            "sku": "4936968814372",
            "upc": "4936968814372",
            "brand": "チャントアチャーム / chant a charm",
            "specifications": [
                {
                    "name": "タイプ",
                    "value": "本体"
                },
                {
                    "name": "サイズ",
                    "value": "150mL"
                }
            ],
            "categories": "スキンケア・基礎化粧品 > クレンジング > クレンジングオイル",
            "images": "https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_1_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_2_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_3_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_4_800.jpg;https://www.cosme.com/upload/save_image/product/00/30/32/86/303286_5_800.jpg",
            "price": 20.09,
            "available_qty": 0,
            "reviews": 4,
            "rating": 4.14,
            "shipping_fee": 2.08,
            "weight": 0.29
        }
        for key in target_product:
            self.assertEqual(product[key], target_product[key])


if __name__ == "__main__":
    unittest.main()
