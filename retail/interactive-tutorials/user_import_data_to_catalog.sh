#!/bin/bash

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

{
  # Create a GCS bucket and upload the product data to the bucket
  output=$(python ~/cloudshell_open/python-docs-samples/retail/interactive-tutorials/product/setup_product/products_create_gcs_bucket.py)

  # Get the bucket name and store it in the env variable BUCKET_NAME
  temp="${output#*The gcs bucket }"
  bucket_name="${temp% was created*}"
  export BUCKET_NAME=$bucket_name

  # Import products to the Retail catalog
  python ~/cloudshell_open/python-docs-samples/retail/interactive-tutorials/product/import_products_gcs.py
} && {
  # Print success message
  echo "====================================="
  echo "Your Retail catalog is ready to use!"
  echo "====================================="
} || {
  # Print error message
  echo "====================================="
  echo "Your Retail catalog wasn't created! Please fix the errors above!"
  echo "====================================="
}
