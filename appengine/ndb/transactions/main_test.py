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

from testing import AppEngineTest

from . import main


class TestHandlers(AppEngineTest):
    def setUp(self):
        super(TestHandlers, self).setUp()
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()

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
