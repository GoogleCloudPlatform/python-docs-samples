# Copyright 2022 Google LLC
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

import os
import flask
from requests import Response
import pytest

import main


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_functions_log_http_should_print_message(app, capsys):
    # Mimick the Cloud Run / GCFv2 environment to force handler to print to stdout 
    os.environ['K_SERVICE'] = 'test-service-name'
    os.environ['K_REVISION'] = 'test-revision-name'
    os.environ['K_CONFIGURATION'] = 'test-config-name'
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    mock_trace_value = 'abcdef'
    expected = {
        'severity': 'INFO',
        'component': 'arbitrary-property',
        'logging.googleapis.com/trace': f"projects/{project_id}/traces/{ mock_trace_value}",
    }
    # Force trace with trace header
    with app.test_request_context(headers={'x-cloud-trace-context': f"{mock_trace_value}/2;o=1"}):
        response = main.structured_logging(flask.request)
        out, err = capsys.readouterr()
        print(err)
        assert "Hello, world!" in err
        assert expected['severity'] in err
        assert expected['component'] in err
        assert expected['logging.googleapis.com/trace'] in err
