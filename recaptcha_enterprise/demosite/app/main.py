# Copyright 2023 Google LLC
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

from flask import Flask

import urls

app = Flask(__name__)

app.add_url_rule(rule="/", methods=["GET"], view_func=urls.home)
app.add_url_rule(rule="/store", methods=["GET"], view_func=urls.store)
app.add_url_rule(rule="/login", methods=["GET"], view_func=urls.login)
app.add_url_rule(rule="/comment", methods=["GET"], view_func=urls.comment)
app.add_url_rule(rule="/signup", methods=["GET"], view_func=urls.signup)
app.add_url_rule(rule="/game", methods=["GET"], view_func=urls.game)
app.add_url_rule(
    rule="/create_assessment", methods=["POST"], view_func=urls.create_assessment
)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
