# Copyright 2018 Google LLC
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


# [START healthcare_dicom_keeplist_deidentify_dataset]
# Imports the Dict type for runtime type hints.
from typing import Dict


# [END healthcare_dicom_keeplist_deidentify_dataset]
# [START healthcare_dicom_keeplist_deidentify_dataset]
def deidentify_dataset(
    project_id: str,
    location: str,
    dataset_id: str,
    destination_dataset_id: str,
) -> Dict[str, str]:
    """Uses a DICOM tag keeplist to create a new dataset containing de-identified DICOM data from the source dataset.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/datasets
    before running the sample.
    See https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.html#deidentify
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Google Cloud project you want
          to use.
      location: The name of the dataset's location.
      dataset_id: The ID of the source dataset containing the DICOM store to de-identify.
      destination_dataset_id: The ID of the dataset where de-identified DICOM data
        is written.

    Returns:
      A dictionary representing a long-running operation that results from
      calling the 'DeidentifyDataset' method. Use the
      'google.longrunning.Operation'
      API to poll the operation status.
    """
    # Imports the Python built-in time module.
    import time

    # Imports the Google API Discovery Service.
    from googleapiclient import discovery

    # Imports HttpError from the Google Python API client errors module.
    from googleapiclient.errors import HttpError

    api_version = "v1"
    service_name = "healthcare"
    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-source-dataset'
    # destination_dataset_id = 'my-destination-dataset'
    source_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, dataset_id
    )
    destination_dataset = "projects/{}/locations/{}/datasets/{}".format(
        project_id, location, destination_dataset_id
    )

    body = {
        "destinationDataset": destination_dataset,
        "config": {
            "dicom": {
                "keepList": {
                    "tags": [
                        "Columns",
                        "NumberOfFrames",
                        "PixelRepresentation",
                        "MediaStorageSOPClassUID",
                        "MediaStorageSOPInstanceUID",
                        "Rows",
                        "SamplesPerPixel",
                        "BitsAllocated",
                        "HighBit",
                        "PhotometricInterpretation",
                        "BitsStored",
                        "PatientID",
                        "TransferSyntaxUID",
                        "SOPInstanceUID",
                        "StudyInstanceUID",
                        "SeriesInstanceUID",
                        "PixelData",
                    ]
                }
            }
        },
    }

    request = (
        client.projects()
        .locations()
        .datasets()
        .deidentify(sourceDataset=source_dataset, body=body)
    )

    # Set a start time for operation completion.
    start_time = time.time()
    # TODO(developer): Increase the max_time if de-identifying many resources.
    max_time = 600

    try:
        operation = request.execute()
        while not operation.get("done", False):
            # Poll until the operation finishes.
            print("Waiting for operation to finish...")
            if time.time() - start_time > max_time:
                raise RuntimeError("Timed out waiting for operation to finish.")
            operation = (
                client.projects()
                .locations()
                .datasets()
                .operations()
                .get(name=operation["name"])
                .execute()
            )
            # Wait 5 seconds between each poll to the operation.
            time.sleep(5)

        if operation.get("error"):
            raise TimeoutError(f"De-identify operation failed: {operation['error']}")
        else:
            print(f"De-identified data to dataset: {destination_dataset_id}")
            print(
                f"Resources succeeded: {operation.get('metadata').get('counter').get('success')}"
            )
            print(
                f"Resources failed: {operation.get('metadata').get('counter').get('failure')}"
            )
            return operation

    except HttpError as err:
        # A common error is when the destination dataset already exists.
        if err.resp.status == 409:
            raise RuntimeError(
                f"Destination dataset with ID {destination_dataset_id} already exists."
            )
        else:
            raise err


# [END healthcare_dicom_keeplist_deidentify_dataset]
