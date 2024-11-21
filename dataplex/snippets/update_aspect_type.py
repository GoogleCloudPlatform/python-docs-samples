# Copyright 2024 Google LLC
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

# [START dataplex_update_aspect_type]
from typing import List

from google.cloud import dataplex_v1


def update_aspect_type(
    project_id: str,
    location: str,
    aspect_type_id: str,
    aspect_fields: List[dataplex_v1.AspectType.MetadataTemplate],
) -> dataplex_v1.AspectType:
    """Method to update Aspect Type located in project_id, location and with aspect_type_id and
    aspect_fields specifying schema of the Aspect Type"""

    # Initialize client that will be used to send requests across threads. This
    # client only needs to be created once, and can be reused for multiple requests.
    # After completing all of your requests, call the "__exit__()" method to safely
    # clean up any remaining background resources. Alternatively, use the client as
    # a context manager.
    with dataplex_v1.CatalogServiceClient() as client:
        # The resource name of the Aspect Type
        name = (
            f"projects/{project_id}/locations/{location}/aspectTypes/{aspect_type_id}"
        )
        aspect_type = dataplex_v1.AspectType(
            name=name,
            description="updated description of the aspect type",
            metadata_template=dataplex_v1.AspectType.MetadataTemplate(
                # Because Record Fields is an array, it needs to be fully replaced.
                # It is because you do not have a way to specify array elements in update mask.
                record_fields=aspect_fields
            ),
        )

        # Update mask specifies which fields will be updated.
        # For more information on update masks, see: https://google.aip.dev/161
        update_mask = {"paths": ["description", "metadata_template.record_fields"]}
        update_operation = client.update_aspect_type(
            aspect_type=aspect_type, update_mask=update_mask
        )
        return update_operation.result(60)


if __name__ == "__main__":
    # TODO(developer): Replace these variables before running the sample.
    project_id = "MY_PROJECT_ID"
    # Available locations: https://cloud.google.com/dataplex/docs/locations
    location = "MY_LOCATION"
    aspect_type_id = "MY_ASPECT_TYPE_ID"
    aspect_field = dataplex_v1.AspectType.MetadataTemplate(
        # The name must follow regex ^(([a-zA-Z]{1})([\\w\\-_]{0,62}))$
        # That means name must only contain alphanumeric character or dashes or underscores,
        # start with an alphabet, and must be less than 63 characters.
        name="name_of_the_field",
        # Metadata Template is recursive structure,
        # primitive types such as "string" or "integer" indicate leaf node,
        # complex types such as "record" or "array" would require nested Metadata Template
        type="string",
        index=1,
        annotations=dataplex_v1.AspectType.MetadataTemplate.Annotations(
            description="updated description of the field"
        ),
        constraints=dataplex_v1.AspectType.MetadataTemplate.Constraints(
            # Specifies if field will be required in Aspect Type.
            required=True
        ),
    )
    aspect_fields = [aspect_field]

    updated_aspect_type = update_aspect_type(
        project_id, location, aspect_type_id, aspect_fields
    )
    print(f"Successfully updated aspect type: {updated_aspect_type.name}")
# [END dataplex_update_aspect_type]
