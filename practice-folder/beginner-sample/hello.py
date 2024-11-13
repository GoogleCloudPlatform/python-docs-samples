# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    last_updated = "3:01 PM PST, Friday, January 8, 2024"
    return f"Hello. This page was last updated at {last_updated}."


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")
