# Copyright 202 Google LLC
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

from mock import patch
import pytest
import redis
import uuid

import main

KEY_PREFIX = str(uuid.uuid4())  # Avoid interfering with other tests
TEST_VALUES = {
    KEY_PREFIX + "weather_USA_98105": "raining",
    KEY_PREFIX + "weather_USA_98115": "cloudy",
    KEY_PREFIX + "weather_USA_94105": "foggy",
    KEY_PREFIX + "weather_USA_94043": "sunny",
}


@patch('main.query_for_data', return_value='data')
def test_get_data_not_present(query_fn, testbed):
    try:
        main.client.set(KEY_PREFIX + 'counter', '0', 9000)
    except redis.RedisError:
        pytest.skip('Redis is unavailable')

    data = main.get_data(KEY_PREFIX + 'key')
    query_fn.assert_called_once_with()
    assert data == 'data'
    assert 'data' == main.client.get(KEY_PREFIX + 'key')
    main.client.delete(KEY_PREFIX + 'key')


@patch('main.query_for_data', return_value='data')
def test_get_data_present(query_fn, testbed):
    try:
        main.client.set(KEY_PREFIX + 'key', 'data', 9000)
    except Exception:
        pytest.skip('Redis is unavailable')

    data = main.get_data()
    query_fn.assert_not_called()
    assert data == 'data'
    main.client.delete(KEY_PREFIX + 'key')


def test_add_values(testbed):
    try:
        main.client.set(KEY_PREFIX + 'counter', '0', 9000)
    except Exception:
        pytest.skip('Redis is unavailable')

    main.add_values(TEST_VALUES)
    for key, value in TEST_VALUES.iteritems():
        assert main.client.get(key) == value
    assert main.client.get(KEY_PREFIX + 'counter') == 3
