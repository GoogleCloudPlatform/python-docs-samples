#!/usr/bin/env python

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

"""Demonstrates how to obtain short-lived credentials with identity federation.
"""

import urllib
import json
import boto3
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth


def create_token_aws(project_id: str, pool_id: str, provider_id: str) -> None:
    # TODO(Developer): Make sure to set the env var:
    #  "GOOGLE_APPLICATION_CREDENTIALS" before running the code.

    # Prepare a GetCallerIdentity request.
    request = AWSRequest(
        method="POST",
        url="https://sts.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15",
        headers={
            'Host': 'sts.amazonaws.com',
            'x-goog-cloud-target-resource': f'//iam.googleapis.com/projects/{project_id}/locations/global/workloadIdentityPools/{pool_id}/providers/{provider_id}'
        })

    # Sign the request.
    SigV4Auth(boto3.Session().get_credentials(), "sts", "us-east-1").add_auth(request)

    # Create token from signed request.
    token = {
        'url': request.url,
        "method": request.method,
        "headers": [{'key': key, 'value': value} for (key, value) in request.headers.items()]
    }

    print("Token:\n%s" % json.dumps(token, indent=2, sort_keys=True))
    print("URL encoded token:\n%s" % urllib.parse.quote(json.dumps(token)))


def main():
    project_id = "my-project-id"
    pool_id = "my-pool-id"
    provider_id = "my-provider-id"

    create_token_aws(project_id, pool_id, provider_id)


if __name__ == '__main__':
    main()

