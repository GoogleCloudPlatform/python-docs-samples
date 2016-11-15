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
    def get(self):
        acct = Account.get_by_id(users.get_current_user().user_id())
        acct.view_counter += 1
        acct.put()

        # ...read something else from Datastore...

        self.response.out.write('Content of the page')


app = webapp2.WSGIApplication([('/', MyRequestHandler)])
