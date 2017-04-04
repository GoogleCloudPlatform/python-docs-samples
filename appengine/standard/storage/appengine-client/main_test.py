# Copyright 2017 Google Inc. All rights reserved.
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

import webtest

import main

PROJECT = os.environ['GCLOUD_PROJECT']


def test_get(testbed):
    main.BUCKET_NAME = PROJECT
    app = webtest.TestApp(main.app)

    response = app.get('/')

    assert response.status_int == 200
    assert 'The demo ran successfully!' in response.body
