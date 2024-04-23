#!/usr/bin/env python
# Copyright 2024 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import google.auth
import time
import jwt
import json

from google.cloud import iam_credentials_v1

def generate_jwt_payload(service_account_email: str, resource_url: str) -> str:
  """Generates JWT payload for service account
  
  The resource url provided must be the same as the url of the IAP secured resource
  """
  iat = time.time()
  exp = iat + 3600
  payload = {
      'iss': service_account_email,
      'sub': service_account_email,
      'aud': resource_url,
      'iat': iat,
      'exp': exp,
  }
  return json.dumps(payload)

def sign_jwt(target_sa: str, resource_url: str) -> str:
  """Signs JWT payload using ADC and IAM credentials API """
  # Uses Application Default Credentials
  source_credentials, project_id = google.auth.default()
  # use the IAM api and the users credentials to sign the JWT
  iam_client = iam_credentials_v1.IAMCredentialsClient(credentials=source_credentials)
  name = iam_client.service_account_path('-', target_sa)
  payload = generate_jwt_payload(target_sa, resource_url)
  resp = iam_client.sign_jwt(name=name, payload=payload)
  signed_jwt = resp.signed_jwt
  return signed_jwt

def sign_jwt_with_key_file(credential_key_file_path: str, resource_url: str) -> str:
  """Signs JWT payload using local service account credential key file"""
  with open(credential_key_file_path, 'r') as credential_key_file:
      key_data = json.load(credential_key_file)
  
  # Data retrieved from credential key file
  PRIVATE_KEY_ID_FROM_JSON = key_data["private_key_id"]
  PRIVATE_KEY_FROM_JSON = key_data["private_key"]
  SERVICE_ACCOUNT_EMAIL=key_data["client_email"]
  
  # Creating JWT Header and Payload
  additional_headers = {'kid': PRIVATE_KEY_ID_FROM_JSON}
  payload = generate_jwt_payload(service_account_email=SERVICE_ACCOUNT_EMAIL, resource_url=resource_url)
  # Signing JWT
  signed_jwt = jwt.encode(
      payload,
      PRIVATE_KEY_FROM_JSON,
      headers=additional_headers,
      algorithm='RS256',
  )
  return signed_jwt
