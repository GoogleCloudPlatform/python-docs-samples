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

# from the app main.py
from appengine.images import main
import mock
from tests import DatastoreTestbedCase

import webapp2


class TestHandlers(DatastoreTestbedCase):
    def setUp(self):
        super(TestHandlers, self).setUp()

        # Workaround for other tests clobbering our Greeting model.
        reload(main)

    def test_get(self):
        # Build a request object passing the URI path to be tested.
        # You can also pass headers, query arguments etc.
        request = webapp2.Request.blank('/')
        # Get a response for that request.
        response = request.get_response(main.app)

        # Let's check if the response is correct.
        self.assertEqual(response.status_int, 200)

    @mock.patch('appengine.images.main.images')
    def test_post(self, mock_images):
        mock_images.resize.return_value = 'asdf'
        request = webapp2.Request.blank(
            '/sign',
            POST={'content': 'asdf'},
            )
        response = request.get_response(main.app)
        mock_images.resize.assert_called_once_with(mock.ANY, 32, 32)

        # Correct response is a redirect
        self.assertEqual(response.status_int, 302)

    def test_img(self):
        greeting = main.Greeting(
            parent=main.guestbook_key('default_guestbook'),
            id=123,
        )
        greeting.author = 'asdf'
        greeting.content = 'asdf'
        greeting.put()

        request = webapp2.Request.blank(
            '/img?img_id=%s' % greeting.key.urlsafe()
        )
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)

    def test_img_missing(self):
        # Bogus image id, should get error
        request = webapp2.Request.blank('/img?img_id=123')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 500)

    @mock.patch('appengine.images.main.images')
    def test_post_and_get(self, mock_images):
        mock_images.resize.return_value = 'asdf'
        request = webapp2.Request.blank(
            '/sign',
            POST={'content': 'asdf'},
            )
        response = request.get_response(main.app)

        request = webapp2.Request.blank('/')
        response = request.get_response(main.app)

        self.assertEqual(response.status_int, 200)
