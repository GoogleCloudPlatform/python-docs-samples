import google.auth
import time
import jwt
import json

from google.cloud import iam_credentials_v1
from google.auth import credentials

def generate_jwt_payload(service_account_email, resource_url):
  """Generates JWT payload for service account to access application at specified resource url"""
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

def sign_jwt(target_sa, resource_url):
  """Signs JWT payload using ADC and IAM credentials API"""
  # Uses Application Default Credentials
  source_credentials, project_id = google.auth.default()
  # use the IAM api and the users credentials to sign the JWT
  iam_client = iam_credentials_v1.IAMCredentialsClient(credentials=source_credentials)
  name = iam_client.service_account_path('-', target_sa)
  payload = generate_jwt_payload(target_sa, resource_url)
  resp = iam_client.sign_jwt(name=name, payload=payload)
  signed_jwt = resp.signed_jwt
  return signed_jwt

def sign_jwt_with_key_file(credential_key_file_path, resource_url):
  """Signs JWT payload using local service account credential key file"""
  credential_key_file = open(credential_key_file_path)
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
