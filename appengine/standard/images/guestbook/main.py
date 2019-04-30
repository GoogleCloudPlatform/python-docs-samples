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

"""
Sample application that demonstrates how to use the App Engine Images API.

For more information, see README.md.
"""

# [START all]

import cgi
import urllib

# [START import_images]
from google.appengine.api import images
# [END import_images]
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2


# [START model]
class Greeting(ndb.Model):
    """Models a Guestbook entry with an author, content, avatar, and date."""
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    avatar = ndb.BlobProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END model]


def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with name."""
    return ndb.Key('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')

        greetings = Greeting.query(
            ancestor=guestbook_key(guestbook_name)) \
            .order(-Greeting.date) \
            .fetch(10)

        for greeting in greetings:
            if greeting.author:
                self.response.out.write(
                    '<b>%s</b> wrote:' % greeting.author)
            else:
                self.response.out.write('An anonymous person wrote:')
            # [START display_image]
            self.response.out.write('<div><img src="/img?img_id=%s"></img>' %
                                    greeting.key.urlsafe())
            self.response.out.write('<blockquote>%s</blockquote></div>' %
                                    cgi.escape(greeting.content))
            # [END display_image]

        # [START form]
        self.response.out.write("""
              <form action="/sign?%s"
                    enctype="multipart/form-data"
                    method="post">
                <div>
                  <textarea name="content" rows="3" cols="60"></textarea>
                </div>
                <div><label>Avatar:</label></div>
                <div><input type="file" name="img"/></div>
                <div><input type="submit" value="Sign Guestbook"></div>
              </form>
              <hr>
              <form>Guestbook name: <input value="%s" name="guestbook_name">
              <input type="submit" value="switch"></form>
            </body>
          </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                        cgi.escape(guestbook_name)))
        # [END form]


# [START image_handler]
class Image(webapp2.RequestHandler):
    def get(self):
        greeting_key = ndb.Key(urlsafe=self.request.get('img_id'))
        greeting = greeting_key.get()
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')
# [END image_handler]


# [START sign_handler]
class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = users.get_current_user().nickname()

        greeting.content = self.request.get('content')

        # [START sign_handler_1]
        avatar = self.request.get('img')
        # [END sign_handler_1]
        # [START transform]
        avatar = images.resize(avatar, 32, 32)
        # [END transform]
        # [START sign_handler_2]
        greeting.avatar = avatar
        greeting.put()
        # [END sign_handler_1]

        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))
# [END sign_handler]


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/img', Image),
                               ('/sign', Guestbook)],
                              debug=True)
# [END all]
