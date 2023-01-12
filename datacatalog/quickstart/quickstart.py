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


def quickstart(override_values):
    """Creates a tag template and attach a tag to a BigQuery table."""
    # [START data_catalog_quickstart]
    # Import required modules.
    from google.cloud import datacatalog_v1

    # TODO: Set these values before running the sample.
    # Google Cloud Platform project.
    project_id = "my_project"
    # Set dataset_id to the ID of existing dataset.
    dataset_id = "demo_dataset"
    # Set table_id to the ID of existing table.
    table_id = "trips"
    # Tag template to create.
    tag_template_id = "example_tag_template"

    # [END data_catalog_quickstart]

    # To facilitate testing, we replace values with alternatives
    # provided by the testing harness.
    project_id = override_values.get("project_id", project_id)
    dataset_id = override_values.get("dataset_id", dataset_id)
    table_id = override_values.get("table_id", table_id)
    tag_template_id = override_values.get("tag_template_id", tag_template_id)

    # [START data_catalog_quickstart]
    # For all regions available, see:
    # https://cloud.google.com/data-catalog/docs/concepts/regions
    location = "us-central1"

    # Use Application Default Credentials to create a new
    # Data Catalog client. GOOGLE_APPLICATION_CREDENTIALS
    # environment variable must be set with the location
    # of a service account key file.
    datacatalog_client = datacatalog_v1.DataCatalogClient()

    # Create a Tag Template.
    tag_template = datacatalog_v1.types.TagTemplate()

    tag_template.display_name = "Demo Tag Template"

    tag_template.fields["source"] = datacatalog_v1.types.TagTemplateField()
    tag_template.fields["source"].display_name = "Source of data asset"
    tag_template.fields[
        "source"
    ].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.STRING

    tag_template.fields["num_rows"] = datacatalog_v1.types.TagTemplateField()
    tag_template.fields["num_rows"].display_name = "Number of rows in data asset"
    tag_template.fields[
        "num_rows"
    ].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.DOUBLE

    tag_template.fields["has_pii"] = datacatalog_v1.types.TagTemplateField()
    tag_template.fields["has_pii"].display_name = "Has PII"
    tag_template.fields[
        "has_pii"
    ].type_.primitive_type = datacatalog_v1.types.FieldType.PrimitiveType.BOOL

    tag_template.fields["pii_type"] = datacatalog_v1.types.TagTemplateField()
    tag_template.fields["pii_type"].display_name = "PII type"

    for display_name in ["EMAIL", "SOCIAL SECURITY NUMBER", "NONE"]:
        enum_value = datacatalog_v1.types.FieldType.EnumType.EnumValue(
            display_name=display_name
        )
        tag_template.fields["pii_type"].type_.enum_type.allowed_values.append(
            enum_value
        )

    expected_template_name = datacatalog_v1.DataCatalogClient.tag_template_path(
        project_id, location, tag_template_id
    )

    # Create the Tag Template.
    try:
        tag_template = datacatalog_client.create_tag_template(
            parent=f"projects/{project_id}/locations/{location}",
            tag_template_id=tag_template_id,
            tag_template=tag_template,
        )
        print(f"Created template: {tag_template.name}")
    except OSError as e:
        print(f"Cannot create template: {expected_template_name}")
        print(f"{e}")

    # Lookup Data Catalog's Entry referring to the table.
    resource_name = (
        f"//bigquery.googleapis.com/projects/{project_id}"
        f"/datasets/{dataset_id}/tables/{table_id}"
    )
    table_entry = datacatalog_client.lookup_entry(
        request={"linked_resource": resource_name}
    )

    # Attach a Tag to the table.
    tag = datacatalog_v1.types.Tag()

    tag.template = tag_template.name
    tag.name = "my_super_cool_tag"

    tag.fields["source"] = datacatalog_v1.types.TagField()
    tag.fields["source"].string_value = "Copied from tlc_yellow_trips_2018"

    tag.fields["num_rows"] = datacatalog_v1.types.TagField()
    tag.fields["num_rows"].double_value = 113496874

    tag.fields["has_pii"] = datacatalog_v1.types.TagField()
    tag.fields["has_pii"].bool_value = False

    tag.fields["pii_type"] = datacatalog_v1.types.TagField()
    tag.fields["pii_type"].enum_value.display_name = "NONE"

    tag = datacatalog_client.create_tag(parent=table_entry.name, tag=tag)
    print(f"Created tag: {tag.name}")
    # [END data_catalog_quickstart]
