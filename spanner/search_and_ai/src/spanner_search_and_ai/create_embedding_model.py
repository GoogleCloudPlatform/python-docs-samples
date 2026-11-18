# Copyright 2026 Google LLC
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

# [START spanner_create_embedding_model]
import sys

from google.api_core import exceptions
from google.cloud import spanner_admin_database_v1


def create_embedding_model(
    project_id: str,
    location_id: str,
    instance_id: str,
    database_id: str,
) -> None:
    """Registers a remote Vertex AI text-embedding model in a Spanner schema.

    Args:
        project_id: The Google Cloud project ID.
        location_id: The Vertex AI endpoint region (such as 'us-central1').
        instance_id: The Spanner instance ID.
        database_id: The Spanner GoogleSQL database ID.
    """
    client = spanner_admin_database_v1.DatabaseAdminClient()
    database_path = client.database_path(project_id, instance_id, database_id)
    model_name = "TextEmbeddingModel"
    endpoint = (
        f"//aiplatform.googleapis.com/projects/{project_id}"
        f"/locations/{location_id}/publishers/google/models/text-embedding-005"
    )
    ddl_statement = f"""
        CREATE OR REPLACE MODEL {model_name}
        INPUT (
            content STRING(MAX),
            task_type STRING(MAX) OPTIONS (required = false)
        )
        OUTPUT (
            embeddings STRUCT<
                statistics STRUCT<truncated BOOL, token_count FLOAT64>,
                values ARRAY<FLOAT32>
            >
        )
        REMOTE OPTIONS (
            endpoint = '{endpoint}'
        )
    """.strip()
    request = spanner_admin_database_v1.UpdateDatabaseDdlRequest(
        database=database_path,
        statements=[ddl_statement],
    )

    try:
        operation = client.update_database_ddl(request=request)
        print(f"Waiting for remote model '{model_name}' registration...")
        operation.result(timeout=300)
    except exceptions.AlreadyExists as err:
        print(
            f"error: model '{model_name}' already exists on database "
            f"'{database_id}' in instance '{instance_id}' and location "
            f"'{location_id}': {err.message}",
            file=sys.stderr,
        )
    except exceptions.GoogleAPICallError as err:
        print(
            f"error: failed to register model '{model_name}' on database "
            f"'{database_id}' in instance '{instance_id}' and location "
            f"'{location_id}': {err.message}",
            file=sys.stderr,
        )
    else:
        print(f"Resource ID: {database_id}")
        print(f"Endpoint Location: {location_id}")
        print(f"Model Name: {model_name}")


# [END spanner_create_embedding_model]


if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="Register a Vertex AI text-embedding model in Spanner."
    )
    parser.add_argument(
        "--project-id",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT", "example-project-id"),
        help="Google Cloud project ID (default: $GOOGLE_CLOUD_PROJECT)",
    )
    parser.add_argument(
        "--location-id",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Vertex AI region (default: $GOOGLE_CLOUD_LOCATION)",
    )
    parser.add_argument(
        "--instance-id",
        default=os.environ.get("SPANNER_INSTANCE_ID", "example-instance"),
        help="Spanner instance ID (default: $SPANNER_INSTANCE_ID)",
    )
    parser.add_argument(
        "--database-id",
        default=os.environ.get("SPANNER_DATABASE_ID", "example-db"),
        help="Spanner database ID (default: $SPANNER_DATABASE_ID)",
    )
    args = parser.parse_args()

    create_embedding_model(
        project_id=args.project_id,
        location_id=args.location_id,
        instance_id=args.instance_id,
        database_id=args.database_id,
    )
