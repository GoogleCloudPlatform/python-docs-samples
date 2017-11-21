# Copyright Google Inc.
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
Sample application that demonstrates refreshing a session when using
Identity Aware Proxy. This application is for App Engine Standard.
"""

import os

from google.appengine.api import users
import jinja2
import webapp2


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logged_in = True
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            login_url = None
        else:
            logged_in = False
            nickname = None
            logout_url = None
            login_url = users.create_login_url('/')
        template_values = {
            'logged_in': logged_in,
            'nickname': nickname,
            'logout_url': logout_url,
            'login_url': login_url,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class AdminPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                self.response.write('You are an administrator.')
            else:
                self.response.write('You are not an administrator.')
        else:
            self.response.write('You are not logged in.')


# Fake status
class StatusPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Success')


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
    ('/status', StatusPage),
], debug=True)
