# Copyright 2025 Google LLC
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

# Hello developer! This file uses special syntax to import parts of
# this file into the Google Cloud documentation
#
# You can safely ignore any line that starts with:
#  * `# [START `
#  * `# [END `
#

# [START secret_create_secret_ipy_style]
from google.cloud import secretmanager
# [END secret_create_secret_ipy_style]

"""
# Define these values to use this sample:
# [START secret_create_secret_ipy_style]
project_id = "PROJECT_ID"
secret_id = "SECRET_ID"
# [END secret_create_secret_ipy_style]
"""

def create_secret(project_id, secret_id):
    # [START secret_create_secret_ipy_style]
    client = secretmanager.SecretManagerServiceClient()
    response = client.create_secret(
        parent=f"projects/{project_id}",
        secret_id=secret_id,
        secret={"replication": {"automatic": {}}},
    )

    print(f"Created secret: {response.name}")
    # [START secret_create_secret_ipy_style]
    return response

# [START secret_create_secret_ipy_style]
"""
Run this sample:
create_secret(project_id, secret_id)
"""
# [END secret_create_secret_ipy_style]
