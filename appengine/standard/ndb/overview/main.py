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

"""Cloud Datastore NDB API guestbook sample.

This sample is used on this page:
    https://cloud.google.com/appengine/docs/python/ndb/

For more information, see README.md
"""

# [START all]
import cgi
import textwrap
import urllib

from google.appengine.ext import ndb

import webapp2


# [START greeting]
class Greeting(ndb.Model):
    """Models an individual Guestbook entry with content and date."""
    content = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]

# [START query]
    @classmethod
    def query_book(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        guestbook_name = self.request.get('guestbook_name')
        ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
        greetings = Greeting.query_book(ancestor_key).fetch(20)
# [END query]

        greeting_blockquotes = []
        for greeting in greetings:
            greeting_blockquotes.append(
                '<blockquote>%s</blockquote>' % cgi.escape(greeting.content))

        self.response.out.write(textwrap.dedent("""\
            <html>
              <body>
                {blockquotes}
                <form action="/sign?{sign}" method="post">
                  <div>
                    <textarea name="content" rows="3" cols="60">
                    </textarea>
                  </div>
                  <div>
                    <input type="submit" value="Sign Guestbook">
                  </div>
                </form>
                <hr>
                <form>
                  Guestbook name:
                    <input value="{guestbook_name}" name="guestbook_name">
                    <input type="submit" value="switch">
                </form>
              </body>
            </html>""").format(
                blockquotes='\n'.join(greeting_blockquotes),
                sign=urllib.urlencode({'guestbook_name': guestbook_name}),
                guestbook_name=cgi.escape(guestbook_name)))


# [START submit]
class SubmitForm(webapp2.RequestHandler):
    def post(self):
        # We set the parent key on each 'Greeting' to ensure each guestbook's
        # greetings are in the same entity group.
        guestbook_name = self.request.get('guestbook_name')
        greeting = Greeting(parent=ndb.Key("Book",
                                           guestbook_name or "*notitle*"),
                            content=self.request.get('content'))
        greeting.put()
# [END submit]
        self.redirect('/?' + urllib.urlencode(
            {'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', SubmitForm)
])
# [END all]
