# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def authenticate(key_path):
    # [START bigquery_client_json_credentials]
    from google.oauth2 import service_account

    # TODO(developer): Set key_path to the path to the service account key
    #                  file.
    # key_path = "path/to/service_account.json"

    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    # [END bigquery_client_json_credentials]
    return credentials


def create_client(credentials):
    # [START bigquery_client_json_credentials]
    from google.cloud import bigquery

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )
    # [END bigquery_client_json_credentials]
    return client


def main():
    import os
    credentials = authenticate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    create_client(credentials)


if __name__ == "__main__":
    main()
