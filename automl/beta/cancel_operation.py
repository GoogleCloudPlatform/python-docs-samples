#
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


# [START automl_cancel_operation]

from google.cloud import automl_v1beta1


def sample_cancel_operation(project, operation_id):
    """
    Cancel Long-Running Operation

    Args:
      project Required. Your Google Cloud Project ID.
      operation_id Required. The ID of the Operation.
    """

    client = automl_v1beta1.AutoMlClient()

    operations_client = client._transport.operations_client

    # project = '[Google Cloud Project ID]'
    # operation_id = '[Operation ID]'
    name = "projects/{}/locations/us-central1/operations/{}".format(
        project, operation_id
    )

    operations_client.cancel_operation(name)

    print(f"Cancelled operation: {name}")


# [END automl_cancel_operation]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--operation_id", type=str, default="[Operation ID]")
    args = parser.parse_args()

    sample_cancel_operation(args.project, args.operation_id)


if __name__ == "__main__":
    main()
