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


# Create, update, get and delete product in a catalog using Retail API.
#
import random
import string

import google.auth
from google.cloud.retail import (
    CreateProductRequest,
    DeleteProductRequest,
    GetProductRequest,
    PriceInfo,
    Product,
    ProductServiceClient,
    UpdateProductRequest,
)
from google.cloud.retail_v2.types import product

project_id = google.auth.default()[1]
default_branch_name = (
    "projects/"
    + project_id
    + "/locations/global/catalogs/default_catalog/branches/default_branch"
)
product_id = "".join(random.sample(string.ascii_lowercase, 8))
product_name = f"{default_branch_name}/products/{product_id}"


# generate product for create
def generate_product() -> Product:
    price_info = PriceInfo()
    price_info.price = 30.0
    price_info.original_price = 35.5
    price_info.currency_code = "USD"
    return product.Product(
        title="Nest Mini",
        type_=product.Product.Type.PRIMARY,
        categories=["Speakers and displays"],
        brands=["Google"],
        price_info=price_info,
        availability="IN_STOCK",
    )


# generate product for update
def generate_product_for_update() -> Product:
    price_info = PriceInfo()
    price_info.price = 20.0
    price_info.original_price = 25.5
    price_info.currency_code = "EUR"
    return product.Product(
        id=product_id,
        name=product_name,
        title="Updated Nest Mini",
        type_=product.Product.Type.PRIMARY,
        categories=["Updated Speakers and displays"],
        brands=["Updated Google"],
        availability="OUT_OF_STOCK",
        price_info=price_info,
    )


# create product
def create_product() -> object:
    create_product_request = CreateProductRequest()
    create_product_request.product = generate_product()
    create_product_request.product_id = product_id
    create_product_request.parent = default_branch_name

    print("---create product request---")
    print(create_product_request)

    product_created = ProductServiceClient().create_product(create_product_request)
    print("---created product:---")
    print(product_created)
    return product_created


# get product
def get_product() -> object:
    get_product_request = GetProductRequest()
    get_product_request.name = product_name

    print("---get product request---")
    print(get_product_request)

    get_product_response = ProductServiceClient().get_product(get_product_request)

    print("---get product response:---")
    print(get_product_response)
    return get_product_response


# update product
def update_product():
    update_product_request = UpdateProductRequest()
    update_product_request.product = generate_product_for_update()
    update_product_request.allow_missing = True

    print("---update product request---")
    print(update_product_request)

    updated_product = ProductServiceClient().update_product(update_product_request)
    print("---updated product---:")
    print(updated_product)
    return updated_product


# delete product
def delete_product():
    delete_product_request = DeleteProductRequest()
    delete_product_request.name = product_name

    print("---delete product request---")
    print(delete_product_request)

    ProductServiceClient().delete_product(delete_product_request)

    print("deleting product " + product_name)
    print("---product was deleted:---")


# call the methods
create_product()
get_product()
update_product()
delete_product()
