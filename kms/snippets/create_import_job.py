# Copyright 2020 Google LLC
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


# [START kms_create_import_job]
def create_import_job(project_id, location_id, key_ring_id, import_job_id):
    """
    Create a new import job in Cloud KMS.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        key_ring_id (string): ID of the Cloud KMS key ring (e.g. 'my-key-ring').
        import_job_id (string): ID of the import job (e.g. 'my-import-job').
    """

    # Import the client library.
    from google.cloud import kms

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Retrieve the fully-qualified key_ring string.
    key_ring_name = client.key_ring_path(project_id, location_id, key_ring_id)

    # Set paramaters for the import job, allowed values for ImportMethod and ProtectionLevel found here:
    # https://googleapis.dev/python/cloudkms/latest/_modules/google/cloud/kms_v1/types/resources.html

    import_method = kms.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    protection_level = kms.ProtectionLevel.HSM
    import_job_params = {"import_method": import_method, "protection_level": protection_level}

    # Call the client to create a new import job.
    import_job = client.create_import_job({"parent": key_ring_name, "import_job_id": import_job_id, "import_job": import_job_params})

    print('Created import job: {}'.format(import_job.name))
# [END kms_create_import_job]
