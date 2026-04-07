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

# [START storage_update_bucket_encryption_enforcement_config]
from google.cloud import storage
from google.cloud.storage.bucket import EncryptionEnforcementConfig


def update_bucket_encryption_enforcement_config(bucket_name):
    """Updates the encryption enforcement policy for a bucket."""
    # The ID of your GCS bucket with GMEK and CSEK restricted
    # bucket_name = "your-unique-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    # Update a specific type (e.g., change GMEK to NotRestricted)
    bucket.encryption.google_managed_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="NotRestricted")
    )

    # Update another type (e.g., change CMEK to FullyRestricted)
    bucket.encryption.customer_managed_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="FullyRestricted")
    )

    # Keeping CSEK unchanged
    bucket.encryption.customer_supplied_encryption_enforcement_config = (
        EncryptionEnforcementConfig(restriction_mode="FullyRestricted")
    )

    bucket.patch()

    print(f"Encryption enforcement policy updated for bucket {bucket.name}.")

    gmek = bucket.encryption.google_managed_encryption_enforcement_config
    cmek = bucket.encryption.customer_managed_encryption_enforcement_config
    csek = bucket.encryption.customer_supplied_encryption_enforcement_config

    print(f"GMEK restriction mode: {gmek.restriction_mode if gmek else 'None'}")
    print(f"CMEK restriction mode: {cmek.restriction_mode if cmek else 'None'}")
    print(f"CSEK restriction mode: {csek.restriction_mode if csek else 'None'}")


# [END storage_update_bucket_encryption_enforcement_config]


if __name__ == "__main__":
    update_bucket_encryption_enforcement_config(bucket_name="your-unique-bucket-name")
