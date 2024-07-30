# # Copyright 2023 Google LLC
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

import os

from contentwarehouse.snippets import create_document_schema_sample
from contentwarehouse.snippets import delete_document_schema_sample
from contentwarehouse.snippets import get_document_schema_sample
from contentwarehouse.snippets import test_utilities

import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
@pytest.mark.dependency(name="create")
def test_create_document_schema(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    response = create_document_schema_sample.sample_create_document_schema(
        project_number=project_number, location=location
    )

    assert "display_name" in response

    document_schema_id = response.name.split("/")[-1]

    request.config.cache.set("document_schema_id", document_schema_id)


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
@pytest.mark.dependency(name="get", depends=["create"])
def test_get_document_schema(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    document_schema_id = request.config.cache.get("document_schema_id", None)

    response = get_document_schema_sample.sample_get_document_schema(
        project_number=project_number,
        location=location,
        document_schema_id=document_schema_id,
    )

    assert "display_name" in response


@pytest.mark.skip(
    "Document AI Warehouse is deprecated and will no longer be available on Google Cloud after January 16, 2025."
)
@pytest.mark.dependency(name="delete", depends=["get"])
def test_delete_document_schema(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    document_schema_id = request.config.cache.get("document_schema_id", None)

    response = delete_document_schema_sample.sample_delete_document_schema(
        project_number=project_number,
        location=location,
        document_schema_id=document_schema_id,
    )

    assert response is None
