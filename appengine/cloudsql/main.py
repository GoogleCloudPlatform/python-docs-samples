# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

import MySQLdb
import webapp2


class IndexPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            db = MySQLdb.connect(
                unix_socket='/cloudsql/my_project:my_instance',
                user='root')
        else:
            db = MySQLdb.connect(host='localhost', user='root')

        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')
        for r in cursor.fetchall():
            self.response.write('%s\n' % str(r))


app = webapp2.WSGIApplication([
    ('/', IndexPage),
], debug=True)
