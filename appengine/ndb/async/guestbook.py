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

from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2


class Guestbook(ndb.Model):
    content = ndb.StringProperty()
    post_date = ndb.DateTimeProperty(auto_now_add=True)


class Account(ndb.Model):
    email = ndb.StringProperty()
    nickname = ndb.StringProperty()

    def nick(self):
        return self.nickname or self.email  # Whichever is non-empty


class Message(ndb.Model):
    text = ndb.StringProperty()
    when = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.KeyProperty(kind=Account)  # references Account


class MainPage(webapp2.RequestHandler):
    def get(self):
        if self.request.path == '/guestbook':
            if self.request.get('async'):
                self.get_guestbook_async()
            else:
                self.get_guestbook_sync()
        elif self.request.path == '/messages':
            if self.request.get('async'):
                self.get_messages_async()
            else:
                self.get_messages_sync()

    def get_guestbook_sync(self):
        uid = users.get_current_user().user_id()
        acct = Account.get_by_id(uid)  # I/O action 1
        qry = Guestbook.query().order(-Guestbook.post_date)
        recent_entries = qry.fetch(10)  # I/O action 2

        # ...render HTML based on this data...
        self.response.out.write('<html><body>{}</body></html>'.format(''.join(
            '<p>{}</p>'.format(entry.content) for entry in recent_entries)))

        return acct, qry

    def get_guestbook_async(self):
        uid = users.get_current_user().user_id()
        acct_future = Account.get_by_id_async(uid)  # Start I/O action #1
        qry = Guestbook.query().order(-Guestbook.post_date)
        recent_entries_future = qry.fetch_async(10)  # Start I/O action #2
        acct = acct_future.get_result()  # Complete #1
        recent_entries = recent_entries_future.get_result()  # Complete #2

        # ...render HTML based on this data...
        self.response.out.write('<html><body>{}</body></html>'.format(''.join(
            '<p>{}</p>'.format(entry.content) for entry in recent_entries)))

        return acct, recent_entries

    def get_messages_sync(self):
        qry = Message.query().order(-Message.when)
        for msg in qry.fetch(20):
            acct = msg.author.get()
            self.response.out.write(
                '<p>On {}, {} wrote:'.format(msg.when, acct.nick()))
            self.response.out.write('<p>{}'.format(msg.text))

    def get_messages_async(self):
        @ndb.tasklet
        def callback(msg):
            acct = yield msg.author.get_async()
            raise ndb.Return('On {}, {} wrote:\n{}'.format(
                msg.when, acct.nick(), msg.text))

        qry = Message.query().order(-Message.when)
        outputs = qry.map(callback, limit=20)
        for output in outputs:
            self.response.out.write('<p>{}</p>'.format(output))


app = webapp2.WSGIApplication([
    ('/.*', MainPage),
], debug=True)
