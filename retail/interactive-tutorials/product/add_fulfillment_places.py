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

# Adding place IDs using Retail API.
#
import asyncio
import random
import string

from google.api_core.exceptions import GoogleAPICallError
import google.auth
from google.cloud.retail import AddFulfillmentPlacesRequest, ProductServiceAsyncClient

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
    product_name: str, place_id
) -> AddFulfillmentPlacesRequest:
    add_fulfillment_request = AddFulfillmentPlacesRequest()
    add_fulfillment_request.product = product_name
    add_fulfillment_request.type_ = "pickup-in-store"
    add_fulfillment_request.place_ids = [place_id]
    add_fulfillment_request.allow_missing = True

    # To send an out-of-order request assign the invalid add_time here:
    # import datetime
    # add_fulfillment_request.add_time = datetime.datetime.now() - datetime.timedelta(days=1)

    print("---add fulfillment request---")
    print(add_fulfillment_request)

    return add_fulfillment_request


async def add_places(product_name: str):
    print("------add fulfillment places-----")
    add_fulfillment_request = get_add_fulfillment_request(product_name, "store2")
    operation = await ProductServiceAsyncClient().add_fulfillment_places(
        add_fulfillment_request
    )
    # This operation doesn't have result or errors. So GoogleAPICallError will be raised.
    try:
        await operation.result()
    except GoogleAPICallError:
        pass

    get_product(product_name)
    delete_product(product_name)


create_product(product_id)

asyncio.run(add_places(product_name))
