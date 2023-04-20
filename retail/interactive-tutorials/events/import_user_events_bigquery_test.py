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
from setup_events.setup_cleanup import (
    create_bq_dataset,
    create_bq_table,
    delete_bq_table,
    upload_data_to_bq_table,
)
from setup_events.update_user_events_json import update_events_timestamp


@Retry()
def test_import_products_bq(table_id_prefix):
    dataset = "user_events"
    valid_products_table = f"{table_id_prefix}events"
    product_schema = "../resources/events_schema.json"
    valid_products_source_file = "../resources/user_events.json"

    try:
        update_events_timestamp("../resources/user_events.json")
        update_events_timestamp("../resources/user_events_some_invalid.json")
        create_bq_dataset(dataset)
        create_bq_table(dataset, valid_products_table, product_schema)
        upload_data_to_bq_table(
            dataset, valid_products_table, valid_products_source_file, product_schema
        )
        output = str(
            subprocess.check_output(
                f"python import_user_events_big_query.py {dataset} {valid_products_table}",
                shell=True,
            )
        )
    finally:
        delete_bq_table(dataset, valid_products_table)

    assert re.match(
        '.*import user events from BigQuery source request.*?parent: "projects/.*?/locations/global/catalogs/default_catalog.*',
        output,
    )
    assert re.match(
        ".*import user events from BigQuery source request.*?input_config.*?big_query_source.*",
        output,
    )
    assert re.match(
        ".*the operation was started.*?projects/.*?/locations/global/catalogs/default_catalog/operations/import-user-events.*",
        output,
    )
    assert re.match(".*import user events operation is done.*", output)
    assert re.match(".*number of successfully imported events.*", output)
    assert re.match(".*number of failures during the importing.*?0.*", output)
    assert re.match(".*operation result.*?errors_config.*", output)
