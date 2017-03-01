# Copyright 2015 Google Inc.
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

"""
Sample Google App Engine application that demonstrates how to use the App
Engine Log Service API to read application logs.
"""

# [START all]
import base64
import datetime
from itertools import islice
from textwrap import dedent
import time

from google.appengine.api.logservice import logservice
import webapp2


def get_logs(offset=None):
    # Logs are read backwards from the given end time. This specifies to read
    # all logs up until now.
    end_time = time.time()

    logs = logservice.fetch(
        end_time=end_time,
        offset=offset,
        minimum_log_level=logservice.LOG_LEVEL_INFO,
        include_app_logs=True)

    return logs


def format_log_entry(entry):
    # Format any application logs that happened during this request.
    logs = []
    for log in entry.app_logs:
        date = datetime.datetime.fromtimestamp(
            log.time).strftime('%D %T UTC')
        logs.append('Date: {}, Message: {}'.format(
            date, log.message))

    # Format the request log and include the application logs.
    date = datetime.datetime.fromtimestamp(
        entry.end_time).strftime('%D %T UTC')

    output = dedent("""
        Date: {}
        IP: {}
        Method: {}
        Resource: {}
        Logs:
    """.format(date, entry.ip, entry.method, entry.resource))

    output += '\n'.join(logs)

    return output


class MainPage(webapp2.RequestHandler):
    def get(self):
        offset = self.request.get('offset', None)

        if offset:
            offset = base64.urlsafe_b64decode(str(offset))

        # Get the logs given the specified offset.
        logs = get_logs(offset=offset)

        # Output the first 10 logs.
        log = None
        for log in islice(logs, 10):
            self.response.write(
                '<pre>{}</pre>'.format(format_log_entry(log)))

            offset = log.offset

        if not log:
            self.response.write('No log entries found.')

        # Add a link to view more log entries.
        elif offset:
            self.response.write(
                '<a href="/?offset={}"">More</a>'.format(
                    base64.urlsafe_b64encode(offset)))


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)

# [END all]
