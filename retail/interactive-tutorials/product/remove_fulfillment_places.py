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

# Remove place IDs using Retail API.
#
import asyncio
import random
import string

from google.api_core.exceptions import GoogleAPICallError
from google.cloud.retail import (
    ProductServiceAsyncClient,
    RemoveFulfillmentPlacesRequest,
)

from setup_product.setup_cleanup import create_product, delete_product, get_product

product_id = "".join(random.sample(string.ascii_lowercase, 8))


# remove fulfillment request
def get_remove_fulfillment_request(
    product_name: str, store_id
) -> RemoveFulfillmentPlacesRequest:
    remove_fulfillment_request = RemoveFulfillmentPlacesRequest()
    remove_fulfillment_request.product = product_name
    remove_fulfillment_request.type_ = "pickup-in-store"
    remove_fulfillment_request.place_ids = [store_id]
    remove_fulfillment_request.allow_missing = True

    # To send an out-of-order request assign the invalid remove_time here:
    # import datetime
    # remove_fulfillment_request.remove_time = datetime.datetime.now() - datetime.timedelta(days=1)

    print("---remove fulfillment request---")
    print(remove_fulfillment_request)

    return remove_fulfillment_request


async def remove_places(product_name: str):
    print("------remove fulfillment places-----")
    remove_fulfillment_request = get_remove_fulfillment_request(product_name, "store0")
    operation = await ProductServiceAsyncClient().remove_fulfillment_places(
        remove_fulfillment_request
    )
    # This operation doesn't have result or errors. So GoogleAPICallError will be raised.
    try:
        await operation.result()
    except GoogleAPICallError:
        pass

    get_product(product_name)
    delete_product(product_name)


product = create_product(product_id)

asyncio.run(remove_places(product.name))
