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
# [START run_events_pubsub_server_setup]
import os

from flask import Flask, request


required_fields = ['Ce-Id', 'Ce-Source', 'Ce-Type', 'Ce-Specversion']

app = Flask(__name__)
# [END run_events_pubsub_server_setup]


# [START run_events_pubsub_handler]
@app.route('/', methods=['POST'])
def index():
    for field in required_fields:
        if field not in request.headers:
            errmsg = f'Bad Request: missing required header {field}'
            print(errmsg)
            return errmsg, 400

    if 'Ce-Subject' not in request.headers:
        errmsg = 'Bad Request: expected header Ce-Subject'
        print(errmsg)
        return errmsg, 400

    ce_subject = request.headers.get('Ce-Subject')
    print(f'GCS CloudEvent type: {ce_subject}')
    return (f'GCS CloudEvent type: {ce_subject}', 200)
# [END run_events_pubsub_handler]


# [START run_events_pubsub_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END run_events_pubsub_server]
