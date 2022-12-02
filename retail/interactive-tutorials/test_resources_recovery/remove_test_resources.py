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

import os
import shlex
import subprocess

from google.api_core.exceptions import NotFound, PermissionDenied
import google.auth
from google.cloud import storage
from google.cloud.retail import DeleteProductRequest, ListProductsRequest, \
    ProductServiceClient
from google.cloud.storage.bucket import Bucket


project_id = google.auth.default()[1]
product_bucket_name = os.environ['BUCKET_NAME']
events_bucket_name = os.environ['EVENTS_BUCKET_NAME']

product_dataset = "products"
events_dataset = "user_events"

default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog/branches/default_branch"

storage_client = storage.Client()


def delete_bucket(bucket_name):
    """Delete bucket"""
    try:
        bucket = storage_client.get_bucket(bucket_name)
    except NotFound:
        print(f"Bucket {bucket_name} does not exists")
    else:
        delete_object_from_bucket(bucket)
        bucket.delete()
        print(f"bucket {bucket_name} is deleted")


def delete_object_from_bucket(bucket: Bucket):
    """Delete object from bucket"""
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
    print(f"all objects are deleted from GCS bucket {bucket.name}")


def delete_all_products():
    """Delete all products in the catalog"""
    print("Deleting all products, please wait")
    product_client = ProductServiceClient()
    list_request = ListProductsRequest()
    list_request.parent = default_catalog
    products = product_client.list_products(list_request)
    delete_count = 0
    for product in products:
        delete_request = DeleteProductRequest()
        delete_request.name = product.name
        try:
            product_client.delete_product(delete_request)
            delete_count += 1
        except PermissionDenied:
            print(
                "Ignore PermissionDenied in case the product does not exist at time of deletion")
    print(f"{delete_count} products were deleted from {default_catalog}")


def delete_bq_dataset_with_tables(dataset):
    """Delete a BigQuery dataset with all tables"""
    delete_dataset_command = f"bq rm -r -d -f {dataset}"
    output = subprocess.check_output(shlex.split(delete_dataset_command))
    print(output)


delete_bucket(product_bucket_name)
delete_bucket(events_bucket_name)
delete_all_products()
delete_bq_dataset_with_tables(product_dataset)
delete_bq_dataset_with_tables(events_dataset)
