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

from setup_cleanup import create_bq_dataset, create_bq_table, \
    upload_data_to_bq_table

dataset = "products"
valid_products_table = "products"
invalid_products_table = "products_some_invalid"
product_schema = "../resources/product_schema.json"
valid_products_source_file = "../resources/products.json"
invalid_products_source_file = "../resources/products_some_invalid.json"

create_bq_dataset(dataset)
create_bq_table(dataset, valid_products_table, product_schema)
upload_data_to_bq_table(dataset, valid_products_table,
                        valid_products_source_file, product_schema)
create_bq_table(dataset, invalid_products_table, product_schema)
upload_data_to_bq_table(dataset, invalid_products_table,
                        invalid_products_source_file, product_schema)
