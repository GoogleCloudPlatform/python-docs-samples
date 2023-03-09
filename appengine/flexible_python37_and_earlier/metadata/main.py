# Copyright 2015 Google LLC.
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

import logging

from flask import Flask
import requests


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


# [START gae_flex_metadata]
METADATA_NETWORK_INTERFACE_URL = \
    ('http://metadata/computeMetadata/v1/instance/network-interfaces/0/'
     'access-configs/0/external-ip')


def get_external_ip():
    """Gets the instance's external IP address from the Compute Engine metadata
    server. If the metadata server is unavailable, it assumes that the
    application is running locally.
    """
    try:
        r = requests.get(
            METADATA_NETWORK_INTERFACE_URL,
            headers={'Metadata-Flavor': 'Google'},
            timeout=2)
        return r.text
    except requests.RequestException:
        logging.info('Metadata server could not be reached, assuming local.')
        return 'localhost'
# [END gae_flex_metadata]


@app.route('/')
def index():
    # Websocket connections must be made directly to this instance, so the
    # external IP address of this instance is needed.
    external_ip = get_external_ip()
    return 'External IP: {}'.format(external_ip)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
