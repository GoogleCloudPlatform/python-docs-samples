# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def create_table_cmek(table_id: str, kms_key_name: str) -> None:
    orig_table_id = table_id
    orig_key_name = kms_key_name
    # [START bigquery_create_table_cmek]
    from google.cloud import bigquery

    client = bigquery.Client()

    # TODO(dev): Change table_id to the full name of the table you want to create.
    table_id = "your-project.your_dataset.your_table_name"

    # Set the encryption key to use for the table.
    # TODO: Replace this key with a key you have created in Cloud KMS.
    kms_key_name = "projects/your-project/locations/us/keyRings/test/cryptoKeys/test"

    # [END bigquery_create_table_cmek]

    table_id = orig_table_id
    kms_key_name = orig_key_name

    # [START bigquery_create_table_cmek]
    table = bigquery.Table(table_id)
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=kms_key_name
    )
    table = client.create_table(table)  # API request

    print(f"Created {table_id}.")
    print(f"Key: {table.encryption_configuration.kms_key_name}.")

    # [END bigquery_create_table_cmek]
