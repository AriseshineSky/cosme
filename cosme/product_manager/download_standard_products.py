# from datetime import datetime
# import json
# from multiprocessing.pool import ThreadPool
# import re

# from peewee import *
# from playhouse.db_url import connect

# from em_product.product import StandardProduct
# from pymongo import MongoClient
# from urllib.parse import urlparse


# from google.oauth2 import service_account
# from google.cloud.translate_v2 import Client


# from cosme.settings import MONGO_URI
# from utils.site_product import fetch_source_ids


# def connect_to_mongo_by_collection(db_name, collection_name):
#     client = MongoClient(MONGO_URI)
#     db = client[db_name]
#     collection = db[collection_name]
#     return collection


# def invalid_specification(spec):
#     invalid_values = ["상품상세설명 참조", "상품상세 설명 참고", "상세설명참조", "전화"]
#     invalid_keys = [
#         "상품상세설명 참조",
#         "소비자상담관련 전화번호",
#         "A/S 책임자와 전화번호 또는 소비자상담 관련 전화번호",
#         "해당사항없음",
#     ]
#     for value in invalid_values:
#         if value in spec.get("value"):
#             return True
#     for name in invalid_keys:
#         if name in spec.get("name"):
#             return True


# def add_specs_to_description(specs, description):
#     if not specs:
#         return description

#     trs = []
#     for spec in specs:
#         tr_str = f"""<tr><th>{spec["name"]}</th><td><span>{spec["value"]}</span></td></tr>"""
#         trs.append(tr_str)

#     return f"""<tbody>{"".join(trs)}</tbody>""" + description


# def get_specifications(product):
#     if not product["specifications"]:
#         return None, None

#     new_specs = []
#     desc_specs = []
#     for spec in product["specifications"]:
#         if invalid_specification(spec):
#             continue
#         if (
#             spec.get("name").find("기한 ") > -1
#             or spec.get("name").find("사용방법") > -1
#             or spec.get("name").find("화장품법") > -1
#             or spec.get("name").find("사용할 때의 주의사항") > -1
#             or spec.get("name").find("품질보증기준") > -1
#         ):
#             desc_specs.append(spec)

#             continue
#         new_specs.append(spec)

#     if not new_specs:
#         new_specs = None

#     return new_specs, desc_specs


# def format_product(product):
#     new_specs, desc_specs = get_specifications(product)
#     product["specifications"] = new_specs
#     product["description"] = add_specs_to_description(desc_specs, product["description"])

#     return product


# def upadate_product_in_db(collection, product):
#     query = {"_id": product.pop("_id")}
#     new_value = {"$set": product}
#     collection.update_one(query, new_value, True)


# def main():
#     db_name = "cosme"
#     collection_name = "formated_products"
#     collection = connect_to_mongo_by_collection(db_name, collection_name)
#     product_ids = fetch_source_ids(["WEMAKEPRICE"])

#     count_total = 0
#     count_exists = 0
#     with open("cosme_0628_6.txt", "w+") as file:
#         for doc in collection.find(
#             {
#                 "title_en": {"$exists": True},
#                 "price": {"$exists": True, "$ne": None},
#             }
#         ):
#             count_total += 1

#             if str(doc["_id"]) in product_ids or doc.get("options") or doc.get("variants"):
#                 count_exists += 1
#                 continue

#             try:
#                 formated_product = format_product(doc)
#                 if not formated_product or not formated_product["price"]:
#                     continue

#                 standard_product = StandardProduct(**formated_product)
#                 json.dump(standard_product.model_dump(), file, ensure_ascii=False)
#                 file.write("\n")
#             except Exception as e:
#                 breakpoint()
#                 pass

#     print(count_total)


# if __name__ == "__main__":
#     main()
