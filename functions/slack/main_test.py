# Copyright 2018 Google LLC
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

import json
import os
import time
from unittest import mock

import googleapiclient.discovery
import pytest
from slack.signature import SignatureVerifier

import main


kg_search = googleapiclient.discovery.build(
    'kgsearch', 'v1',
    developerKey=os.environ['KG_API_KEY'])
example_response = kg_search.entities().search(query='lion', limit=1).execute()


class Request:
    def __init__(self, data='', headers={}):
        self.data = data
        self.headers = headers

    def get_data(self):
        return self.data


class TestGCFPySlackSample:
    def test_verify_signature_request_form_empty(self):
        with pytest.raises(ValueError):
            request = Request()
            main.verify_signature(request)

    def test_verify_signature_token_incorrect(self):
        with pytest.raises(ValueError):
            request = Request(headers={'X-Slack-Signature': '12345'})
            main.verify_signature(request)

    def test_verify_web_hook_valid_request(self):
        request = Request()
        request.body = ''

        now = str(int(time.time()))

        verifier = SignatureVerifier(os.environ['SLACK_SECRET'])
        test_signature = verifier.generate_signature(
            timestamp=now,
            body=''
        )

        request.headers = {
            'X-Slack-Request-Timestamp': now,
            'X-Slack-Signature': test_signature
        }
        main.verify_signature(request)

    def test_format_slack_message(self):
        message = main.format_slack_message('lion', example_response)

        # Just make sure there's a result.
        assert 'title' in message['attachments'][0]
        assert message['attachments'][0]['color'] == '#3367d6'

    def test_make_search_request(self):
        with mock.patch.object(main, 'kgsearch'):
            entities = main.kgsearch.entities.return_value
            search = entities.search.return_value
            search.execute.return_value = example_response
            message = main.make_search_request('lion')
        # Just make sure there's a result.
        assert 'title' in message['attachments'][0]
        assert message['attachments'][0]['color'] == '#3367d6'

    def test_kg_search(self):
        with mock.patch.object(main, 'kgsearch'):
            entities = main.kgsearch.entities.return_value
            search = entities.search.return_value
            search.execute.return_value = example_response

            request = Request()
            request.form = {
                'text': 'lion'
            }
            request.data = json.dumps(request.form)

            now = str(int(time.time()))
            verifier = SignatureVerifier(os.environ['SLACK_SECRET'])
            test_signature = verifier.generate_signature(
                timestamp=now,
                body=request.data
            )

            request.method = 'POST'
            request.headers = {
                'X-Slack-Request-Timestamp': now,
                'X-Slack-Signature': test_signature
            }

            with mock.patch('main.jsonify', side_effect=json.dumps):
                response = main.kg_search(request)

        assert 'lion' in response.lower()
        assert 'color' in response.lower()
