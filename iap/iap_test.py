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

"""Test script for Identity-Aware Proxy code samples."""

from gcp_devrel.testing.flaky import flaky

import make_iap_request
import validate_jwt

# The hostname of an application protected by Identity-Aware Proxy.
# When a request is made to https://${JWT_REFLECT_HOSTNAME}/, the
# application should respond with the value of the
# X-Goog-Authenticated-User-JWT (and nothing else.) The
# app_engine_app/ subdirectory contains an App Engine standard
# environment app that does this.
# The project must have the service account used by this test added as a
# member of the project.
REFLECT_SERVICE_HOSTNAME = 'gcp-devrel-iap-reflect.appspot.com'
IAP_CLIENT_ID = ('320431926067-ldm6839p8l2sei41nlsfc632l4d0v2u1'
                 '.apps.googleusercontent.com')
IAP_APP_ID = 'gcp-devrel-iap-reflect'
IAP_PROJECT_NUMBER = '320431926067'


@flaky
def test_main(capsys):
    # JWTs are obtained by IAP-protected applications whenever an
    # end-user makes a request.  We've set up an app that echoes back
    # the JWT in order to expose it to this test.  Thus, this test
    # exercises both make_iap_request and validate_jwt.
    iap_jwt = make_iap_request.make_iap_request(
        'https://{}/'.format(REFLECT_SERVICE_HOSTNAME),
        IAP_CLIENT_ID)
    iap_jwt = iap_jwt.split(': ').pop()
    jwt_validation_result = validate_jwt.validate_iap_jwt_from_app_engine(
        iap_jwt, IAP_PROJECT_NUMBER, IAP_APP_ID)

    assert jwt_validation_result[0]
    assert jwt_validation_result[1]
    assert not jwt_validation_result[2]
