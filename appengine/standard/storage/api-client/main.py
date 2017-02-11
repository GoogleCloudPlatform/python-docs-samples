#!/usr/bin/env python

# Copyright 2015 Google Inc.
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
Sample Google App Engine application that lists the objects in a Google Cloud
Storage bucket.

For more information about Cloud Storage, see README.md in /storage.
For more information about Google App Engine, see README.md in /appengine.
"""

import json
import StringIO

from googleapiclient import discovery
from googleapiclient import http
from oauth2client.client import GoogleCredentials
import webapp2


# The bucket that will be used to list objects.
BUCKET_NAME = '<your-bucket-name>'

# The filename for an object to be uploaded.
FILE_NAME = 'storage-api-client-sample-file.txt'

credentials = GoogleCredentials.get_application_default()
storage = discovery.build('storage', 'v1', credentials=credentials)


class MainPage(webapp2.RequestHandler):
    def upload_object(self, bucket, filename):
        body = {
            'name': FILE_NAME,
        }
        req = storage.objects().insert(
            bucket=bucket, body=body, media_body=http.MediaIoBaseUpload(
                filename, 'application/octet-stream'))
        resp = req.execute()
        return resp

    def delete_object(self, bucket, filename):
        req = storage.objects().delete(bucket=bucket, object=filename)
        resp = req.execute()
        return resp

    def get(self):
        string_io_file = StringIO.StringIO()
        string_io_file.write('Hello World!')
        self.upload_object(BUCKET_NAME, string_io_file)

        response = storage.objects().list(bucket=BUCKET_NAME).execute()
        self.response.write(
            '<h3>Objects.list raw response:</h3>'
            '<pre>{}</pre>'.format(
                json.dumps(response, sort_keys=True, indent=2)))

        self.delete_object(BUCKET_NAME, FILE_NAME)


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
