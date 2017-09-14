import json
import logging
import requests
import time

from pprint import pprint

from google.auth import crypt, jwt

logging.basicConfig(level=logging.DEBUG)


# generates a signed JSON Web Token

with open('/usr/local/google/home/ensonic/robco_gob/cloud-robotics/src/bootstrap/robot/robot-credentials.json', 'r') as fh:
    service_account_info = json.load(fh)

signer = crypt.RSASigner.from_service_account_info(service_account_info)

now = int(time.time())
payload = {
    'iat': now,
    # expires after one hour.
    'exp': now + 3600,
    'iss': service_account_info['client_email'],
    # the URL of the target service.
    'target_audience': 'https://registry.endpoints.robco-166608.cloud.goog',
    # Google token endpoints URL, FIXME: use discovery doc
    'aud': 'https://www.googleapis.com/oauth2/v4/token'
}
signed_jwt = jwt.encode(signer, payload)

pprint(signed_jwt)


# send the JWT to Google Token endpoints to request Google ID token

params = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': signed_jwt
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post('https://www.googleapis.com/oauth2/v4/token', data=params, headers=headers)
res = response.json()

pprint(res)

# request

headers = {'Authorization': 'Bearer {}'.format(res['id_token'])}
response = requests.get('https://registry.ensonic.cloudrobotics.com/v1/testauth', headers=headers, verify=False)
response.raise_for_status()
print("-- got response --")
print(response.json())
