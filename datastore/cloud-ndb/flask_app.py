# Copyright 2019 Google LLC All Rights Reserved.
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

from middleware import ndb_wsgi_middleware

# [START ndb_flask_middleware_usage]
from flask import Flask
# [END ndb_flask_middleware_usage]
from google.cloud import ndb
# [START ndb_flask_middleware_usage]

app = Flask(__name__)
app.wsgi_app = ndb_wsgi_middleware(app.wsgi_app)  # Wrap the app in middleware.
# [END ndb_flask_middleware_usage]


class Book(ndb.Model):
    title = ndb.StringProperty()


client = ndb.Client()


@app.route('/')
def list_books():
    books = Book.query()
    return str([book.to_dict() for book in books])
