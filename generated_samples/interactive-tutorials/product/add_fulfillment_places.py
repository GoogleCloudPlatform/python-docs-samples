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

# [START retail_add_fulfillment_places]
# Adding place IDs using Retail API.
#
import datetime
import random
import string
import time

import google.auth
from google.cloud.retail import AddFulfillmentPlacesRequest, ProductServiceClient

from setup_product.setup_cleanup import create_product, delete_product, get_product

project_id = google.auth.default()[1]
product_id = "".join(random.sample(string.ascii_lowercase, 8))
product_name = (
    "projects/"
    + project_id
    + "/locations/global/catalogs/default_catalog/branches/default_branch/products/"
    + product_id
)


# add fulfillment request
def get_add_fulfillment_request(
    product_name: str, timestamp, place_id
) -> AddFulfillmentPlacesRequest:
    add_fulfillment_request = AddFulfillmentPlacesRequest()
    add_fulfillment_request.product = product_name
    add_fulfillment_request.type_ = "pickup-in-store"
    add_fulfillment_request.place_ids = [place_id]
    add_fulfillment_request.add_time = timestamp
    add_fulfillment_request.allow_missing = True

    print("---add fulfillment request---")
    print(add_fulfillment_request)

    return add_fulfillment_request


# add fulfillment places to product
def add_fulfillment_places(product_name: str, timestamp, place_id):
    add_fulfillment_request = get_add_fulfillment_request(
        product_name, timestamp, place_id
    )
    ProductServiceClient().add_fulfillment_places(add_fulfillment_request)

    # This is a long running operation and its result is not immediately present with get operations,
    # thus we simulate wait with sleep method.
    print("---add fulfillment places, wait 90 seconds :---")
    time.sleep(90)


# [END retail_add_fulfillment_places]


create_product(product_id)

# The request timestamp
current_date = datetime.datetime.now() + datetime.timedelta(seconds=30)
print(f"------add fulfilment places with current date: {current_date}-----")
add_fulfillment_places(product_name, current_date, "store2")
get_product(product_name)
delete_product(product_name)
