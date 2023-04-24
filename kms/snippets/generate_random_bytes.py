# Copyright 2021 Google LLC
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


# [START kms_generate_random_bytes]
def generate_random_bytes(project_id, location_id, num_bytes):
    """
    Generate random bytes with entropy sourced from the given location.

    Args:
        project_id (string): Google Cloud project ID (e.g. 'my-project').
        location_id (string): Cloud KMS location (e.g. 'us-east1').
        num_bytes (integer): number of bytes of random data.

    Returns:
        bytes: Encrypted ciphertext.

    """

    # Import the client library.
    from google.cloud import kms

    # Import base64 for encoding the bytes for printing.
    import base64

    # Create the client.
    client = kms.KeyManagementServiceClient()

    # Build the location name.
    location_name = client.common_location_path(project_id, location_id)

    # Call the API.
    protection_level = kms.ProtectionLevel.HSM
    random_bytes_response = client.generate_random_bytes(
      request={'location': location_name, 'length_bytes': num_bytes, 'protection_level': protection_level})

    print('Random bytes: {}'.format(base64.b64encode(random_bytes_response.data)))
    return random_bytes_response
# [END kms_generate_random_bytes]
