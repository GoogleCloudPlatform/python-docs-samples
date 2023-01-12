# Copyright 2022 Google LLC
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
#

# [START documentai_list_processor_versions]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample


def list_processor_versions_sample(project_id: str, location: str, processor_id: str):
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    parent = client.processor_path(project_id, location, processor_id)

    # Make ListProcessorVersions request
    processor_versions = client.list_processor_versions(parent=parent)

    # Print the processor version information
    for processor_version in processor_versions:
        processor_version_id = client.parse_processor_version_path(
            processor_version.name
        )["processor_version"]

        print(f"Processor Version: {processor_version_id}")
        print(f"Display Name: {processor_version.display_name}")
        print(processor_version.state)
        print("")

    # [END documentai_list_processor_versions]
    return processor_versions
