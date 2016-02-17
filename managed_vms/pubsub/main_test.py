# Copyright 2015 Google Inc. All Rights Reserved.
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

import base64
import json
import os

import main
from testing import CloudTest


class PubSubTest(CloudTest):
    def setUp(self):
        super(PubSubTest, self).setUp()
        main.app.testing = True
        self.client = main.app.test_client()

    def test_index(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_post_index(self):
        r = self.client.post('/', data={'payload': 'Test payload'})
        self.assertEqual(r.status_code, 200)

    def test_push_endpoint(self):
        url = '/pubsub/push?token=' + os.environ['PUBSUB_VERIFICATION_TOKEN']

        r = self.client.post(
            url,
            data=json.dumps({
                "message": {
                    "data": base64.b64encode(
                        u'Test message'.encode('utf-8')
                    ).decode('utf-8')
                }
            })
        )

        self.assertEqual(r.status_code, 200)

        # Make sure the message is visible on the home page.
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertTrue('Test message' in r.data.decode('utf-8'))

    def test_push_endpoint_errors(self):
        # no token
        r = self.client.post('/pubsub/push')
        self.assertEqual(r.status_code, 400)

        # invalid token
        r = self.client.post('/pubsub/push?token=bad')
        self.assertEqual(r.status_code, 400)
