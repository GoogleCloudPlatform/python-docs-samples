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

import cgi

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb
import webapp2


class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


class MainPage(webapp2.RequestHandler):
    GREETINGS_PER_PAGE = 20

    def get(self):
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key('Book', guestbook_name or '*notitle*')
        greetings = Greeting.query_book(ancestor_key).fetch(
            self.GREETINGS_PER_PAGE)

        self.response.out.write('<html><body>')

        for greeting in greetings:
            self.response.out.write(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write('</body></html>')


class List(webapp2.RequestHandler):
    GREETINGS_PER_PAGE = 10

    def get(self):
        """Handles requests like /list?cursor=1234567."""
        cursor = Cursor(urlsafe=self.request.get('cursor'))
        greets, next_cursor, more = Greeting.query().fetch_page(
            self.GREETINGS_PER_PAGE, start_cursor=cursor)

        self.response.out.write('<html><body>')

        for greeting in greets:
            self.response.out.write(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        if more and next_cursor:
            self.response.out.write('<a href="/list?cursor=%s">More...</a>' %
                                    next_cursor.urlsafe())

        self.response.out.write('</body></html>')


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/list', List),
], debug=True)
