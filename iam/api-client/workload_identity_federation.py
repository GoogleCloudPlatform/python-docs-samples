#  Copyright 2021 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Demonstrates how to obtain short-lived credentials with identity federation."""
# [START iam_workload_identity_aws_credential]
import json
import urllib

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def create_token_aws(project_number: str, pool_id: str, provider_id: str) -> None:
    # Prepare a GetCallerIdentity request.
    request = AWSRequest(
        method="POST",
        url="https://sts.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15",
        headers={
            "Host": "sts.amazonaws.com",
            "x-goog-cloud-target-resource": f"//iam.googleapis.com/projects/{project_number}/locations/global/workloadIdentityPools/{pool_id}/providers/{provider_id}"
        })

    # Set the session credentials and Sign the request.
    # get_credentials loads the required credentials as environment variables.
    # Refer:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    SigV4Auth(boto3.Session().get_credentials(), "sts", "us-east-1").add_auth(request)

    # Create token from signed request.
    token = {
        "url": request.url,
        "method": request.method,
        "headers": []
    }
    for key, value in request.headers.items():
        token["headers"].append({"key": key, "value": value})

    # The token lets workload identity federation verify the identity without revealing the AWS secret access key.
    print("Token:\n%s" % json.dumps(token, indent=2, sort_keys=True))
    print("URL encoded token:\n%s" % urllib.parse.quote(json.dumps(token)))


def main() -> None:
    # TODO(Developer): Replace the below credentials.
    # project_number: Google Project number (not the project id)
    project_number = "my-project-number"
    pool_id = "my-pool-id"
    provider_id = "my-provider-id"

    create_token_aws(project_number, pool_id, provider_id)


if __name__ == "__main__":
    main()
# [END iam_workload_identity_aws_credential]
