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

import re
import subprocess

from google.api_core.retry import Retry
from setup_product.setup_cleanup import create_bucket, delete_bucket, upload_blob


@Retry()
def test_import_products_gcs(bucket_name_prefix):
    # gcs buckets have a limit of 63 characters. Get the last 60 characters
    bucket_name = bucket_name_prefix[63:]

    try:
        create_bucket(bucket_name)
        upload_blob(bucket_name, "../resources/products.json")

        output = str(
            subprocess.check_output(
                f"python import_products_gcs.py {bucket_name}", shell=True
            )
        )
    finally:
        delete_bucket(bucket_name)

    assert re.match(".*import products from google cloud source request.*", output)
    assert re.match('.*input_uris: "gs://.*/products.json".*', output)
    assert re.match(".*the operation was started.*", output)
    assert re.match(
        ".*projects/.*/locations/global/catalogs/default_catalog/branches/0/operations/import-products.*",
        output,
    )

    assert re.match(".*number of successfully imported products.*?316.*", output)
    assert re.match(".*number of failures during the importing.*?0.*", output)
