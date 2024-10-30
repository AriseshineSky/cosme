from datetime import datetime
import re

import scrapy
import scrapy.selector
from bs4 import BeautifulSoup

# from resources.base_spider import BaseSpider


class ProductSpider(BaseSpider):
    name = "product"
    allowed_domains = ["cosme.com"]
    start_urls = []

    custom_settings = {
        "ITEM_PIPELINES": {
            "cosme.pipelines.ProductPipeline": 400,
        }
    }

    def get_headers(self):
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Linux"',
        }

        return headers

    def __init__(self, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.cookies = {
            "PHPSESSID": "fhhf2q1g45dmm7jlt75pua8p35",
            "@COSME_VISITOR": "VISITOR_ID=59d16095fc626471c6d07efd0ca5eb327aee27da",
            "krt.vis": "jb9AOAAl3SujUGq",
            "TMPPPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "PPTK": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ3bHQiOiJhZjZjMzQzMjQ0NjE2ZjBhZDhjNGNlOGMzYWE4MjY1ZSIsImNvcnMiOjEsIm5iZiI6MTcyMDcyMzI4MiwiZXhwIjoxNzUyMjU5MjgyfQ._UNgBKTyH9otOclxScACP2A5AKW23riiEYrm0D6xTXU",
            "__sna_s1d": "kXDqtp2TPGg3zQxwR2DzvGFfgNYKLh",
            "_gid": "GA1.2.208641811.1721140007",
            "product_history": "%5B%22331482%22%2C%22331910%22%2C%22323866%22%2C%22323864%22%5D",
            "_gat": "1",
            "_gat_commonTracker": "1",
            "GA_LINKER_PARAM": "_ga%3D2.130410764.208641811.1721140007-1385196681.1720723281",
            "_ga_HEKY12CWNG": "GS1.1.1721156002.6.0.1721156002.60.0.0",
            "_ga": "GA1.1.1385196681.1720723281",
            "cto_bundle": "n1QZW19CMnJjcVVFMVhBeGtWTkdJY21qOFklMkJtenNka0ZWYnVIZ3F5cFR6UmElMkIlMkJPWllQYzhPJTJCYVFCZXRSMzhZQXZyRlB3dmVHQ3pRdEpRODRLMnNzM0NzRWpVOTNHaWloYmYzdHdUZWZkR3laNzYxSUZ3TUNVJTJGdEZDODBUQTF0UmtMbFcxd2EzayUyRnBTJTJCbEx6Q29JYzBzMXZBJTJCUjRGZnBaZVN1VHNZQW5jNnZrd0RMYmdrS0hMRnBDa3VDNXRXSnZuUXo4MTJlUDR6TGFPN1BDcHJDZ1diT293USUzRCUzRA",
        }

    def extract_pro_id_from_url(self, url):
        pro_id = url.split("?product_id=")[1]
        if "?" in pro_id:
            pro_id = pro_id.split("?")[0]
        return pro_id

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

    def write_html_response_for_debug(self, url, text):
        outHtmlFile = "output_product_detail_" + self.extract_pro_id_from_url(url) + ".html"
        outHtmlFile = outHtmlFile.replace("/", "_")
        outfileResponse = open("out_html/" + outHtmlFile, "w", encoding="utf-8")
        outfileResponse.write(text)
        outfileResponse.close()

    def start_requests(self):
        for url in ProductSpider.start_urls:
            yield scrapy.Request(
                url,
                method="GET",
                headers=self.get_headers(),
                cookies=self.cookies,
                callback=self.parse_product,
            )

    def get_usd_from_jyp(self, i_jyp):
        return int((float(i_jyp) * 0.0063) * 100) / 100.0

    def get_title(self, selector):
        return selector.xpath("//p[@class='product__lead']/text()").get()

    def get_price(self, selector):
        jyp_price = selector.xpath("//span[@itemprop='price']/@content").get()

        us_dollar_price = self.get_usd_from_jyp(jyp_price)
        return us_dollar_price

    def get_brand(self, selector):
        return selector.xpath("//p[@class='product__brand flt']//span/text()").get()

    def get_categories(self, selector):
        list_categories = selector.xpath(
            "//div[@class='breadcrumb-wrap']/ul[@class='breadcrumb']/li//span/text()"
        ).getall()
        if list_categories[0] == "TOP":
            list_categories.pop(0)

        str_categories = " > ".join(list_categories)
        return str_categories

    def extractDigitListFromStr(self, string):
        values = re.findall(r"[-+]?(?:\d*)", string)

        rets = []

        for x in values:
            if x.isdigit():
                rets.append(int(x))

        return rets

    def get_shipping_days(self, selector):
        list_ship_days = []

        product_condition = selector.xpath("//ul[@class='product-condition-list']").get()

        min_days = 0
        max_days = 0

        if product_condition:
            if "当日発送" in product_condition:
                min_days = 1
                max_days = 5
            else:
                min_days = 2
                max_days = 5
        else:
            status = selector.xpath(
                "//div[@class='wrap-product__stock']/p[@class='product__stock']"
            ).get()

            if "在庫あり" in status or "在庫残りわずか" in status:
                min_days = 2
                max_days = 5
            else:
                digits_list = self.extractDigitListFromStr(status)
                if len(digits_list) == 2:
                    min_days = digits_list[0]
                    max_days = digits_list[1]
                else:
                    min_days = 7
                    max_days = 10

        list_ship_days.extend([min_days, max_days])

        return list_ship_days

    def get_shipping_fee(self, selector):
        shipping_fee = 0
        condition_list = selector.xpath("//ul[@class='product-condition-list']/li/text()").getall()

        if "送料無料" in condition_list:
            shipping_fee = 0
        else:
            shipping_fee = self.get_usd_from_jyp(319)

        return shipping_fee

    def get_reviews(self, selector):
        i_num_review = None

        review_text = selector.xpath("//div[@class='unique-product-rate-count']/text()").get()
        if review_text:
            num_list = self.extractDigitListFromStr(review_text)
            if len(num_list) > 0:
                i_num_review = num_list[0]

        return i_num_review

    def get_images(self, selector):
        str_images = ""

        conv_list_images = []

        list_images = []
        list_images.append(selector.xpath("//div[@class='product-details-img']/a/@href").get())
        list_images.extend(selector.xpath("//ul[@class='product__thumb-list']//img/@src").getall())

        for x in list_images:
            if "?" in x:
                x = x.split("?")[0]
            if "https" not in x:
                conv_list_images.append("https://www.cosme.com{}".format(x))

        if len(conv_list_images) > 0:
            str_images = ";".join(conv_list_images)

        return str_images

    def get_sku(self, selector):
        return selector.xpath("//meta[@itemprop='sku']/@content").get()

    def get_description(self, selector):
        desc = None
        desc = selector.xpath("//div[@itemprop='description']").get()
        desc = self.remove_a_tag_replace_content(desc)

        return desc

    def get_specifications(self, selector, response):
        specs = None

        dt_list = selector.xpath("//dl[@class='product-desc']/dt").getall()
        dd_list = selector.xpath("//dl[@class='product-desc']/dd").getall()

        if len(dt_list) != len(dd_list):  # should be same length
            breakpoint()

        if len(dt_list) == len(dd_list):
            specs = []

            for i, dt in enumerate(dt_list):
                conv_dt = self.remove_a_tag_replace_content(dt_list[i])
                conv_dt = conv_dt.replace("<dt>", "").replace("</dt>", "")

                conv_dd = self.remove_a_tag_replace_content(dd_list[i])
                conv_dd = conv_dd.replace("<dd>", "").replace("</dd>", "")

                specs.append({"name": conv_dt, "value": conv_dd})

        return specs

    def get_reviews_num(self, selector):
        reviews_num = 0
        return reviews_num

    def get_rating(self, selector):
        src_rating = selector.xpath("//span[@class='unique-product-rating-point']/text()").get()
        if not src_rating:
            return
        f_src_rating = float(src_rating)

        conv_rating = (int(((f_src_rating / 7.0) * 5.0) * 10)) / 10
        return conv_rating

    def parse_product(self, response):
        self.update_cookies(response)

        item = ProductItem()
        item.update(
            {
                "date": datetime.now().replace(microsecond=0).isoformat(),
                "product_id": self.extract_pro_id_from_url(response.url),
                "url": response.url,
                "source": "cosme",
                "returnable": False,
            }
        )
        if response.status == 200:
            item["existence"] = True
        elif "ご指定のページが見つかりません" in response.text:
            item["existence"] = False
            yield item
        selector = scrapy.Selector(text=response.text)
        item["title"] = self.get_title(selector)
        item["title_en"] = None
        item["price"] = self.get_price(selector)
        item["brand"] = self.get_brand(selector)
        item["categories"] = self.get_categories(selector)
        list_ship_days = self.get_shipping_days(selector)
        item["shipping_days_min"] = list_ship_days[0]
        item["shipping_days_max"] = list_ship_days[1]
        item["shipping_fee"] = self.get_shipping_fee(selector)
        item["reviews"] = self.get_reviews(selector)
        item["rating"] = self.get_rating(selector)
        item["images"] = self.get_images(selector)
        item["sku"] = self.get_sku(selector)
        item["description"] = self.get_description(selector)
        item["description_en"] = None
        item["specifications"] = self.get_specifications(selector, response)
        item["summary"] = "{}, {}".format(item["title"], item["brand"])
        item["upc"] = None
        item["videos"] = None
        item["available_qty"] = None
        item["sold_count"] = None
        item["weight"] = None
        item["width"] = None
        item["height"] = None
        item["length"] = None

        item["has_only_default_variant"] = True
        item["variants"] = None
        item["options"] = None

        yield item
