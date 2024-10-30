# from datetime import datetime
# import json
# from multiprocessing.pool import ThreadPool
# import re

# from peewee import *

# from em_product.product import StandardProduct
# from pymongo import MongoClient


# from cosme.settings import MONGO_URI
# from utils.site_product import fetch_source_ids

# from .formatter import to_standard


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
#     collection = connect_to_mongo_by_collection(db_name, "products")
#     standard = connect_to_mongo_by_collection(db_name, "standard")
#     pool = ThreadPool(10)

#     count_total = 0
#     query = {}
#     for doc in collection.find(query):
#         count_total += 1

#         try:
#             formated_product = to_standard(doc)
#             if not formated_product or not formated_product["price"]:
#                 continue

#             standard_product = StandardProduct(**formated_product)
#             # upadate_product_in_db(standard, {**standard_product.model_dump(), "_id": doc["_id"]})
#             pool.apply_async(
#                 upadate_product_in_db,
#                 args=(standard, {**standard_product.model_dump(), "_id": doc["_id"]}),
#             )
#         except Exception as e:
#             pass

#     pool.close()
#     pool.join()

#     print(count_total)


# if __name__ == "__main__":
#     main()
