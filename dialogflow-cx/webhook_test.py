# Copyright 2021, Google LLC
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

"""Test webhook"""

import flask
import pytest

from webhook import handle_webhook

# Create a fake 'app' for generating test request contexts.

request = {"fulfillmentInfo": {"tag": "Default Welcome Intent"}}


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_handle_webhook(app):
    with app.test_request_context(json=request):
        res = handle_webhook(flask.request)
        assert "Hello from a GCF Webhook" in str(res)
