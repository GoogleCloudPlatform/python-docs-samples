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
Compute Engine, Google Container Engine, Google App Engine) to provide
an extra layer of assurance that a request was authorized by IAP.
"""
# [START iap_validate_jwt]
from google.oauth2 import id_token
from google.auth.transport import requests


def validate_iap_jwt(iap_jwt, cloud_project_number,
                                         backend_service_id):
    """Validate an IAP JWT.

    Args:
      iap_jwt: The contents of the X-Goog-IAP-JWT-Assertion header.
      cloud_project_number: The project *number* for your Google Cloud project.
          This is returned by 'gcloud projects describe $PROJECT_ID', or
          in the Project Info card in Cloud Console.
      backend_service_id: The ID of the backend service used to access the
          application. See
          https://cloud.google.com/iap/docs/signed-headers-howto
          for details on how to get this value.

    Returns:
      (user_id, user_email, error_str).
    """
    expected_audience = '/projects/{}/global/backendServices/{}'.format(
        cloud_project_number, backend_service_id)

    try:
        decoded_jwt = id_token.verify_oauth2_token(
            token, requests.Request(), expected_audience)
        return (decoded_jwt['sub'], decoded_jwt['email'], '')
    except Exception as e:
        return (None, None, '**ERROR: JWT validation error {}**'.format(e))

# [END iap_validate_jwt]
