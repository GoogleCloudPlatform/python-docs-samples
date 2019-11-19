# Copyright 2019 Google, LLC.
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

from flask import Flask, request
import json
import os
import sys

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']

    # [START run_manual_logging]
    # Uncomment and populate this variable in your code:
    # PROJECT = 'The project ID of your Cloud Run service';

    # Build structured log messages as an object.
    global_log_fields = {}

    # Add log correlation to nest all log messages
    # beneath request log in Log Viewer.
    trace_header = request.headers.get('X-Cloud-Trace-Context')

    if trace_header and PROJECT:
        trace = trace_header.split('/')
        global_log_fields['logging.googleapis.com/trace'] = (
            f"projects/{PROJECT}/traces/{trace[0]}")

    # Complete a structured log entry.
    entry = dict(severity='NOTICE',
                 message='This is the default display field.',
                 # Log viewer accesses 'component' as jsonPayload.component'.
                 component='arbitrary-property',
                 **global_log_fields)

    print(json.dumps(entry))
    # [END run_manual_logging]

    # Flush the stdout to avoid log buffering.
    sys.stdout.flush()

    return 'Hello Logger!'


if __name__ == '__main__':
    PORT = int(os.getenv('PORT')) if os.getenv('PORT') else 8080

    # This is used when running locally. Gunicorn is used to run the
    # application on Cloud Run. See entrypoint in Dockerfile.
    app.run(host='127.0.0.1', port=PORT, debug=True)
