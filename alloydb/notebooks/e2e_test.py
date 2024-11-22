# Copyright 2022 Google LLC.
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

# Maintainer Note: this sample presumes data exists in
# ALLOYDB_TABLE_NAME within the ALLOYDB_(cluster/instance/database)

import asyncpg  # type: ignore
import conftest as conftest  # python-docs-samples/alloydb/conftest.py
from google.cloud.alloydb.connector import AsyncConnector, IPTypes
import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


def preprocess(source: str) -> str:
    # Skip the cells which add data to table
    if "df" in source:
        return ""
    # Skip the colab auth cell
    if "colab" in source:
        return ""
    return source


async def _init_connection_pool(
    connector: AsyncConnector,
    db_name: str,
    project_id: str,
    cluster_name: str,
    instance_name: str,
    region: str,
    password: str,
) -> AsyncEngine:
    connection_string = (
        f"projects/{project_id}/locations/"
        f"{region}/clusters/{cluster_name}/"
        f"instances/{instance_name}"
    )

    async def getconn() -> asyncpg.Connection:
        conn: asyncpg.Connection = await connector.connect(
            connection_string,
            "asyncpg",
            user="postgres",
            password=password,
            db=db_name,
            ip_type=IPTypes.PUBLIC,
        )
        return conn

    pool = create_async_engine(
        "postgresql+asyncpg://",
        async_creator=getconn,
        max_overflow=0,
    )
    return pool


@pytest.mark.asyncio
async def test_embeddings_batch_processing(
    project_id: str,
    cluster_name: str,
    instance_name: str,
    region: str,
    database_name: str,
    password: str,
    table_name: str,
) -> None:
    # TODO: Create new table
    # Populate the table with embeddings by running the notebook
    conftest.run_notebook(
        "embeddings_batch_processing.ipynb",
        variables={
            "project_id": project_id,
            "cluster_name": cluster_name,
            "database_name": database_name,
            "region": region,
            "instance_name": instance_name,
            "table_name": table_name,
        },
        preprocess=preprocess,
        skip_shell_commands=True,
        replace={
            (
                "password = input(\"Please provide "
                "a password to be used for 'postgres' "
                "database user: \")"
            ): f"password = '{password}'",
            (
                "await create_db("
                "database_name=database_name, "
                "connector=connector)"
            ): "",
        },
        until_end=True,
    )

    # Connect to the populated table for validation and clean up
    async with AsyncConnector() as connector:
        pool = await _init_connection_pool(
            connector,
            database_name,
            project_id,
            cluster_name,
            instance_name,
            region,
            password,
        )
        async with pool.connect() as conn:
            # Validate that embeddings are non-empty for all rows
            result = await conn.execute(
                sqlalchemy.text(
                    f"SELECT COUNT(*) FROM "
                    f"{table_name} WHERE "
                    f"analysis_embedding IS NULL"
                )
            )
            row = result.fetchone()
            assert row[0] == 0
            result = await conn.execute(
                sqlalchemy.text(
                    f"SELECT COUNT(*) FROM "
                    f"{table_name} WHERE "
                    f"overview_embedding IS NULL"
                )
            )
            row = result.fetchone()
            assert row[0] == 0

            # Get the table back to the original state
            await conn.execute(
                sqlalchemy.text(
                    f"UPDATE {table_name} set "
                    f"analysis_embedding = NULL"
                )
            )
            await conn.execute(
                sqlalchemy.text(
                    f"UPDATE {table_name} set "
                    f"overview_embedding = NULL"
                )
            )
            await conn.commit()
        await pool.dispose()
