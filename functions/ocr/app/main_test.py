# Copyright 2018, Google, LLC.
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

import concurrent.futures
import json
import os

import mock

import main


bucket = os.environ['CLOUD_STORAGE_BUCKET']
filename = 'menu.jpg'


class TestGCFPyOCRSample():
    @mock.patch.object(main, 'publisher')
    def test_detect_text(self, m):
        mock_future = concurrent.futures.Future()
        mock_future.set_result(True)
        m.publish.return_value = mock_future
        main.detect_text(bucket, filename)

    @mock.patch.object(main, 'detect_text')
    def test_process_image(self, m):
        m.return_value = None
        event = {
            'bucket': bucket,
            'name': filename
        }
        context = {}
        main.process_image(event, context)

    @mock.patch.object(main, 'publisher')
    def test_translate_text(self, m):
        mock_future = concurrent.futures.Future()
        mock_future.set_result(True)
        m.publish.return_value = mock_future

        event = json.dumps({
            'text': 'menu',
            'filename': filename,
            'target_lang': 'es',
            'src_lang': 'en'
        }).encode('utf-8')
        context = {}
        main.translate_text(event, context)

    @mock.patch.object(main, 'storage_client')
    def test_save_result(self, m):
        bucket = m.bucket.return_value
        file = bucket.file.return_value
        file.save.return_value = None

        event = json.dumps({
            'text': 'menu',
            'filename': filename,
            'lang': 'fr',
        }).encode('utf-8')
        context = {}
        main.save_result(event, context)
