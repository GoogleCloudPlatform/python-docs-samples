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
import sqlalchemy
import sys

import tink
from tink import aead
from tink.integration import gcpkms


# [START cloud_sql_mysql_cse_key]
def init_tink():
    aead.register()
    key_uri = "gcp-kms://" + os.environ["KMS_KEY_URI"]
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")

    try:
        gcp_client = gcpkms.GcpKmsClient(key_uri, credentials)
        gcp_aead = gcp_client.get_aead(key_uri)
    except tink.TinkError as e:
        logging.error('Error initializing GCP client: %s', e)
        return None

    # Create envelope AEAD primitive using AES256 GCM for encrypting the data
    try:
        key_template = aead.aead_key_templates.AES256_GCM
        env_aead = aead.KmsEnvelopeAead(key_template, gcp_aead)
    except tink.TinkError as e:
        logging.error('Error creating primitive: %s', e)
        return None
    return env_aead
# [END cloud_sql_mysql_cse_key]


    
def init_connection_engine():
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


def init_tcp_connection_engine(db_config):
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        ),
        **db_config
    )

    return pool


def init_unix_connection_engine(db_config):
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )

    return pool


def init_db():
    db = init_connection_engine()

    # Create tables (if they don't already exist)
    with db.connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS votes "
            "( vote_id SERIAL NOT NULL, time_cast timestamp NOT NULL, "
            "candidate CHAR(6) NOT NULL, voter_email VARBINARY(255), "
            "PRIMARY KEY (vote_id) );"
        )
    return db



# [START cloud_sql_mysql_cse_query]
def list_votes(db, eaead):
    import sqlalchemy
    
    with db.connect() as conn:
        # Execute the query and fetch all results
        recent_votes = conn.execute(
            "SELECT candidate, time_cast, voter_email FROM votes "
            "ORDER BY time_cast DESC LIMIT 5"
        ).fetchall()

        print("Team\tEmail\tTime Cast")
        
        for row in recent_votes:
            team = row[0]
            email = eaead.decrypt(row[2], team.encode()).decode()
            time_cast = row[1]

            # Print recent votes
            print("{}\t{}\t{}".format(team, email, time_cast))

        stmt = sqlalchemy.text(
            "SELECT COUNT(vote_id) FROM votes WHERE candidate=:candidate"
        )
        # Count number of votes for tabs
        tab_result = conn.execute(stmt, candidate="TABS").fetchone()
        tab_count = tab_result[0]
        # Count number of votes for spaces
        space_result = conn.execute(stmt, candidate="SPACES").fetchone()
        space_count = space_result[0]

        # Print total votes
        print("")
        print("Total: {} spaces, {} tabs".format(space_count, tab_count))
# [END cloud_sql_mysql_cse_query]


# [START cloud_sql_mysql_cse_insert]
def add_vote(team, email, db, eaead):
    import sqlalchemy

    time_cast = datetime.datetime.utcnow()
    # Encrypt the email of the voter
    encrypted_email = eaead.encrypt(email.encode(), team.encode())
    # Verify that the team is one of the allowed options
    if team != "TABS" and team != "SPACES":
        logger.error("Invalid team specified: {}".format(team))
        return

    # Preparing a statement before hand can help protect against injections.
    stmt = sqlalchemy.text(
        "INSERT INTO votes (time_cast, candidate, voter_email)"
        " VALUES (:time_cast, :candidate, :voter_email)"
    )
    try:
        # Using a with statement ensures that the connection is always released
        # back into the pool at the end of statement (even if an error occurs)
        with db.connect() as conn:
            conn.execute(stmt, time_cast=time_cast, candidate=team,
                         voter_email=encrypted_email)
    except Exception as e:
        # If something goes wrong, handle the error in this section. This might
        # involve retrying or adjusting parameters depending on the situation.
        logger.exception(e)

    print("Vote successfully cast for '{}' at time {}!".format(team, time_cast))
# [END cloud_sql_mysql_cse_insert]


if __name__ == "__main__":
    db = init_db()
    eaead = init_tink_eaead()

    action = "VIEW"
    if len(sys.argv) > 1:
        action = sys.argv[1]
    
    if action == "VOTE_TABS":
        add_vote(team="TABS", email=sys.argv[2], db=db, eaead=eaead)
    elif action == "VOTE_SPACES":
        add_vote(team="SPACES", email=sys.argv[2], db=db, eaead=eaead)
    elif action == "VIEW":
        list_votes(db=db, eaead)
