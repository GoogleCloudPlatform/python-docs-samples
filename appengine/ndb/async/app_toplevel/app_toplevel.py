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


class Account(ndb.Model):
    view_counter = ndb.IntegerProperty()


class MyRequestHandler(webapp2.RequestHandler):
    @ndb.toplevel
    def get(self):
        acct = Account.get_by_id(users.get_current_user().user_id())
        acct.view_counter += 1
        acct.put_async()  # Ignoring the Future this returns

        # ...read something else from Datastore...

        self.response.out.write('Content of the page')


# This is actually redundant, since the `get` decorator already handles it, but
# for demonstration purposes, you can also make the entire app toplevel with
# the following.
app = ndb.toplevel(webapp2.WSGIApplication([('/', MyRequestHandler)]))
