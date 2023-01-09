# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Import products into a catalog from inline source using Retail API
#
import random
import string
import time

import google.auth
from google.cloud.retail import (
    ColorInfo,
    FulfillmentInfo,
    ImportProductsRequest,
    PriceInfo,
    Product,
    ProductInlineSource,
    ProductInputConfig,
    ProductServiceClient,
)
from google.protobuf.field_mask_pb2 import FieldMask

project_id = google.auth.default()[1]

default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog/branches/default_branch"


# prepare product to import as inline source
def get_products():
    products = []
    product1 = Product()
    product2 = Product()

    price_info1 = PriceInfo()
    price_info1.price = 16.0
    price_info1.original_price = 45.0
    price_info1.cost = 12.0
    price_info1.currency_code = "USD"

    color_info1 = ColorInfo()
    color_info1.color_families = ["Blue"]
    color_info1.colors = ["Light blue", "Blue", "Dark blue"]

    fulfillment_info1 = FulfillmentInfo()
    fulfillment_info1.type_ = "pickup-in-store"
    fulfillment_info1.place_ids = ["store1", "store2"]

    field_mask1 = FieldMask(paths=["title", "categories", "price_info", "color_info"])

    # TO CHECK ERROR HANDLING COMMENT OUT THE PRODUCT TITLE HERE:
    product1.title = "#IamRemarkable Pen"
    product1.id = "".join(random.sample(string.ascii_lowercase, 8))
    product1.categories = ["Office"]
    product1.uri = "https://shop.googlemerchandisestore.com/Google+Redesign/Office/IamRemarkable+Pen"
    product1.brands = ["#IamRemarkable"]
    product1.price_info = price_info1
    product1.color_info = color_info1
    product1.fulfillment_info = [fulfillment_info1]
    product1.retrievable_fields = field_mask1

    price_info2 = PriceInfo()
    price_info2.price = 35.0
    price_info2.original_price = 45.0
    price_info2.cost = 12.0
    price_info2.currency_code = "USD"

    color_info2 = ColorInfo()
    color_info2.color_families = ["Blue"]
    color_info2.colors = ["Sky blue"]

    fulfillment_info2 = FulfillmentInfo()
    fulfillment_info2.type_ = "pickup-in-store"
    fulfillment_info2.place_ids = ["store2", "store3"]

    field_mask2 = FieldMask(paths=["title", "categories", "price_info", "color_info"])

    product2.title = "Android Embroidered Crewneck Sweater"
    product2.id = "".join(random.sample(string.ascii_lowercase, 8))
    product2.categories = ["Apparel"]
    product2.uri = "https://shop.googlemerchandisestore.com/Google+Redesign/Apparel/Android+Embroidered+Crewneck+Sweater"
    product2.brands = ["Android"]
    product2.price_info = price_info2
    product2.color_info = color_info2
    product2.fulfillment_info = [fulfillment_info2]
    product2.retrievable_fields = field_mask2

    products.append(product1)
    products.append(product2)
    return products


# get import products from inline source request
def get_import_products_inline_request(products_to_import):
    # TO CHECK ERROR HANDLING PASTE THE INVALID CATALOG NAME HERE:
    # default_catalog = "invalid_catalog_name"
    inline_source = ProductInlineSource()
    inline_source.products = products_to_import

    input_config = ProductInputConfig()
    input_config.product_inline_source = inline_source

    import_request = ImportProductsRequest()
    import_request.parent = default_catalog
    import_request.input_config = input_config

    print("---import products from inline source request---")
    print(import_request)

    return import_request


# call the Retail API to import products
def import_products_from_inline_source():
    import_request = get_import_products_inline_request(get_products())
    import_operation = ProductServiceClient().import_products(import_request)

    print("---the operation was started:----")
    print(import_operation.operation.name)

    while not import_operation.done():
        print("---please wait till operation is done---")
        time.sleep(5)
    print("---import products operation is done---")

    if import_operation.metadata is not None:
        print("---number of successfully imported products---")
        print(import_operation.metadata.success_count)
        print("---number of failures during the importing---")
        print(import_operation.metadata.failure_count)
    else:
        print("---operation.metadata is empty---")


import_products_from_inline_source()
