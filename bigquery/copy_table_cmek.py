# Copyright 2019 Google LLC
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


def copy_table_cmek(dest_table_id: str, orig_table_id: str, kms_key_name: str) -> None:

    # [START bigquery_copy_table_cmek]
    from google.cloud import bigquery

    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO(developer): Set dest_table_id to the ID of the destination table.
    # dest_table_id = "your-project.your_dataset.your_table_name"

    # TODO(developer): Set orig_table_id to the ID of the original table.
    # orig_table_id = "your-project.your_dataset.your_table_name"

    # Set the encryption key to use for the destination.
    # TODO(developer): Replace this key with a key you have created in KMS.
    # kms_key_name = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
    #     your-project, location, your-ring, your-key
    # )

    job_config = bigquery.CopyJobConfig(
        destination_encryption_configuration=bigquery.EncryptionConfiguration(
            kms_key_name=kms_key_name
        )
    )
    job = client.copy_table(orig_table_id, dest_table_id, job_config=job_config)
    job.result()  # Wait for the job to complete.

    dest_table = client.get_table(dest_table_id)  # Make an API request.
    if dest_table.encryption_configuration.kms_key_name == kms_key_name:
        print("A copy of the table created")
    # [END bigquery_copy_table_cmek]
