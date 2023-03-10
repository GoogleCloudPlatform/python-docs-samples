# Copyright 2023 Google LLC
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

import json
import os

import flask
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_functions_log_http_should_print_message(app, capsys):
    # Mimic the Cloud Run / GCFv2 environment to force handler to print to stdout
    os.environ['K_SERVICE'] = 'test-service-name'
    os.environ['K_REVISION'] = 'test-revision-name'
    os.environ['K_CONFIGURATION'] = 'test-config-name'
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    mock_trace = 'abcdef'
    mock_span = '2'
    expected = {
        'message': 'Hello, world!',
        'severity': 'INFO',
        'component': 'arbitrary-property',
        'logging.googleapis.com/trace': f"projects/{project_id}/traces/{mock_trace}",
        'logging.googleapis.com/spanId': mock_span
    }
    # Force trace with trace header
    with app.test_request_context(headers={'x-cloud-trace-context': f"{mock_trace}/{mock_span};o=1"}):
        main.structured_logging(flask.request)
        _, err = capsys.readouterr()

        # In some situations, the library adds information before the first
        # intended line. Use the next line in that case.
        err_lines = err.splitlines()
        if len(err_lines) > 1:
            err = err_lines[1]

        output_json = json.loads(err.splitlines()[0])
        for (key, value) in expected.items():
            assert value == output_json[key]
