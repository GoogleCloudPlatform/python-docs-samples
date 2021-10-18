# Copyright 2021 Google Inc. All Rights Reserved.
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

"""Demonstrates how to obtain short-lived credentials with identity federation."""
import os
import urllib
import json
import boto3
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth


def create_token_aws(project_id: str, pool_id: str, provider_id: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
    # Prepare a GetCallerIdentity request.
    request = AWSRequest(
        method="POST",
        url="https://sts.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15",
        headers={
            'Host': 'sts.amazonaws.com',
            'x-goog-cloud-target-resource': f'//iam.googleapis.com/projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}/providers/{provider_id}'
        })

    # Set the session credentials.
    # **NOTE: Please refrain from passing the variables as parameters.**
    # Instead load them as env variables or for other ways, refer:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # Sign the request.
    SigV4Auth(session.get_credentials(), "sts", "us-east-1").add_auth(request)

    # Create token from signed request.
    token = {
        'url': request.url,
        "method": request.method,
        "headers": [{'key': key, 'value': value} for (key, value) in request.headers.items()]
    }

    print("Token:\n%s" % json.dumps(token, indent=2, sort_keys=True))
    print("URL encoded token:\n%s" % urllib.parse.quote(json.dumps(token)))


def main():
    # TODO(Developer): Replace the below credentials.
    project_id = "my-project-id"
    pool_id = "my-pool-id"
    provider_id = "my-provider-id"

    aws_access_key_id=os.environ["aws_access_key_id"]
    aws_secret_access_key=os.environ["aws_secret_access_key"]

    create_token_aws(project_id, pool_id, provider_id, aws_access_key_id, aws_secret_access_key)


if __name__ == '__main__':
    main()
