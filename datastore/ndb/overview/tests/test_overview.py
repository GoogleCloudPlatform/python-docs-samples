# Copyright 2015 Google Inc. All rights reserved.
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

import unittest

# from the app main.py
from datastore.ndb.overview import main

from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed

import webapp2


class TestHandlers(unittest.TestCase):
    def setUp(self):
        """Setup the datastore and memcache stub."""
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for
        # use.
        self.testbed.activate()
        # Create a consistency policy that will simulate the High
        # Replication consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_hello(self):
        # Build a request object passing the URI path to be tested.
        # You can also pass headers, query arguments etc.
        request = webapp2.Request.blank('/')
        # Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)
        # self.assertEqual(response.body, 'Hello, world!')
