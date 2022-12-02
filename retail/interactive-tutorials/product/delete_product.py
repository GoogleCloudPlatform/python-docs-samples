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


# Delete product from a catalog using Retail API.
#
import random
import string

import google.auth
from google.cloud.retail import DeleteProductRequest, ProductServiceClient

from setup_product.setup_cleanup import create_product

project_id = google.auth.default()[1]
default_branch_name = (
    "projects/"
    + project_id
    + "/locations/global/catalogs/default_catalog/branches/default_branch"
)
product_id = "".join(random.sample(string.ascii_lowercase, 8))


# get delete product request
def get_delete_product_request(product_name: str):
    delete_product_request = DeleteProductRequest()
    delete_product_request.name = product_name

    print("---delete product request---")
    print(delete_product_request)

    return delete_product_request


# call the Retail API to delete product
def delete_product(product_name: str):
    delete_product_request = get_delete_product_request(product_name)
    ProductServiceClient().delete_product(delete_product_request)

    print("deleting product " + product_name)
    print("---product was deleted:---")


# delete created product
created_product_name = create_product(product_id).name
delete_product(created_product_name)
