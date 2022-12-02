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
import re
import shlex
import subprocess
import time

import google.auth
from google.cloud import storage
from google.cloud.retail import GcsSource, ImportErrorsConfig, \
    ImportProductsRequest, ProductInputConfig
from google.cloud.retail import ProductServiceClient
from google.cloud.storage.bucket import Bucket

products_bucket_name = os.environ['BUCKET_NAME']
events_bucket_name = os.environ['EVENTS_BUCKET_NAME']
project_id = google.auth.default()[1]

product_resource_file = "../resources/products.json"
events_source_file = "../resources/user_events.json"

product_dataset = "products"
product_table = "products"
product_schema = "../resources/product_schema.json"
events_dataset = "user_events"
events_table = "events"
events_schema = "../resources/events_schema.json"

object_name = re.search('resources/(.*?)$', product_resource_file).group(1)
default_catalog = f"projects/{project_id}/locations/global/catalogs/default_catalog/branches/default_branch"

storage_client = storage.Client()


def create_bucket(bucket_name: str) -> Bucket:
    """Create a new bucket in Cloud Storage"""
    print("Creating new bucket:" + bucket_name)
    bucket_exists = check_if_bucket_exists(bucket_name)
    if bucket_exists:
        print(f"Bucket {bucket_name} already exists")
        return storage_client.bucket(bucket_name)
    else:
        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = "STANDARD"
        new_bucket = storage_client.create_bucket(bucket, location="us")
        print(
            f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}"
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
    blob.upload_from_filename(product_resource_file)
    print(f"Data from {product_resource_file} has being uploaded to {bucket.name}")


def get_import_products_gcs_request():
    """Get import products from gcs request"""
    gcs_bucket = f"gs://{products_bucket_name}"
    gcs_errors_bucket = f"{gcs_bucket}/error"

    gcs_source = GcsSource()
    gcs_source.input_uris = [f"{gcs_bucket}/{object_name}"]

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
        f"Import operation is started: {gcs_operation.operation.name}")

    while not gcs_operation.done():
        print("Please wait till operation is completed")
        time.sleep(30)
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


def create_bq_dataset(dataset_name):
    """Create a BigQuery dataset"""
    print(f"Creating dataset {dataset_name}")
    try:
        list_bq_dataset(project_id, dataset_name)
        print(f"dataset {dataset_name} already exists")
    except subprocess.CalledProcessError:
        create_dataset_command = f'bq --location=US mk -d --default_table_expiration 3600 --description "This is my dataset." {project_id}:{dataset_name}'
        subprocess.check_output(shlex.split(create_dataset_command))
        print("dataset is created")


def list_bq_dataset(project_id: str, dataset_name: str):
    """List BigQuery dataset in the project"""
    list_dataset_command = f"bq show {project_id}:{dataset_name}"
    dataset_name = subprocess.check_output(shlex.split(list_dataset_command))
    return str(dataset_name)


def create_bq_table(dataset, table_name, schema):
    """Create a BigQuery table"""
    print(f"Creating BigQuery table {table_name}")
    if table_name not in list_bq_tables(dataset):
        create_table_command = f"bq mk --table {project_id}:{dataset}.{table_name} {schema}"
        output = subprocess.check_output(shlex.split(create_table_command))
        print(output)
        print("table is created")
    else:
        print(f"table {table_name} already exists")


def list_bq_tables(dataset):
    """List BigQuery tables in the dataset"""
    list_tables_command = f"bq ls {project_id}:{dataset}"
    tables = subprocess.check_output(shlex.split(list_tables_command))
    return str(tables)


def upload_data_to_bq_table(dataset, table_name, source, schema):
    """Upload data to the table from specified source file"""
    print(f"Uploading data from {source} to the table {dataset}.{table_name}")
    upload_data_command = f"bq load --source_format=NEWLINE_DELIMITED_JSON {project_id}:{dataset}.{table_name} {source} {schema}"
    output = subprocess.check_output(shlex.split(upload_data_command))
    print(output)


# Create a GCS bucket with products.json file
created_products_bucket = create_bucket(products_bucket_name)
upload_data_to_bucket(created_products_bucket)

# Create a GCS bucket with user_events.json file
created_events_bucket = create_bucket(events_bucket_name)
upload_data_to_bucket(created_events_bucket)

# Import prodcuts from the GCS bucket to the Retail catalog
import_products_from_gcs()

# Create a BigQuery table with products
create_bq_dataset(product_dataset)
create_bq_table(product_dataset, product_table, product_schema)
upload_data_to_bq_table(product_dataset, product_table,
                        product_resource_file, product_schema)

# Create a BigQuery table with user events
create_bq_dataset(events_dataset)
create_bq_table(events_dataset, events_table, events_schema)
upload_data_to_bq_table(events_dataset, events_table, events_source_file,
                        events_schema)
