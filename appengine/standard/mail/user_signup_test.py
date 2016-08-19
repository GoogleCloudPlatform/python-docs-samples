# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webtest

import user_signup


def test_user_signup(testbed):
    testbed.init_mail_stub()
    testbed.init_app_identity_stub()
    testbed.init_datastore_v3_stub()
    app = webtest.TestApp(user_signup.app)
    response = app.post('/user/signup', 'email_address=alice@example.com')
    assert response.status_int == 200
    assert 'An email has been sent to alice@example.com.' in response.body

    records = user_signup.UserConfirmationRecord.query().fetch(1)
    response = app.get('/user/confirm?code={}'.format(records[0].key.id()))
    assert response.status_int == 200
    assert 'Confirmed alice@example.com.' in response.body


def test_bad_code(testbed):
    testbed.init_datastore_v3_stub()
    app = webtest.TestApp(user_signup.app)
    response = app.get('/user/confirm?code=garbage', status=404)
    assert response.status_int == 404
