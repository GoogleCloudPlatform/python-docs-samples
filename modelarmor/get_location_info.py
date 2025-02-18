# python-docs-samples/modelarmor/get_location_info.py

# Copyright 2021 Google LLC
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


def get_location_info(project_id: str, location_id: str):
    """
    Gets information about a specific location.

    Args:
        project_id (str): The Google Cloud project ID.
        location_id (str): The ID of the location to retrieve information for.

    Returns:
        The location information.
    """
    from google.cloud import modelarmor_v1
    from google.cloud.location import locations_pb2
    from google.api_core.client_options import ClientOptions

    # Initialize the client for the specific Google Cloud service.
    client = modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com")
    )

    request = locations_pb2.GetLocationRequest(
        name=f"projects/{project_id}/locations/{location_id}"
    )

    # Retrieve the location information
    location_info = client.get_location(request=request)

    print(f"Location Information: {location_info}")
    return location_info

if __name__ == "__main__":
    # Sample usage
    project_id = "gma-api-53286"
    location_id = "us-central1"

    get_location_info(project_id=project_id, location_id=location_id)