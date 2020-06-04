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


# Remember - storing secrets in plaintext is potentially unsafe. Consider using
# something like https://cloud.google.com/kms/ to help keep secrets secret.
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
db_name = os.environ.get("DB_NAME")
cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

app = Flask(__name__)

logger = logging.getLogger()


def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]
        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]
        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]
        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }

    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        return init_unix_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_tcp]
    db_socket_addr = os.environ.get("DB_HOST").split(":")

    # Extract host and port from socket address
    db_host = db_socket_addr[0]
    db_port = int(db_socket_addr[1])

    return sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
        # ... Specify additional properties here.
        # [START_EXCLUDE]
        **db_config
        # [END_EXCLUDE]
    )
    # [END cloud_sql_mysql_sqlalchemy_create_tcp]


def init_unix_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_socket]
    if os.environ.get("DB_SOCKET_PATH"):
        socket_path = os.environ.get("DB_SOCKET_PATH")
    else:
        socket_path = "/cloudsql"

    return sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "unix_socket": "{}/{}".format(
                    socket_path,
                    cloud_sql_connection_name)
            }
        ),
        # ... Specify additional properties here.
        # [START_EXCLUDE]
        **db_config
        # [END_EXCLUDE]
    )
    # [END cloud_sql_mysql_sqlalchemy_create_socket]


# The SQLAlchemy engine will help manage interactions, including automatically
# managing a pool of connections to your database
db = init_connection_engine()


@app.before_first_request
def create_tables():
    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS votes "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate CHAR(6) NOT NULL, PRIMARY KEY (vote_id) );"
        )


@app.route("/", methods=["GET"])
def index():
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

    return render_template(
        "index.html", recent_votes=votes, tab_count=tab_count, space_count=space_count
    )


@app.route("/", methods=["POST"])
def save_vote():
    # Get the team and time the vote was cast.
    team = request.form["team"]
    time_cast = datetime.datetime.utcnow()
    # Verify that the team is one of the allowed options
    if team != "TABS" and team != "SPACES":
        logger.warning(team)
        return Response(response="Invalid team specified.", status=400)

    # [START cloud_sql_mysql_sqlalchemy_connection]
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
    # [END cloud_sql_mysql_sqlalchemy_connection]

    return Response(
        status=200,
        response="Vote successfully cast for '{}' at time {}!".format(team, time_cast),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
