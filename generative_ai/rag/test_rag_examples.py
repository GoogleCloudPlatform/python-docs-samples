# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: Rename the test file to rag_test.py after deleting /generative_ai/rag_test.py
import os
from pathlib import Path

import pytest
import vertexai

import create_corpus_example
import delete_corpus_example
import delete_file_example
import generate_content_example
import get_corpus_example
import get_file_example
import import_files_async_example
import import_files_example
import list_corpora_example
import list_files_example
import quickstart_example
import retrieval_query_example
import upload_file_example


# TODO(https://github.com/GoogleCloudPlatform/python-docs-samples/issues/11557): Remove once Allowlist is removed
pytest.skip(allow_module_level=True)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
GCS_FILE = "gs://cloud-samples-data/generative-ai/pdf/earnings_statement.pdf"


vertexai.init(project=PROJECT_ID, location=LOCATION)


@pytest.fixture(scope="module", name="test_file")
def test_file_fixture() -> None:
    file_path = Path("./hello.txt")
    file_path.write_text("Hello World", encoding="utf-8")
    yield file_path.absolute().as_posix()
    file_path.unlink()  # Delete the file after tests


@pytest.fixture(scope="module", name="test_corpus")
def test_corpus_fixture() -> None:
    """Creates a corpus for testing and deletes it after tests are complete."""
    corpus = create_corpus_example.create_corpus("test_corpus")
    yield corpus
    delete_corpus_example.delete_corpus(corpus.name)


@pytest.fixture(scope="module", name="uploaded_file")
def uploaded_file_fixture(
    test_corpus: pytest.fixture, test_file: pytest.fixture
) -> None:
    """Uploads a file to the corpus and deletes it after the test."""
    rag_file = upload_file_example.upload_file(test_corpus.name, test_file)
    yield rag_file
    delete_file_example.delete_file(rag_file.name)


def test_create_corpus() -> None:
    corpus = create_corpus_example.create_corpus("test_create_corpus")
    assert corpus.display_name == "test_create_corpus"
    delete_corpus_example.delete_corpus(corpus.name)


def test_get_corpus(test_corpus: pytest.fixture) -> None:
    retrieved_corpus = get_corpus_example.get_corpus(test_corpus.name)
    assert retrieved_corpus.name == test_corpus.name


def test_list_corpora(test_corpus: pytest.fixture) -> None:
    corpora = list_corpora_example.list_corpora()
    assert any(c.display_name == test_corpus.display_name for c in corpora)


def test_upload_file(test_corpus: pytest.fixture, test_file: pytest.fixture) -> None:
    rag_file = upload_file_example.upload_file(test_corpus.name, test_file)
    assert rag_file
    files = list_files_example.list_files(test_corpus.name)
    imported_file = next(iter(files))
    delete_file_example.delete_file(imported_file.name)


def test_import_files(test_corpus: pytest.fixture) -> None:
    response = import_files_example.import_files(test_corpus.name, [GCS_FILE])
    assert response.imported_rag_files_count > 0
    files = list_files_example.list_files(test_corpus.name)
    imported_file = next(iter(files))
    delete_file_example.delete_file(imported_file.name)


@pytest.mark.asyncio
async def test_import_files_async(test_corpus: pytest.fixture) -> None:
    result = await import_files_async_example.import_files_async(
        test_corpus.name, [GCS_FILE]
    )
    assert result.imported_rag_files_count > 0
    files = list_files_example.list_files(test_corpus.name)
    imported_file = next(iter(files))
    delete_file_example.delete_file(imported_file.name)


def test_get_file(uploaded_file: pytest.fixture) -> None:
    retrieved_file = get_file_example.get_file(uploaded_file.name)
    assert retrieved_file.name == uploaded_file.name


def test_list_files(test_corpus: pytest.fixture, uploaded_file: pytest.fixture) -> None:
    files = list_files_example.list_files(test_corpus.name)
    assert any(f.name == uploaded_file.name for f in files)


def test_retrieval_query(test_corpus: pytest.fixture) -> None:
    response = retrieval_query_example.retrieval_query(test_corpus.name)
    assert response
    assert response.contexts


def test_generate_content_with_rag(test_corpus: pytest.fixture) -> None:
    response = generate_content_example.generate_content_with_rag(test_corpus.name)
    assert response
    assert response.text


def test_quickstart() -> None:
    corpus, response = quickstart_example.quickstart(
        "test_corpus_quickstart", [GCS_FILE]
    )
    assert response
    assert response.text
    delete_corpus_example.delete_corpus(corpus.name)
