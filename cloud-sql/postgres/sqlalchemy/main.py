# Copyright 2018 Google LLC
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

import flask

import functions_framework

from app import get_index_context, init_connection_pool, migrate_db, save_vote

############ TABS vs. SPACES App for Cloud Functions ############

# lazy global initialization
# db connection must be established within request context
db = None


@functions_framework.http
def votes(request: flask.Request) -> flask.Response:
    global db
    # initialize db within request context
    if not db:
        # initiate a connection pool to a Cloud SQL database
        db = init_connection_pool()
        # creates required 'votes' table in database (if it does not exist)
        migrate_db(db)
    if request.method == "GET":
        context = get_index_context(db)
        return flask.render_template("index.html", **context)

    if request.method == "POST":
        team = request.form["team"]
        return save_vote(db, team)

    return flask.Response(
        response="Invalid http request. Method not allowed, must be 'GET' or 'POST'",
        status=400,
    )
