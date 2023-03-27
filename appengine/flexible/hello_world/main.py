# Copyright 2015 Google LLC
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

# [START gae_flex_quickstart]
from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello() -> str:
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


data = [
    {"id": "s3450966", "user_name": "mohamed ali0", "password": "012345"},
    {"id": "s3450967", "user_name": "mohamed ali1", "password": "123456"},
    {"id": "s3450968", "user_name": "mohamed ali2", "password": "234567"},
    {"id": "s3450969", "user_name": "mohamed ali3", "password": "345678"},
    {"id": "s3450970", "user_name": "mohamed ali4", "password": "456789"},
    {"id": "s3450971", "user_name": "mohamed ali5", "password": "567890"},
    {"id": "s3450972", "user_name": "mohamed ali6", "password": "678901"},
    {"id": "s3450973", "user_name": "mohamed ali7", "password": "789012"},
    {"id": "s3450974", "user_name": "mohamed ali8", "password": "890123"},
    {"id": "s3450975", "user_name": "mohamed ali9", "password": "901234"},
]

# Print header row
print("{:<15} {:<20} {:<15}".format("id", "user_name", "password"))

# Print table rows
for item in data:
    print("{:<15} {:<20} {:<15}".format(item["id"], item["user_name"], item["password"]))





if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
