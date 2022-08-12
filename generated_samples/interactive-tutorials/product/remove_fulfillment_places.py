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

# [START retail_remove_fulfillment_places]
# Remove place IDs using Retail API.
#
import datetime
import random
import string
import time

from google.cloud.retail import ProductServiceClient, RemoveFulfillmentPlacesRequest

from setup_product.setup_cleanup import create_product, delete_product, get_product

product_id = "".join(random.sample(string.ascii_lowercase, 8))


# remove fulfillment request
def get_remove_fulfillment_request(
    product_name: str, timestamp, store_id
) -> RemoveFulfillmentPlacesRequest:
    remove_fulfillment_request = RemoveFulfillmentPlacesRequest()
    remove_fulfillment_request.product = product_name
    remove_fulfillment_request.type_ = "pickup-in-store"
    remove_fulfillment_request.place_ids = [store_id]
    remove_fulfillment_request.remove_time = timestamp
    remove_fulfillment_request.allow_missing = True

    print("---remove fulfillment request---")
    print(remove_fulfillment_request)

    return remove_fulfillment_request


# remove fulfillment places to product
def remove_fulfillment_places(product_name: str, timestamp, store_id):
    remove_fulfillment_request = get_remove_fulfillment_request(
        product_name, timestamp, store_id
    )
    ProductServiceClient().remove_fulfillment_places(remove_fulfillment_request)

    # This is a long running operation and its result is not immediately present with get operations,
    # thus we simulate wait with sleep method.
    print("---remove fulfillment places, wait 90 seconds:---")
    time.sleep(90)


# [END retail_remove_fulfillment_places]


product = create_product(product_id)

# The request timestamp
current_date = datetime.datetime.now()

print(f"------remove fulfilment places with current date: {current_date}-----")
remove_fulfillment_places(product.name, current_date, "store0")
get_product(product.name)
delete_product(product.name)
