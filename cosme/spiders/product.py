from datetime import datetime
import re

import scrapy
import scrapy.selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup


class ProductSpider(scrapy.Spider):
    name = "product"
    allowed_domains = ["www.cosme.com"]
    start_urls = []

    # custom_settings = {
    #     "ITEM_PIPELINES": {
    #         "cosme.pipelines.ProductPipeline": 400,
    #     }
    # }

    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "de-DE,de;q=0.9,en-GB;q=0.8,en;q=0.7",
        "dnt": "1",
        "priority": "u=0, i",
        "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jpy_rate = 153.346419

    def get_prod_id(self, url: str):
        pid_match = re.findall(r'product_id=(\d+)', url)
        if pid_match:
            return pid_match[0]

    def remove_a_tag(self, text):
        soup = BeautifulSoup(text, "html.parser")
        while True:
            if not soup.a:
                break
            soup.a.decompose()

        text = soup
        return text

    def remove_a_tag_replace_content(self, text):
        will_remove_tags = ["a"]
        soup = BeautifulSoup(text, "html.parser")
        for tag in will_remove_tags:
            for match in soup.findAll(tag):
                if "詳し" in match.text.strip():
                    match.string.replace_with("")
                match.replaceWithChildren()
        return soup.text

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(url, headers=self.HEADERS,
                                 meta={ "cookiejar": i },
                                 callback=self.parse)

    def get_exist(self, response: HtmlResponse):
        stockout_sel = response.css('.stockout__copy')
        return not stockout_sel

    def get_title(self, response: HtmlResponse):
        return response.xpath("//p[@class='product__lead']/text()").get()

    def get_price(self, response: HtmlResponse):
        jpy_price = response.xpath("//span[@itemprop='price']/@content").get()
        return round(jpy_price*self.jpy_rate, 2)

    def get_shipping_fee(self, response: HtmlResponse):
        condition_list = response.xpath("//ul[@class='product-condition-list']/li/text()").getall()

        if "送料無料" in condition_list:
            shipping_fee = 0.00
        else:
            shipping_fee = round(319*self.jpy_rate, 2)

        return shipping_fee

    def get_images(self, response: HtmlResponse):
        str_images = ""
        conv_list_images = []

        list_images = response.xpath("//ul[@class='product__thumb-list']//img/@src").getall()
        for x in list_images:
            if "?" in x:
                x = x.split("?")[0]
            if "https" not in x:
                x = 'https://www.cosme.com'+x
            x = x.replace('_360.', '_800.')
            conv_list_images.append(x)

        if len(conv_list_images) > 0:
            str_images = ";".join(conv_list_images)

        return str_images

    def get_sku(self, response: HtmlResponse):
        return response.xpath("//meta[@itemprop='sku']/@content").get()

    def get_description(self, selector: HtmlResponse):
        desc = None
        desc = selector.xpath("//div[@itemprop='description']").get()
        desc = self.remove_a_tag_replace_content(desc)

        return desc

    def get_specifications_etc(self, response: HtmlResponse):
        specs = []
        brand = None
        cats = None
        weight = None

        thx = response.css('dl.product-desc > dt::text').getall()
        tdx = response.css('dl.product-desc > dd')

        for th, td in zip(thx, tdx):
            if th and ('コスメ' not in th) and (th != 'JANコード'):
                if th == 'ブランド名':
                    brand_txt = td.css('a::text').get()
                    if brand_txt:
                        brand = brand_txt
                elif th == 'アイテムカテゴリ':
                    cats_txts = td.css(':scope a::text').getall()
                    if cats_txts:
                        cats = " > ".join(cats_txts)
                elif td.css('::text').get():
                    specs.append({
                        "name": th,
                        "value": td,
                    })
                    if th == 'サイズ':
                        weight = self.get_weight(td.css('::text').get().lower())

        return (specs if specs else None), brand, cats, weight

    def get_weight(self, txt: str):
        weight_match = re.findall(r'(\d+(?:\.\d+)?)\s*(g|ml|kg|l)', txt)
        if weight_match:
            if weight_match[1] in {'g', 'ml'}:
                return round(float(weight_match[0])/453.59237, 2)
            elif weight_match[1] in {'kg', 'l'}:
                return round(float(weight_match[0])*2.20462, 2)

    def get_reviews(self, response: HtmlResponse):
        src_reviews = response.css('div.unique-product-rate-count::text').get()
        if not src_reviews:
            return
        rev_match = re.findall(r'(\d+)', src_reviews)
        if rev_match:
            return int(rev_match[0])

    def get_rating(self, response: HtmlResponse):
        src_rating = response.xpath("//span[@class='unique-product-rating-point']/text()").get()
        if not src_rating:
            return

        f_src_rating = float(src_rating)
        if f_src_rating <= 1.0:
            return 1.00

        conv_rating = f_src_rating * 5.0 / 7.0
        return round(conv_rating, 2)

    def parse(self, response: HtmlResponse):
        existence = self.get_exist(response)
        specifications, brand, categories, weight = self.get_specifications_etc(response)

        images = self.get_images(response)
        if not images:
            print("Skip no images")
            return

        item = {
            "date": datetime().strftime('%Y-%m-%dT%H:%M:%S'),
            "url": response.url,
            "source": "cosme",
            "product_id": self.get_prod_id(response.url),
            "existence": existence,
            "title": self.get_title(response),
            "title_en": None,
            "description": self.get_description(response),
            "description_en": None,
            "summary": None,
            "sku": self.get_sku(response),
            "upc": self.get_sku(response),
            "brand": brand,
            "specifications": specifications,
            "categories": categories,
            "images": self.get_images(response),
            "videos": None,
            "price": self.get_price(response),
            "available_qty": 0 if not existence else None,
            "options": None,
            "variants": None,
            "has_only_default_variant": True,
            "returnable": False,
            "reviews": self.get_reviews(response),
            "rating": self.get_rating(response),
            "sold_count": None,
            "shipping_fee": self.get_shipping_fee(response),
            "shipping_days_min": 1, # https://www.cosme.com/help/help_04_2.html#yu_packet
            "shipping_days_max": 2,
            "weight": weight,
            "length": None,
            "width": None,
            "height": None
        }

        yield item
