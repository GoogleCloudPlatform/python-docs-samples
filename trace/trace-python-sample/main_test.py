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

import os

import main


def test_index():
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    main.app.testing = True
    main.app.config['TRACER'] = main.initialize_tracer(project_id)
    client = main.app.test_client()

    resp = client.get('/index.html')
    assert resp.status_code == 200
    assert 'Tracing requests' in resp.data.decode('utf-8')


def test_redirect():
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    main.app.testing = True
    main.app.config['TRACER'] = main.initialize_tracer(project_id)
    client = main.app.test_client()

    resp = client.get('/')
    assert resp.status_code == 302
    assert '/index.html' in resp.headers.get('location', '')
