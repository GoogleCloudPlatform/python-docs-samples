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

# [START storage_set_bucket_encryption_enforcement_config]
from google.cloud import storage
from google.cloud.storage.bucket import EncryptionEnforcementConfig


def set_bucket_encryption_enforcement_config(bucket_name):
    """Creates a bucket with encryption enforcement configuration."""
    # The ID of your GCS bucket
    # bucket_name = "your-unique-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Setting restriction_mode to "FullyRestricted" for Google-managed encryption (GMEK)
    # means objects cannot be created using the default Google-managed keys.
    bucket.encryption.google_managed_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="FullyRestricted")
    )

    # Setting restriction_mode to "NotRestricted" for Customer-managed encryption (CMEK)
    # ensures that objects ARE permitted to be created using Cloud KMS keys.
    bucket.encryption.customer_managed_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="NotRestricted")
    )

    # Setting restriction_mode to "FullyRestricted" for Customer-supplied encryption (CSEK)
    # prevents objects from being created using raw, client-side provided keys.
    bucket.encryption.customer_supplied_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="FullyRestricted")
    )

    bucket.create()

    print(f"Created bucket {bucket.name} with Encryption Enforcement Config.")


# [END storage_set_bucket_encryption_enforcement_config]


if __name__ == "__main__":
    set_bucket_encryption_enforcement_config(bucket_name="your-unique-bucket-name")
