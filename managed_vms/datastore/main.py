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

import datetime

from flask import Flask, request
from gcloud import datastore


app = Flask(__name__)


# [START example]
@app.route('/')
def index():
    ds = datastore.Client()

    entity = datastore.Entity(key=ds.key('visit'))
    entity.update({
        'user_ip': request.remote_addr,
        'timestamp': datetime.datetime.utcnow()
    })

    ds.put(entity)

    query = ds.query(kind='visit', order=('-timestamp',))

    results = [
        'Time: {timestamp} Addr: {user_ip}'.format(**x)
        for x in query.fetch(limit=10)]

    output = 'Last 10 visits:\n{}'.format('\n'.join(results))

    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'}
# [END example]


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See CMD in Dockerfile.
    app.run(host='127.0.0.1', port=8080, debug=True)
