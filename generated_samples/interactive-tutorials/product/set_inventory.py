# Copyright 2022 Google Inc. All Rights Reserved.
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

# [START retail_set_inventory]
# Updating inventory information using Retail API.
#
import datetime
import random
import string
import time

import google.auth
from google.cloud.retail import (
    FulfillmentInfo,
    PriceInfo,
    Product,
    ProductServiceClient,
    SetInventoryRequest,
)
from google.protobuf.field_mask_pb2 import FieldMask

from setup_product.setup_cleanup import create_product, delete_product, get_product

project_id = google.auth.default()[1]
product_id = "".join(random.sample(string.ascii_lowercase, 8))
product_name = (
    "projects/"
    + project_id
    + "/locations/global/catalogs/default_catalog/branches/default_branch/products/"
    + product_id
)


# product inventory info
def get_product_with_inventory_info(product_name: str) -> Product:
    price_info = PriceInfo()
    price_info.price = 15.0
    price_info.original_price = 60.0
    price_info.cost = 8.0
    price_info.currency_code = "USD"

    fulfillment_info = FulfillmentInfo()
    fulfillment_info.type_ = "pickup-in-store"
    fulfillment_info.place_ids = ["store1", "store2"]

    product = Product()
    product.name = product_name
    product.price_info = price_info
    product.fulfillment_info = [fulfillment_info]
    product.availability = "IN_STOCK"

    return product


# set inventory request
def get_set_inventory_request(product_name: str) -> SetInventoryRequest:
    # The request timestamp
    request_time = datetime.datetime.now() + datetime.timedelta(seconds=30)
    set_mask = FieldMask(
        paths=["price_info", "availability", "fulfillment_info", "available_quantity"]
    )

    set_inventory_request = SetInventoryRequest()
    set_inventory_request.inventory = get_product_with_inventory_info(product_name)
    set_inventory_request.set_time = request_time
    set_inventory_request.allow_missing = True
    set_inventory_request.set_mask = set_mask

    print("---set inventory request---")
    print(set_inventory_request)

    return set_inventory_request


# set inventory to product
def set_inventory(product_name: str):
    set_inventory_request = get_set_inventory_request(product_name)
    ProductServiceClient().set_inventory(set_inventory_request)

    # This is a long running operation and its result is not immediately present with get operations,
    # thus we simulate wait with sleep method.
    print("---set inventory, wait 90 seconds:---")
    time.sleep(90)


create_product(product_id)
set_inventory(product_name)
get_product(product_name)
delete_product(product_name)
# [END retail_set_inventory]
