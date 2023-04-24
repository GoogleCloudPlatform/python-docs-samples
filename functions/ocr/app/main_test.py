# Copyright 2018 Google, LLC.
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

import base64
import concurrent.futures
import json
from unittest import mock

import main


class TestGCFPyOCRSample():
    @mock.patch.object(main, 'publisher')
    @mock.patch.object(main, 'translate_client')
    @mock.patch.object(main, 'vision_client')
    def test_detect_text(self, mock_vision_client, mock_translate_client,
                         mock_publisher):
        mock_annotation = mock.MagicMock()
        mock_annotation.description = 'sample text'
        mock_annotations = mock.MagicMock()
        mock_annotations.text_annotations = [mock_annotation]
        mock_vision_client.text_detection.return_value = mock_annotations

        mock_translate_client.detect_language.return_value = {'language': 'en'}

        mock_future = concurrent.futures.Future()
        mock_future.set_result(True)
        mock_publisher.publish.return_value = mock_future

        main.detect_text('sample-bucket', 'sample-file')

    @mock.patch.object(main, 'detect_text')
    def test_process_image(self, m):
        m.return_value = None
        event = {
            'bucket': 'sample-bucket',
            'name': 'sample-file'
        }
        context = {}
        main.process_image(event, context)

    @mock.patch.object(main, 'publisher')
    @mock.patch.object(main, 'translate_client')
    def test_translate_text(self, mock_translate_client, mock_publisher):
        mock_translate_client.translate.return_value = {'translatedText': ''}

        mock_future = concurrent.futures.Future()
        mock_future.set_result(True)
        mock_publisher.publish.return_value = mock_future

        data = base64.b64encode(json.dumps({
            'text': 'menu',
            'filename': 'sample-file',
            'lang': 'es',
            'src_lang': 'en'
        }).encode('utf-8'))
        event = {
            'data': data
        }
        context = {}
        main.translate_text(event, context)

    @mock.patch.object(main, 'storage_client')
    def test_save_result(self, m):
        bucket = m.bucket.return_value
        file = bucket.file.return_value
        file.save.return_value = None

        data = base64.b64encode(json.dumps({
            'text': 'menu',
            'filename': 'sample-file',
            'lang': 'fr',
        }).encode('utf-8'))
        event = {
            'data': data
        }
        context = {}
        main.save_result(event, context)
