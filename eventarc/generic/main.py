# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START eventarc_generic_server]
import os

from flask import Flask, request


app = Flask(__name__)
# [END eventarc_generic_server]


# [START eventarc_generic_handler]
@app.route('/', methods=['POST'])
def index():
    print('Event received!')

    print('HEADERS:')
    headers = dict(request.headers)
    headers.pop('Authorization', None)  # do not log authorization header if exists
    print(headers)

    print('BODY:')
    body = dict(request.json)
    print(body)

    resp = {
        "headers": headers,
        "body": body
    }
    return (resp, 200)
# [END eventarc_generic_handler]


# [START eventarc_generic_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END eventarc_generic_server]
