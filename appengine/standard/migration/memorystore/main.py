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

# This code contrasts how Python 2.7 apps using the memcache library can be
# changed to use the Memorycache for Redis API and libraries, instead, under
# either Python 2.7 or Python 3.6 or later.
#
# The examples are taken from the appengine/standard/memcache/snippets example
# in this repository. The lines of code from the old example are included here
# as comments, preceded by ## to distinguish them.
#
# The samples are wrapped in a Flask web app to run in App Engine.

## from google.appengine.api import memcache
import os
import redis
import time

from flask import Flask, redirect, render_template, request

redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', '6379')
client = redis.Redis(host=redis_host, port=redis_port)


# Dummy store that this sample shows being cached
def query_for_data():
    # Add artificial delay so user can see when cache has been used
    time.sleep(5)
    return 'prestored value'


def get_data(cache_key):
    ##  data = memcache.get('key')
    data = client.get(cache_key)

    if data is not None:
        return data.decode()
    else:
        data = query_for_data()
    ##      memcache.add('key', data, 60)
        client.set(cache_key, data, ex=60)

    return data


def add_values(values, expires=3600):
    # Add a value if it doesn't exist in the cache
    # with a cache expiration of 1 hour.
    ##  memcache.add(key="weather_USA_98105", value="raining", time=3600)
    ##  # Remove one of the values and set by itself first
    ##  first_key = values.keys()[0]
    ##  first_value = values[first_key]
    ##  del values[first_key]
    ##  memcache.add(first_key, first_value, ex=expires)
    ##
    ##  # Set several values, overwriting any existing values for these keys.
    ##  memcache.set_multi(
    ##      {"USA_98115": "cloudy", "USA_94105": "foggy", "USA_94043": "sunny"},
    ##      key_prefix="weather_",
    ##      time=3600
    ##  )
    # Redis mset is similar to memcache.set_multi, but cannot set expirations
    client.mset(values)

    # Rather than set expiration with separate operations for each key, batch
    # them using pipeline
    with client.pipeline() as pipe:
        for name in values:
            pipe.pexpire(name, expires * 1000)  # Time in milliseconds
        pipe.execute()


def increment_counter(name, expires=60, value=0):
    # Atomically increment an integer value.
    ##  memcache.set(key="counter", value=0)
    client.set(name, value, ex=expires)
    ##  memcache.incr("counter")
    client.incr(name)
    ##  memcache.incr("counter")
    client.incr(name)
    ##  memcache.incr("counter")
    client.incr(name)


# Web app to invoke above samples follows
app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/showdata', methods=['GET'])
def showdata():
    data = get_data('data')

    values = {}
    for key in client.keys():
        if key == 'data':
            next
        values[key.decode()] = client.get(key).decode()

    return render_template('showdata.html', data=data, values=values)


@app.route('/showdata', methods=['POST'])
def savedata():
    key = request.form['key']
    value = request.form['value']
    add_values({key: value})
    if key == 'counter':
        increment_counter('counter', expires=60, value=value)
    return redirect('/')


if __name__ == '__main__':
    # This is used when running locally.
    app.run(host='127.0.0.1', port=8080, debug=True)
