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

import datetime
import uuid

from google.api_core.exceptions import NotFound, PermissionDenied
import google.auth
from google.cloud import datacatalog_v1
import pytest

LOCATION = "us-central1"


def temp_suffix():
    now = datetime.datetime.now()
    return "{}_{}".format(now.strftime("%Y%m%d%H%M%S"), uuid.uuid4().hex[:8])


@pytest.fixture(scope="session")
def client(credentials):
    return datacatalog_v1.DataCatalogClient(credentials=credentials)


@pytest.fixture(scope="session")
def default_credentials():
    return google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )


@pytest.fixture(scope="session")
def credentials(default_credentials):
    return default_credentials[0]


@pytest.fixture(scope="session")
def project_id(default_credentials):
    return default_credentials[1]


@pytest.fixture
def valid_member_id(client, project_id, random_existing_tag_template_id):
    template_name = datacatalog_v1.DataCatalogClient.tag_template_path(
        project_id, LOCATION, random_existing_tag_template_id
    )

    # Retrieve Template's current IAM Policy.
    policy = client.get_iam_policy(resource=template_name)
    yield policy.bindings[0].members[0]


@pytest.fixture
def resources_to_delete(client, project_id):
    doomed = {
        "entries": [],
        "entry_groups": [],
        "templates": [],
    }
    yield doomed

    for entry_name in doomed["entries"]:
        try:
            client.delete_entry(name=entry_name)
        except (NotFound, PermissionDenied):
            pass
    for group_name in doomed["entry_groups"]:
        try:
            client.delete_entry_group(name=group_name)
        except (NotFound, PermissionDenied):
            pass
    for template_name in doomed["templates"]:
        try:
            client.delete_tag_template(name=template_name, force=True)
        except (NotFound, PermissionDenied):
            pass


@pytest.fixture
def random_entry_id():
    random_entry_id = f"python_sample_entry_{temp_suffix()}"
    yield random_entry_id


@pytest.fixture
def random_entry_group_id():
    random_entry_group_id = f"python_sample_group_{temp_suffix()}"
    yield random_entry_group_id


@pytest.fixture
def random_tag_template_id():
    random_tag_template_id = f"python_sample_{temp_suffix()}"
    yield random_tag_template_id


@pytest.fixture
def random_existing_tag_template_id(client, project_id, resources_to_delete):
    random_tag_template_id = f"python_sample_{temp_suffix()}"
    random_tag_template = datacatalog_v1.types.TagTemplate()
    random_tag_template.fields["source"] = datacatalog_v1.types.TagTemplateField()
    random_tag_template.fields[
        "source"
    ].type_.primitive_type = datacatalog_v1.FieldType.PrimitiveType.STRING.value
    random_tag_template = client.create_tag_template(
        parent=datacatalog_v1.DataCatalogClient.common_location_path(
            project_id, LOCATION
        ),
        tag_template_id=random_tag_template_id,
        tag_template=random_tag_template,
    )
    yield random_tag_template_id
    resources_to_delete["templates"].append(random_tag_template.name)


@pytest.fixture(scope="session")
def policy_tag_manager_client(credentials):
    return datacatalog_v1.PolicyTagManagerClient(credentials=credentials)


@pytest.fixture
def random_taxonomy_display_name(policy_tag_manager_client, project_id):
    now = datetime.datetime.now()
    random_display_name = (
        f"example_taxonomy"
        f'_{now.strftime("%Y%m%d%H%M%S")}'
        f"_{uuid.uuid4().hex[:8]}"
    )
    yield random_display_name
    parent = datacatalog_v1.PolicyTagManagerClient.common_location_path(
        project_id, "us"
    )
    taxonomies = policy_tag_manager_client.list_taxonomies(parent=parent)
    taxonomy = next(
        (t for t in taxonomies if t.display_name == random_display_name), None
    )
    if taxonomy:
        policy_tag_manager_client.delete_taxonomy(name=taxonomy.name)
