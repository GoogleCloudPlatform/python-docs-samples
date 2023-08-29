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

from contentwarehouse.snippets import create_document_sample
from contentwarehouse.snippets import delete_document_sample
from contentwarehouse.snippets import get_document_sample
from contentwarehouse.snippets import create_document_schema_sample
from contentwarehouse.snippets import delete_document_schema_sample
from contentwarehouse.snippets import test_utilities

import pytest

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
location = "us"
raw_doc_path = "gs://cloud-samples-data/documentai/codelabs/warehouse/order-invoice.pdf"
mime_type = "application/pdf"
user_id = "user:dmoonat@google.com"
reference_id = "001"


@pytest.mark.dependency(name="create_schema")
def test_create_document_schema(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    response = create_document_schema_sample.sample_create_document_schema(
        project_number=project_number, location=location
    )

    assert "display_name" in response

    document_schema_id = response.name.split("/")[-1]

    request.config.cache.set("document_schema_id", document_schema_id)


@pytest.mark.dependency(name="create_doc", depends=["create_schema"])
def test_create_document(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    document_schema_id = request.config.cache.get("document_schema_id", None)

    response = create_document_sample.sample_create_document(
        project_number=project_number,
        location=location,
        raw_doc_path=raw_doc_path,
        mime_type=mime_type,
        document_schema_id=document_schema_id,
        user_id=user_id,
        reference_id=reference_id,
    )

    assert "document" in response

    request.config.cache.set("document_name", response.document.name)


@pytest.mark.dependency(name="get_doc", depends=["create_doc"])
def test_get_document(request: pytest.fixture) -> None:
    document_name = request.config.cache.get("document_name", None)

    response = get_document_sample.sample_get_document(
        doc_name=document_name, user_id=user_id
    )

    assert "name" in response


@pytest.mark.dependency(name="delete_doc", depends=["get_doc"])
def test_delete_document(request: pytest.fixture) -> None:
    document_name = request.config.cache.get("document_name", None)

    response = delete_document_sample.sample_delete_document(
        doc_name=document_name, user_id=user_id
    )

    assert response is None


@pytest.mark.dependency(name="delete_schema", depends=["delete_doc"])
def test_delete_document_schema(request: pytest.fixture) -> None:
    project_number = test_utilities.get_project_number(project_id)

    document_schema_id = request.config.cache.get("document_schema_id", None)

    response = delete_document_schema_sample.sample_delete_document_schema(
        project_number=project_number,
        location=location,
        document_schema_id=document_schema_id,
    )

    assert response is None
