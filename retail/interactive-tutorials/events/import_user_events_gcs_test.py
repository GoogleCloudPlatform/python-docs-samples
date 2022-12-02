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

from setup_events.setup_cleanup import create_bucket, delete_bucket, upload_blob
from setup_events.update_user_events_json import update_events_timestamp


def test_import_events_gcs(bucket_name_prefix):
    # gcs buckets have a limit of 63 characters. Get the last 60 characters
    bucket_name = bucket_name_prefix[63:]

    try:
        update_events_timestamp("../resources/user_events.json")
        update_events_timestamp("../resources/user_events_some_invalid.json")
        create_bucket(bucket_name)
        upload_blob(bucket_name, "../resources/user_events.json")

        output = str(
            subprocess.check_output("python import_user_events_gcs.py", shell=True)
        )
    finally:
        delete_bucket(bucket_name)

    assert re.match(
        '.*import user events from google cloud source request.*?parent: "projects/.*?/locations/global/catalogs/default_catalog.*',
        output,
    )
    assert re.match(
        ".*import user events from google cloud source request.*?input_config.*?gcs_source.*",
        output,
    )
    assert re.match(
        ".*the operation was started.*?projects/.*?/locations/global/catalogs/default_catalog/operations/import-user-events.*",
        output,
    )
    assert re.match(".*import user events operation is done.*", output)
    assert re.match(".*number of successfully imported events.*?4.*", output)
    assert re.match(".*number of failures during the importing.*?0.*", output)
    assert re.match(".*operation result.*?errors_config.*", output)
