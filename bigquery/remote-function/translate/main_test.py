# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from unittest import mock


import flask
from google.cloud import translate
import pytest


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope='module')
def app() -> flask.Flask:
  return flask.Flask(__name__)


@mock.patch('main.translate_client')
def test_main(mock_translate: object, app: flask.Flask) -> None:
  import main

  mock_translate.translate_text.return_value = translate.TranslateTextResponse(
      {
          'translations': [
              {'translated_text': 'Hola'},
              {'translated_text': 'Mundo'},
          ]
      }
  )

  with app.test_request_context(
      json={
          'caller': (
              '//bigquery.googleapis.com/projects/test-project/jobs/job-id'
          ),
          'userDefinedContext': {},
          'calls': [
              ['Hello'],
              ['World'],
          ],
      }
  ):
    response = main.handle_translation(flask.request)
    assert response.status_code == 200
    assert response.get_json()['replies'] == ['Hola', 'Mundo']
