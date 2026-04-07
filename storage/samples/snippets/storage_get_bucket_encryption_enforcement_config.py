# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START storage_get_bucket_encryption_enforcement_config]
from google.cloud import storage


def get_bucket_encryption_enforcement_config(bucket_name):
    """Gets the bucket encryption enforcement configuration."""
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    print(f"Encryption Enforcement Config for bucket {bucket.name}:")

    cmek_config = bucket.encryption.customer_managed_encryption_enforcement_config
    csek_config = bucket.encryption.customer_supplied_encryption_enforcement_config
    gmek_config = bucket.encryption.google_managed_encryption_enforcement_config

    print(
        f"Customer-managed encryption enforcement config restriction mode: {cmek_config.restriction_mode if cmek_config else None}"
    )
    print(
        f"Customer-supplied encryption enforcement config restriction mode: {csek_config.restriction_mode if csek_config else None}"
    )
    print(
        f"Google-managed encryption enforcement config restriction mode: {gmek_config.restriction_mode if gmek_config else None}"
    )


# [END storage_get_bucket_encryption_enforcement_config]


if __name__ == "__main__":
    get_bucket_encryption_enforcement_config(bucket_name="your-unique-bucket-name")
