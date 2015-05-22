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
from datastore.ndb.transactions import main

from google.appengine.datastore import datastore_stub_util
from google.appengine.ext import testbed



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

        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

    def tearDown(self):
        self.testbed.deactivate()

    def test_hello(self):
        rv = self.app.get('/')
        self.assertIn('Permenant note page', rv.data)
        self.assertEqual(rv.status, '200 OK')

    def test_post(self):
        rv = self.app.post('/add', data=dict(
            note_title='Title',
            note_text='Text'
        ), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')

    def test_post2(self):
        rv = self.app.post('/add', data=dict(
            note_title='Title2',
            note_text='Text'
        ), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')

    def test_post3(self):
        rv = self.app.post('/add', data=dict(
            note_title='Title3',
            note_text='Text'
        ), follow_redirects=True)
        self.assertEqual(rv.status, '200 OK')

    def test_there(self):
        rv = self.app.post('/add', data=dict(
            note_title='Title',
            note_text='New'
        ), follow_redirects=True)
        rv = self.app.post('/add', data=dict(
            note_title='Title',
            note_text='There'
        ), follow_redirects=True)
        self.assertIn('Already there', rv.data)
        self.assertEqual(rv.status, '200 OK')
