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

import main
import flask
import pytest

# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app() -> flask.Flask:
    return flask.Flask(__name__)

def test_main(app):
    with app.test_request_context():
        response = main.stream_big_query_output(flask.request)
        assert response.is_streamed == True
        assert response.status_code == 200
