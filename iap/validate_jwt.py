# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Sample showing how to validate the Identity-Aware Proxy (IAP) JWT.

This code should be used by applications in Google Compute Engine-based
environments (such as Google App Engine flexible environment, Google
Compute Engine, or Google Container Engine) to provide an extra layer
of assurance that a request was authorized by IAP.

For applications running in the App Engine standard environment, use
App Engine's Users API instead.
"""
# [START iap_validate_jwt]
import jwt
import requests


def validate_iap_jwt(cloud_project_number, iap_jwt,
                     app_engine_project_id=None,
                     compute_engine_backend_service_id=None):
    """Validate a JWT passed to your application by Identity-Aware Proxy.

    One and only of of (app_engine_project_id, compute_engine_backend_service_id)
    must be set.

    Args:
      cloud_project_number: The project *number* for your Google Cloud project.
          This is returned by 'gcloud projects describe $PROJECT_ID', or
          in the Project Info card in Cloud Console.
      iap_jwt: The contents of the X-Goog-IAP-JWT-Assertion header.
      app_engine_project_id: For App Engine resources, this must be set to
          your cloud project ID.
      compute_engine_backend_service_id: For Compute Engine and Container Engine
          resources this must be set to the ID of the backend service used to
          access the application. See
          https://cloud.google.com/iap/docs/signed-headers-howto for details on
          how to get this value.

    Returns:
      (user_id, user_email, error_str).
    """
    if not (bool(app_engine_project_id) ^ bool(compute_engine_backend_service_id)):
        raise ValueError('One and only of of app_engine_project_id, '
                         'compute_engine_backend_service_id must be specified.')

    if app_engine_project_id:
        expected_audience = '/projects/{}/apps/{}'.format(
            cloud_project_number, app_engine_project_id)
    else:
        expected_audience = '/projects/{}/global/backendServices/{}'.format(
            cloud_project_number, compute_engine_backend_service_id)
        
    try:
        key_id = jwt.get_unverified_header(iap_jwt).get('kid')
        if not key_id:
            return (None, None, '**ERROR: no key ID**')
        key = get_iap_key(key_id)
        decoded_jwt = jwt.decode(
            iap_jwt, key,
            algorithms=['ES256'],
            audience=expected_audience)
        return (decoded_jwt['sub'], decoded_jwt['email'], '')
    except (jwt.exceptions.InvalidTokenError,
            requests.exceptions.RequestException) as e:
        return (None, None, '**ERROR: JWT validation error {}**'.format(e))


def get_iap_key(key_id):
    """Retrieves a public key from the list published by Identity-Aware Proxy,
    re-fetching the key file if necessary.
    """
    key_cache = get_iap_key.key_cache
    key = key_cache.get(key_id)
    if not key:
        # Re-fetch the key file.
        resp = requests.get(
            'https://www.gstatic.com/iap/verify/public_key')
        if resp.status_code != 200:
            raise Exception(
                'Unable to fetch IAP keys: {} / {} / {}'.format(
                    resp.status_code, resp.headers, resp.text))
        key_cache = resp.json()
        get_iap_key.key_cache = key_cache
        key = key_cache.get(key_id)
        if not key:
            raise Exception('Key {!r} not found'.format(key_id))
    return key


# Used to cache the Identity-Aware Proxy public keys.  This code only
# refetches the file when a JWT is signed with a key not present in
# this cache.
get_iap_key.key_cache = {}
# [END iap_validate_jwt]
