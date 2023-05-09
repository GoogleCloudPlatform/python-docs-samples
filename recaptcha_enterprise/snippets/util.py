# Copyright 2023 Google LLC
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

import hashlib
import hmac
import secrets


def _get_hashed_account_id(account_id: str, key: str) -> str:
    salt = secrets.token_hex(16)
    salted_account_id = salt + account_id

    # Encode the key and salted message as bytes
    key_bytes = bytes(key, 'utf-8')
    salted_message_bytes = bytes(salted_account_id, 'utf-8')

    # Create an HMAC SHA-256 hash of the salted message using the key
    hashed = hmac.new(key_bytes, salted_message_bytes, hashlib.sha256)

    # Get the hex-encoded digest of the hash
    return hashed.hexdigest()
