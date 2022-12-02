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

import datetime
from pathlib import Path, PurePath

import google.auth

from setup_cleanup import create_bucket, upload_blob

project_id = google.auth.default()[1]
timestamp_ = datetime.datetime.now().timestamp().__round__()
BUCKET_NAME = f"{project_id}_products_{timestamp_}"


def create_gcs_bucket(bucket_name=BUCKET_NAME):
    create_bucket(bucket_name)

    path_to_resources_dir = PurePath(
        Path.home(), "cloudshell_open/python-retail/samples/interactive-tutorials/resources"
    )
    upload_blob(bucket_name, str(path_to_resources_dir / "products.json"))
    upload_blob(bucket_name, str(path_to_resources_dir / "products_some_invalid.json"))
    print(f"\nThe gcs bucket {bucket_name} was created")


if __name__ == "__main__":
    create_gcs_bucket()
