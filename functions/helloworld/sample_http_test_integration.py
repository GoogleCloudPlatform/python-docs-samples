# Copyright 2020 Google LLC
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

# [START functions_http_integration_test]
import os
import subprocess
import uuid

import requests
from requests.packages.urllib3.util.retry import Retry


def test_args():
    name = str(uuid.uuid4())
    port = os.getenv('PORT', 8080)  # Each functions framework instance needs a unique port

    process = subprocess.Popen(
      [
        'functions-framework',
        '--target', 'hello_http',
        '--port', str(port)
      ],
      cwd=os.path.dirname(__file__),
      stdout=subprocess.PIPE
    )

    # Send HTTP request simulating Pub/Sub message
    # (GCF translates Pub/Sub messages to HTTP requests internally)
    BASE_URL = f'http://localhost:{port}'

    retry_policy = Retry(total=6, backoff_factor=1)
    retry_adapter = requests.adapters.HTTPAdapter(
      max_retries=retry_policy)

    session = requests.Session()
    session.mount(BASE_URL, retry_adapter)

    name = str(uuid.uuid4())
    res = session.post(
      BASE_URL,
      json={'name': name}
    )
    assert res.text == f'Hello {name}!'

    # Stop the functions framework process
    process.kill()
    process.wait()
# [END functions_http_integration_test]
