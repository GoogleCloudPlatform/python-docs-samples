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

import datetime
import logging
import os

from flask import Flask, render_template, request, Response
import sqlalchemy
from connect_connector import create_connector_pool
from connect_tcp import create_tcp_pool
from connect_unix import create_unix_socket_pool


app = Flask(__name__)

logger = logging.getLogger()


def init_connection_pool():
    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    if os.environ.get("INSTANCE_HOST"):
        return create_tcp_pool()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return create_unix_socket_pool()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        return create_connector_pool()

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )


# Create 'votes' table in database (if doesn't already exist)
def create_table(db):
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS votes "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate VARCHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
        )


# initialize connection pool to database and create 'votes' table on startup
db = init_connection_pool()
create_table(db)


@app.route("/", methods=["GET", "POST"])
@app.route("/votes", methods=["GET", "POST"])
def votes(cloud_function_request=False):
    # Cloud Function requires request param
    if cloud_function_request:
        http_request = cloud_function_request
    # Cloud Run, App Engine, etc. use built-in flask.request
    else:
        http_request = request

    if http_request.method == "GET":
        context = get_index_context()
        return render_template("index.html", **context)

    elif http_request.method == "POST":
        team = http_request.form["team"]
        return save_vote(team)

    else:
        return Response(
            response="Invalid http request. Method not allowed, must be 'GET' or 'POST'",
            status=400,
        )


# get_index_context gets data required for rendering HTML application
def get_index_context():
    votes = []

    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute(
            "SELECT candidate, time_cast FROM votes " "ORDER BY time_cast DESC LIMIT 5"
        ).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in recent_votes:
            votes.append({"candidate": row[0], "time_cast": row[1]})

        stmt = sqlalchemy.text(
            "SELECT COUNT(vote_id) FROM votes WHERE candidate=:candidate"
        )
        # Count number of votes for tabs
        tab_result = conn.execute(stmt, candidate="TABS").fetchone()
        tab_count = tab_result[0]
        # Count number of votes for spaces
        space_result = conn.execute(stmt, candidate="SPACES").fetchone()
        space_count = space_result[0]

    return {
        "space_count": space_count,
        "recent_votes": votes,
        "tab_count": tab_count,
    }


# save_vote saves a vote to the database that was retrieved from form data
def save_vote(team: str) -> Response:
    time_cast = datetime.datetime.now(tz=datetime.timezone.utc)
    # Verify that the team is one of the allowed options
    if team != "TABS" and team != "SPACES":
        logger.warning(f"'Team' property should be 'TABS' or 'SPACES', got {team}")
        return Response(
            response="Invalid team specified. Should be one of 'TABS' or 'SPACES'",
            status=400,
        )

    # [START cloud_sql_postgres_sqlalchemy_connection]
    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        "INSERT INTO votes (time_cast, candidate)" " VALUES (:time_cast, :candidate)"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, time_cast=time_cast, candidate=team)
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        # [START_EXCLUDE]
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to successfully cast vote! Please check the "
            "application logs for more details.",
        )
        # [END_EXCLUDE]
    # [END cloud_sql_postgres_sqlalchemy_connection]

    return Response(
        status=200,
        response="Vote successfully cast for '{}' at time {}!".format(team, time_cast),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
