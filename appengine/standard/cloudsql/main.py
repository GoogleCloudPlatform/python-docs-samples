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

"""
Sample App Engine application demonstrating how to connect to Google Cloud SQL
using App Engine's native unix socket.

For more information, see the README.md.
"""

# [START all]

import os

import MySQLdb
import webapp2


CLOUDSQL_PROJECT = '<your-project-id>'
CLOUDSQL_INSTANCE = '<your-cloud-sql-instance>'


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        # When running on Google App Engine, use the special unix socket
        # to connect to Cloud SQL.
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            db = MySQLdb.connect(
                unix_socket='/cloudsql/{}:{}'.format(
                    CLOUDSQL_PROJECT,
                    CLOUDSQL_INSTANCE),
                user='root')
        # When running locally, you can either connect to a local running
        # MySQL instance, or connect to your Cloud SQL instance over TCP.
        else:
            db = MySQLdb.connect(host='localhost', user='root')

        cursor = db.cursor()
        cursor.execute('SHOW VARIABLES')

        for r in cursor.fetchall():
            self.response.write('{}\n'.format(r))


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

# [END all]
