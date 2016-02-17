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

import main
import mock
from testing import AppEngineTest
import webtest


class TestHandlers(AppEngineTest):
    def setUp(self):
        super(TestHandlers, self).setUp()
        self.app = webtest.TestApp(main.app)

    def test_get(self):
        main.Greeting(
            parent=main.guestbook_key('default_guestbook'),
            author='123',
            content='abc'
        ).put()

        response = self.app.get('/')

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    @mock.patch('main.images')
    def test_post(self, mock_images):
        mock_images.resize.return_value = 'asdf'

        response = self.app.post('/sign', {'content': 'asdf'})
        mock_images.resize.assert_called_once_with(mock.ANY, 32, 32)

        # Correct response is a redirect
        self.assertEqual(response.status_int, 302)

    def test_img(self):
        greeting = main.Greeting(
            parent=main.guestbook_key('default_guestbook'),
            id=123
        )
        greeting.author = 'asdf'
        greeting.content = 'asdf'
        greeting.avatar = b'123'
        greeting.put()

        response = self.app.get('/img?img_id=%s' % greeting.key.urlsafe())

        self.assertEqual(response.status_int, 200)

    def test_img_missing(self):
        # Bogus image id, should get error
        self.app.get('/img?img_id=123', status=500)

    @mock.patch('main.images')
    def test_post_and_get(self, mock_images):
        mock_images.resize.return_value = 'asdf'

        self.app.post('/sign', {'content': 'asdf'})
        response = self.app.get('/')

        self.assertEqual(response.status_int, 200)
