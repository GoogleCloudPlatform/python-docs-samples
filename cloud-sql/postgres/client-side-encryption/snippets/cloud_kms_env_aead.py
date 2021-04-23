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
# limitations under the License.

# [START cloud_sql_postgres_cse_key]
import logging

import tink
from tink import aead
from tink.integration import gcpkms

logger = logging.getLogger(__name__)


def init_tink_env_aead(
        key_uri: str,
        credentials: str) -> tink.aead.KmsEnvelopeAead:
    aead.register()

    try:
        gcp_client = gcpkms.GcpKmsClient(key_uri, credentials)
        gcp_aead = gcp_client.get_aead(key_uri)
    except tink.TinkError as e:
        logger.error("Error initializing GCP client: %s", e)
        raise e

    # Create envelope AEAD primitive using AES256 GCM for encrypting the data
    # This key should only be used for client-side encryption to ensure authenticity and integrity
    # of data.
    key_template = aead.aead_key_templates.AES256_GCM
    env_aead = aead.KmsEnvelopeAead(key_template, gcp_aead)

    print(f"Created envelope AEAD Primitive using KMS URI: {key_uri}")

    return env_aead


# [END cloud_sql_postgres_cse_key]
