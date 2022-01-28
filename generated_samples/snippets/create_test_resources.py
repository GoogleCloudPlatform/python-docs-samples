# Copyright 2021 Google Inc. All Rights Reserved.
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
import re
import time

from google.cloud.storage.bucket import Bucket

from google.cloud import storage
from google.cloud.retail import GcsSource, ImportErrorsConfig, \
    ImportProductsRequest, ProductInputConfig
from google.cloud.retail_v2 import ProductServiceClient

project_number = os.getenv('PROJECT_NUMBER')
bucket_name = os.getenv('BUCKET_NAME')
storage_client = storage.Client()
resource_file = "resources/products.json"
object_name = re.search('resources/(.*?)$', resource_file).group(1)
default_catalog = "projects/{0}/locations/global/catalogs/default_catalog/branches/default_branch".format(
    project_number)


def create_bucket(bucket_name: str) -> Bucket:
    """Create a new bucket in Cloud Storage"""
    print("Creating new bucket:" + bucket_name)
    bucket_exists = check_if_bucket_exists(bucket_name)
    if bucket_exists:
        print("Bucket {} already exists".format(bucket_name))
        return storage_client.bucket(bucket_name)
    else:
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = storage_client.create_bucket(bucket, location="us")
        print(
            "Created bucket {} in {} with storage class {}".format(
                new_bucket.name, new_bucket.location, new_bucket.storage_class
            )
        )
        return new_bucket


def check_if_bucket_exists(new_bucket_name):
    """Check if bucket is already exists"""
    bucket_exists = False
    buckets = storage_client.list_buckets()
    for bucket in buckets:
        if bucket.name == new_bucket_name:
            bucket_exists = True
            break
    return bucket_exists


def upload_data_to_bucket(bucket: Bucket):
    """Upload data to a GCS bucket"""
    blob = bucket.blob(object_name)
    blob.upload_from_filename(resource_file)
    print("Data from {} has being uploaded to {}".format(resource_file,
                                                         bucket.name))


def get_import_products_gcs_request():
    """Get import products from gcs request"""
    gcs_bucket = "gs://{}".format(bucket_name)
    gcs_errors_bucket = "{}/error".format(gcs_bucket)

    gcs_source = GcsSource()
    gcs_source.input_uris = ["{0}/{1}".format(gcs_bucket, object_name)]

    input_config = ProductInputConfig()
    input_config.gcs_source = gcs_source

    errors_config = ImportErrorsConfig()
    errors_config.gcs_prefix = gcs_errors_bucket

    import_request = ImportProductsRequest()
    import_request.parent = default_catalog
    import_request.reconciliation_mode = ImportProductsRequest.ReconciliationMode.INCREMENTAL
    import_request.input_config = input_config
    import_request.errors_config = errors_config

    print("---import products from google cloud source request---")
    print(import_request)

    return import_request


def import_products_from_gcs():
    """Call the Retail API to import products"""
    import_gcs_request = get_import_products_gcs_request()
    gcs_operation = ProductServiceClient().import_products(
        import_gcs_request)
    print(
        "Import operation is started: {}".format(gcs_operation.operation.name))

    while not gcs_operation.done():
        print("Please wait till operation is completed")
        time.sleep(5)
    print("Import products operation is completed")

    if gcs_operation.metadata is not None:
        print("Number of successfully imported products")
        print(gcs_operation.metadata.success_count)
        print("Number of failures during the importing")
        print(gcs_operation.metadata.failure_count)
    else:
        print("Operation.metadata is empty")

    print(
        "Wait 2 -5 minutes till products become indexed in the catalog,\
after that they will be available for search")


created_bucket = create_bucket(bucket_name)
upload_data_to_bucket(created_bucket)
import_products_from_gcs()
