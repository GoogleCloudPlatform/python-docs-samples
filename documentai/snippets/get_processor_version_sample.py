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

# [START documentai_get_processor_version]

from google.api_core.client_options import ClientOptions
from google.cloud import documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
# project_id = 'YOUR_PROJECT_ID'
# location = 'YOUR_PROCESSOR_LOCATION' # Format is 'us' or 'eu'
# processor_id = 'YOUR_PROCESSOR_ID' # Create processor before running sample
# processor_version_id = 'YOUR_PROCESSOR_VERSION_ID'


def get_processor_version_sample(
    project_id: str, location: str, processor_id: str, processor_version_id: str
) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor version
    # e.g.: projects/project_id/locations/location/processors/processor_id/processorVersions/processor_version_id
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version_id
    )

    # Make GetProcessorVersion request
    processor_version = client.get_processor_version(name=name)

    # Print the processor version information
    print(f"Processor Version: {processor_version_id}")
    print(f"Display Name: {processor_version.display_name}")
    print(processor_version.state)


# [END documentai_get_processor_version]
