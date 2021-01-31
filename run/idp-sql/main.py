# Copyright 2021 Google LLC
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
from functools import wraps
import json
import logging
import os
from typing import Any, Callable, Dict, Union

import firebase_admin
from firebase_admin import auth  # noqa: F401
from flask import Flask, render_template, request, Response
from google.cloud import secretmanager
import sqlalchemy

default_app = firebase_admin.initialize_app()
app = Flask(__name__, static_folder="static", static_url_path="")

logger = logging.getLogger()


def init_connection_engine() -> Dict[str, int]:
    db_config = {
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
    }

    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        return init_unix_connection_engine(db_config)


# [START cloudrun_python_user_auth_secrets]
def get_cred_config() -> Dict[str, str]:
    if "CLOUD_SQL_CREDENTIALS_SECRET" in os.environ:
        name = os.environ["CLOUD_SQL_CREDENTIALS_SECRET"]
        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": name})
        return json.loads(response.payload.data.decode("UTF-8"))
    # [END cloudrun_python_user_auth_secrets]
    else:
        logger.info(
            "CLOUD_SQL_CREDENTIALS_SECRET env var not set. Defaulting to environment variables."
        )
        if "DB_USER" not in os.environ:
            raise Exception("DB_USER needs to be set.")

        if "DB_PASSWORD" not in os.environ:
            raise Exception("DB_PASSWORD needs to be set.")

        if "DB_NAME" not in os.environ:
            raise Exception("DB_NAME needs to be set.")

        if "CLOUD_SQL_CONNECTION_NAME" not in os.environ:
            raise Exception("CLOUD_SQL_CONNECTION_NAME needs to be set.")

        return {
            "DB_USER": os.environ["DB_USER"],
            "DB_PASSWORD": os.environ["DB_PASSWORD"],
            "DB_NAME": os.environ["DB_NAME"],
            "DB_HOST": os.environ.get("DB_HOST", None),
            "CLOUD_SQL_CONNECTION_NAME": os.environ["CLOUD_SQL_CONNECTION_NAME"],
        }


def init_tcp_connection_engine(
    db_config: Dict[str, str]
) -> sqlalchemy.engine.base.Engine:
    creds = get_cred_config()
    db_user = creds["DB_USER"]
    db_pass = creds["DB_PASSWORD"]
    db_name = creds["DB_NAME"]
    db_host = creds["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 5432
            database=db_name,  # e.g. "my-database-name"
        ),
        **db_config,
    )
    pool.dialect.description_encoding = None
    return pool


# [START cloudrun_python_user_auth_sql_connect]
def init_unix_connection_engine(
    db_config: Dict[str, str]
) -> sqlalchemy.engine.base.Engine:
    creds = get_cred_config()
    db_user = creds["DB_USER"]
    db_pass = creds["DB_PASSWORD"]
    db_name = creds["DB_NAME"]
    db_socket_dir = creds.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = creds["CLOUD_SQL_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgres+pg8000://<db_user>:<db_pass>@/<db_name>
        #                         ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL(
            drivername="postgresql+pg8000",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir, cloud_sql_connection_name  # e.g. "/cloudsql"
                )  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            },
        ),
        **db_config,
    )
    pool.dialect.description_encoding = None
    return pool


# [END cloudrun_python_user_auth_sql_connect]


# This global variable is declared with a value of `None`, instead of calling
# `init_connection_engine()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None


@app.before_first_request
def create_tables() -> None:
    global db
    db = init_connection_engine()
    # Create tables (if they don't already exist)s
    with db.connect() as conn:
        result = conn.execute(
            "CREATE TABLE IF NOT EXISTS votes "
            "( vote_id SERIAL NOT NULL, "
            "time_cast timestamp NOT NULL, "
            "candidate VARCHAR(6) NOT NULL, "
            "uid VARCHAR(128) NOT NULL, "
            "PRIMARY KEY (vote_id)"
            ");"
        )
        logging.info(result)


@app.route("/", methods=["GET"])
def index() -> str:
    context = get_index_context()
    return render_template("index.html", **context)


def get_index_context() -> Dict[str, Union[int, str]]:
    votes = []

    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute(
            "SELECT candidate, time_cast FROM votes "
            "ORDER BY time_cast DESC LIMIT 5"
        ).fetchall()
        # Convert the results into a list of dicts representing votes
        for row in recent_votes:
            votes.append(
                {
                    "candidate": row[0].strip(),
                    "time_cast": row[1],
                }
            )
        stmt = sqlalchemy.text(
            "SELECT COUNT(vote_id) FROM votes WHERE candidate=:candidate"
        )
        # Count number of votes for cats
        cats_result = conn.execute(stmt, candidate="CATS").fetchone()
        cats_count = cats_result[0]
        # Count number of votes for dogs
        dogs_result = conn.execute(stmt, candidate="DOGS").fetchone()
        dogs_count = dogs_result[0]

    lead_team = ""
    vote_diff = 0
    leader_message = ""
    if cats_count != dogs_count:
        if cats_count > dogs_count:
            lead_team = "CATS"
            vote_diff = cats_count - dogs_count
        else:
            lead_team = "DOGS"
            vote_diff = dogs_count - cats_count
        leader_message = (
            f"{lead_team} are running by {vote_diff} vote{'s' if vote_diff > 1 else ''}"
        )
    else:
        leader_message = "CATS and DOGS are evenly matched!"

    return {
        "dogs_count": dogs_count,
        "recent_votes": votes,
        "cats_count": cats_count,
        "leader_message": leader_message,
        "lead_team": lead_team,
    }


# [START cloudrun_python_user_auth_jwt]
def jwt_authenticated(func: Callable[..., int]) -> Callable[..., int]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        header = request.headers.get("Authorization", None)
        if header:
            token = header.split(" ")[1]
            try:
                decoded_token = firebase_admin.auth.verify_id_token(token)
            except Exception as e:
                logger.exception(e)
                return Response(status=403, response=f"Error with authentication: {e}")
        else:
            return Response(status=401)

        request.uid = decoded_token["uid"]
        return func(*args, **kwargs)

    return decorated_function


# [END cloudrun_python_user_auth_jwt]


@app.route("/", methods=["POST"])
@jwt_authenticated
def save_vote() -> Response:
    # Get the team and time the vote was cast.
    team = request.form["team"]
    uid = request.uid
    time_cast = datetime.datetime.utcnow()
    # Verify that the team is one of the allowed options
    if team != "CATS" and team != "DOGS":
        logger.warning(team)
        return Response(response="Invalid team specified.", status=400)

    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        "INSERT INTO votes (time_cast, candidate, uid)"
        " VALUES (:time_cast, :candidate, :uid)"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, time_cast=time_cast, candidate=team, uid=uid)
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        logger.exception(e)
        return Response(
            status=500,
            response="Unable to successfully cast vote! Please check the "
            "application logs for more details.",
        )

    return Response(
        status=200,
        response="Vote successfully cast for '{}' at time {}!".format(team, time_cast),
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
