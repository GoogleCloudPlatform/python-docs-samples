# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_control_quickstart_sample]
from google.cloud import storage_control_v2


def storage_control_quickstart(bucket_name: str) -> None:
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    storage_control_client = storage_control_v2.StorageControlClient()
    # The storage layout path uses the global access pattern, in which
    # the “_” denotes this bucket exists in the global namespace.
    layout_path = storage_control_v2.StorageControlClient.storage_layout_path(
        project="_", bucket=bucket_name
    )
    request = storage_control_v2.GetStorageLayoutRequest(
        name=layout_path,
    )
    response = storage_control_client.get_storage_layout(request=request)

    print(f"Performed get_storage_layout request for {response.name}")

    # [END storage_control_quickstart_sample]


if __name__ == "__main__":
    storage_control_quickstart(bucket_name=sys.argv[1])
