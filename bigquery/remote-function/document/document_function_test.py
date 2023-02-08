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
from google.cloud import documentai
import pytest

import document_function


# Create a fake "app" for generating test request contexts.
@pytest.fixture(scope="module")
def app() -> flask.Flask:
    return flask.Flask(__name__)


@mock.patch('document_function.urllib.request')
@mock.patch('document_function.documentai')
def test_document_function(
    mock_documentai: object,
    mock_request: object,
    app: flask.Flask
) -> None:
    mock_request.urlopen = mock.Mock(read=mock.Mock(return_value=b'filedata'))
    process_document_mock = mock.Mock(side_effect=[
        documentai.ProcessResponse(
            {'document': {'text': 'apple'}}),
        documentai.ProcessResponse(
            {'document': {'text': 'banana'}})])
    mock_documentai.DocumentProcessorServiceClient = mock.Mock(
        return_value=mock.Mock(process_document=process_document_mock))
    with app.test_request_context(
            json={'calls': [
                ['https://storage.googleapis.com/bucket/apple', 'application/pdf'],
                ['https://storage.googleapis.com/bucket/banana', 'application/pdf']
            ]}):
        response = document_function.document_ocr(flask.request)
        assert response.status_code == 200
        assert len(response.get_json()['replies']) == 2
        assert 'apple' in str(response.get_json()['replies'][0])
        assert 'banana' in str(response.get_json()['replies'][1])


@mock.patch('document_function.urllib.request')
@mock.patch('document_function.documentai')
def test_document_function_error(
    mock_documentai: object,
    mock_request: object,
    app: flask.Flask
) -> None:
    mock_request.urlopen = mock.Mock(read=mock.Mock(return_value=b'filedata'))
    process_document_mock = mock.Mock(side_effect=Exception('API error'))
    mock_documentai.DocumentProcessorServiceClient = mock.Mock(
        return_value=mock.Mock(process_document=process_document_mock))
    with app.test_request_context(
            json={'calls': [
                ['https://storage.googleapis.com/bucket/apple', 'application/pdf'],
                ['https://storage.googleapis.com/bucket/banana', 'application/pdf']
            ]}):
        response = document_function.document_ocr(flask.request)
        assert response.status_code == 400
        assert 'API error' in str(response.get_data())
