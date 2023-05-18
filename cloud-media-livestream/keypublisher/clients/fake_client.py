# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""File containing a fake CPIX client for demonstration purposes."""

import secrets

from typing import Dict
from typing import List

from . import cpix_client


class FakeClient(cpix_client.CpixClient):
    """Fake CPIX client, for demonstration purposes only."""

    def fetch_keys(self, media_id: str, key_ids: List[str]) -> Dict[str, object]:
        """Generates random key information.

        Args:
        media_id (string): Name for your asset, sometimes used by DRM providers to
        show usage and reports.
        key_ids (list[string]): List of IDs of any keys to fetch and prepare.

        Returns:
        dict: Object containing key information to be written to Secret Manager.
        """
        key_info = dict()
        key_info['encryptionKeys'] = []
        for key_id in key_ids:
            fake_key = secrets.token_hex(16)
            key_info['encryptionKeys'].append({
                    'keyId': key_id.replace('-', ''),
                    'key': fake_key,
                    'keyUri': (
                        f'https://storage.googleapis.com/bucket-name/{fake_key}.bin'
                    ),
                    'iv': secrets.token_hex(16),
                })
        return key_info

    def required_env_vars(self) -> List[str]:
        return []
