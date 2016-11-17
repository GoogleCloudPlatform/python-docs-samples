# Copyright 2016 Google Inc. All Rights Reserved.
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
    main.app.testing = True
    client = main.app.test_client()
    test_path = os.path.dirname(os.path.realpath(__file__))
    asset_path = os.path.join(
        test_path, 'assets/resized_google_logo.jpg')
    fixtured_path = os.path.join(
        test_path, 'fixtures/assets/resized_google_logo.jpg')
    try:
        os.remove(asset_path)
    except OSError:
        pass  # if doesn't exist
    r = client.get('/')

    assert os.path.isfile(fixtured_path)
    assert r.status_code == 200
