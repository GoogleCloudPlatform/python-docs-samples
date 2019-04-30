# Copyright 2016 Google Inc. All rights reserved.
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

from google.appengine.api import memcache
from mock import patch

import snippets


SNIPPET_VALUES = {
    "weather_USA_98105": "raining",
    "weather_USA_98115": "cloudy",
    "weather_USA_94105": "foggy",
    "weather_USA_94043": "sunny",
    "counter": 3,
}


@patch('snippets.query_for_data', return_value='data')
def test_get_data_not_present(query_fn, testbed):
    data = snippets.get_data()
    query_fn.assert_called_once_with()
    assert data == 'data'
    memcache.delete('key')


@patch('snippets.query_for_data', return_value='data')
def test_get_data_present(query_fn, testbed):
    memcache.add('key', 'data', 9000)
    data = snippets.get_data()
    query_fn.assert_not_called()
    assert data == 'data'
    memcache.delete('key')


def test_add_values(testbed):
    snippets.add_values()
    for key, value in SNIPPET_VALUES.iteritems():
        assert memcache.get(key) == value
