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

# [START functions_storage_integration_test]
import datetime
import os
import subprocess
import uuid

import requests
from requests.packages.urllib3.util.retry import Retry


def test_print_name():
    filename = str(uuid.uuid4())
    port = 8089  # Each running framework instance needs a unique port

    example_timestamp = datetime.datetime.now().isoformat()
    storage_message = {
        'data': {
            'name': filename,
            'bucket': 'my_bucket',
            'metageneration': '1',
            'timeCreated': example_timestamp,
            'updated': example_timestamp
        }
    }

    process = subprocess.Popen(
      [
        'functions-framework',
        '--target', 'hello_gcs',
        '--signature-type', 'event',
        '--port', str(port)
      ],
      cwd=os.path.dirname(__file__),
      stdout=subprocess.PIPE
    )

    # Send HTTP request simulating Pub/Sub message
    # (GCF translates Pub/Sub messages to HTTP requests internally)
    url = f'http://localhost:{port}/'

    retry_policy = Retry(total=6, backoff_factor=1)
    retry_adapter = requests.adapters.HTTPAdapter(
      max_retries=retry_policy)

    session = requests.Session()
    session.mount(url, retry_adapter)

    response = session.post(url, json=storage_message)

    assert response.status_code == 200

    # Stop the functions framework process
    process.kill()
    process.wait()
    out, err = process.communicate()

    print(out, err, response.content)

    assert f'File: {filename}' in str(out)
# [END functions_storage_integration_test]
