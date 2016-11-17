# Copyright 2015 Google Inc. All Rights Reserved.
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

import pytest

try:
    import main
except ImportError:
    main = None


@pytest.mark.skipif(
    not main,
    reason='pylibmc not installed.')
def test_index():
    try:
        main.memcache_client.set('counter', 0)
    except Exception:
        pytest.skip('Memcache is unavailable.')

    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
    assert r.status_code == 200
    assert '1' in r.data.decode('utf-8')

    r = client.get('/')
    assert r.status_code == 200
    assert '2' in r.data.decode('utf-8')
