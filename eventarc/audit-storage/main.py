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

# [START eventarc_gcs_server]
import os

import cloudevents.exceptions as cloud_exceptions
from cloudevents.http import from_http

from flask import Flask, request


required_fields = ['Ce-Id', 'Ce-Source', 'Ce-Type', 'Ce-Specversion']
app = Flask(__name__)
# [END eventarc_gcs_server]


# [START eventarc_gcs_handler]
@app.route('/', methods=['POST'])
def index():
    # Create CloudEvent from HTTP headers and body
    try:
        event = from_http(request.headers, request.get_data())

    except cloud_exceptions.MissingRequiredFields as e:
        print(f"cloudevents.exceptions.MissingRequiredFields: {e}")
        return "Failed to find all required cloudevent fields. ", 400

    except cloud_exceptions.InvalidStructuredJSON as e:
        print(f"cloudevents.exceptions.InvalidStructuredJSON: {e}")
        return "Could not deserialize the payload as JSON. ", 400

    except cloud_exceptions.InvalidRequiredFields as e:
        print(f"cloudevents.exceptions.InvalidRequiredFields: {e}")
        return "Request contained invalid required cloudevent fields. ", 400

    if 'subject' not in event:
        errmsg = 'Bad Request: expected header ce-subject'
        print(errmsg)
        return errmsg, 400

    print(f"Detected change in GCS bucket: {event['subject']}")
    return (f"Detected change in GCS bucket: {event['subject']}", 200)
# [END eventarc_gcs_handler]


# [START eventarc_gcs_server]
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# [END eventarc_gcs_server]
