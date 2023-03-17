# Copyright 2020 Google LLC
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

import main
import os


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert 'Downloaded text matches uploaded text' in r.data.decode('utf-8')

    if os.environ['CLOUD_STORAGE_BUCKET'] is None:
        os.environ['CLOUD_STORAGE_BUCKET'] = "python-docs-samples-tests-public"
        
    bucket_name = os.environ['CLOUD_STORAGE_BUCKET']
        
    blob_name = os.environ.get('BLOB_NAME', 'storage-migration-test-blob')
    assert '    {}/{}'.format(bucket_name, blob_name) in r.data.decode('utf-8')
    assert 'Blob {} deleted.'.format(blob_name) in r.data.decode('utf-8')
