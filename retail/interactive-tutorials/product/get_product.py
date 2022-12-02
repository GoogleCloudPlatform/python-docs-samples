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


# Get product from a catalog using Retail API.
#
import random
import string

import google.auth
from google.cloud.retail import GetProductRequest, ProductServiceClient

from setup_product.setup_cleanup import create_product, delete_product

project_id = google.auth.default()[1]
product_id = "".join(random.sample(string.ascii_lowercase, 8))


# get product request
def get_product_request(product_name: str) -> object:
    get_product_request = GetProductRequest()
    get_product_request.name = product_name

    print("---get product request---")
    print(get_product_request)

    return get_product_request


# call the Retail API to get product
def get_product(product_name: str):
    # get a product from catalog
    get_request = get_product_request(product_name)
    get_product_response = ProductServiceClient().get_product(get_request)

    print("---get product response:---")
    print(get_product_response)
    return get_product_response


# create a product
created_product = create_product(product_id)
# get created product
product = get_product(created_product.name)
# remove created product
delete_product(created_product.name)
