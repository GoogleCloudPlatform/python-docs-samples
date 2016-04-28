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

# [START import]
from google.appengine.api import memcache
# [END import]


def query_for_data():
    return 'data'


# [START get_data]
def get_data():
    data = memcache.get('key')
    if data is not None:
        return data
    else:
        data = query_for_data()
        memcache.add('key', data, 60)
    return data
# [END get_data]


def add_values():
    # [START add_values]
    # Add a value if it doesn't exist in the cache
    # with a cache expiration of 1 hour.
    memcache.add(key="weather_USA_98105", value="raining", time=3600)

    # Set several values, overwriting any existing values for these keys.
    memcache.set_multi(
        {"USA_98115": "cloudy", "USA_94105": "foggy", "USA_94043": "sunny"},
        key_prefix="weather_",
        time=3600
    )

    # Atomically increment an integer value.
    memcache.set(key="counter", value=0)
    memcache.incr("counter")
    memcache.incr("counter")
    memcache.incr("counter")
    # [END add_values]
