# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Optional, Union

from google.api_core import exceptions as api_exceptions
from google.cloud.alloydb.connector import Connector, IPTypes

from pg8000 import dbapi


def get_db_connection(
    project_id: str,
    region: str,
    cluster_id: str,
    instance_id: str,
    db_user: str,
    db_pass: str,
    db_name: str,
    ip_type: IPTypes,
) -> dbapi.Connection:
    connector = None
    instance_uri = (
        f"projects/{project_id}/locations/{region}/"
        f"clusters/{cluster_id}/instances/{instance_id}"
    )
    try:
        connector = Connector()
        connection = connector.connect(
            instance_uri=instance_uri,
            driver="pg8000",
            ip_type=ip_type,
            user=db_user,
            password=db_pass,
            db=db_name,
            enable_iam_auth=False,
        )
        return connection
    except api_exceptions.Forbidden as e:
        raise ConnectionError("Missing IAM permissions to connect to AlloyDB.") from e
    except api_exceptions.NotFound as e:
        raise ConnectionError("The specified AlloyDB instance was not found.") from e
    except api_exceptions.ServiceUnavailable as e:
        raise ConnectionError("AlloyDB service is temporarily unavailable.") from e
    except api_exceptions.GoogleAPICallError as e:
        raise ConnectionError(
            "An error occurred during the AlloyDB connector's API interaction."
        ) from e
    except Exception as e:
        logging.exception(f"An unexpected error occurred during connection setup: {e}")
        raise


def execute_sql_request(
    db_connection: dbapi.Connection,
    sql_statement: str,
    params: tuple = (),
    fetch_one: bool = False,
    fetch_all: bool = False,
) -> Union[Optional[tuple], list[tuple], bool]:
    cursor = db_connection.cursor()
    cursor.execute(sql_statement, params)

    if fetch_one:
        result = cursor.fetchone()
    elif fetch_all:
        result = cursor.fetchall()
    else:
        db_connection.commit()
        result = True

    if cursor:
        cursor.close()

    return result


def perform_vector_search(
    db_connection: dbapi.Connection, word_to_find: str, limit: int = 5
) -> tuple[list]:
    sql_statement = """
        SELECT id, name, description, category, color
        FROM product
        ORDER BY embedding <=> embedding('text-embedding-005', %s)::vector
        LIMIT %s;
    """
    params = (word_to_find, limit)
    response = execute_sql_request(db_connection, sql_statement, params, fetch_all=True)

    return response
