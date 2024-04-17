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

# flake8: noqa ANN001, ANN201

import os
from pathlib import Path

import pytest
import rag
import vertexai

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
GCS_FILE = "gs://cloud-samples-data/generative-ai/pdf/earnings_statement.pdf"

vertexai.init(project=PROJECT_ID, location=LOCATION)


@pytest.fixture(scope="module", name="test_file")
def test_file_fixture():
    file_path = Path("./hello.txt")
    file_path.write_text("Hello World", encoding="utf-8")
    yield file_path.absolute().as_posix()
    file_path.unlink()  # Delete the file after tests


@pytest.fixture(scope="module", name="test_corpus")
def test_corpus_fixture():
    """Creates a corpus for testing and deletes it after tests are complete."""
    corpus = rag.create_corpus(PROJECT_ID, "test_corpus")
    yield corpus
    rag.delete_corpus(PROJECT_ID, corpus.name)


@pytest.fixture(scope="module", name="uploaded_file")
def uploaded_file_fixture(test_corpus, test_file):
    """Uploads a file to the corpus and deletes it after the test."""
    rag_file = rag.upload_file(PROJECT_ID, test_corpus.name, test_file)
    yield rag_file
    rag.delete_file(PROJECT_ID, rag_file.name)


def test_create_corpus():
    corpus = rag.create_corpus(PROJECT_ID, "test_create_corpus")
    assert corpus.display_name == "test_create_corpus"
    rag.delete_corpus(PROJECT_ID, corpus.name)


def test_get_corpus(test_corpus):
    retrieved_corpus = rag.get_corpus(PROJECT_ID, test_corpus.name)
    assert retrieved_corpus.name == test_corpus.name


def test_list_corpora(test_corpus):
    corpora = rag.list_corpora(PROJECT_ID)
    assert any(c.name == test_corpus.name for c in corpora)


def test_upload_file(test_corpus, test_file):
    rag_file = rag.upload_file(PROJECT_ID, test_corpus.name, test_file)
    assert rag_file


def test_import_files(test_corpus):
    response = rag.import_files(PROJECT_ID, test_corpus.name, [GCS_FILE])
    assert response.imported_rag_files_count > 0


# def test_import_files_async(test_corpus):
#     response = rag.import_files_async(PROJECT_ID, test_corpus.name, [GCS_FILE])
#     assert response


def test_get_file(uploaded_file):
    retrieved_file = rag.get_file(PROJECT_ID, uploaded_file.name)
    assert retrieved_file.name == uploaded_file.name


def test_list_files(test_corpus, uploaded_file):
    files = rag.list_files(PROJECT_ID, test_corpus.name)
    assert any(f.name == uploaded_file.name for f in files)


def test_retrieval_query(test_corpus):
    response = rag.retrieval_query(PROJECT_ID, [test_corpus.name], "test query")
    assert response
    assert response.contexts


def test_generate_content_with_rag(test_corpus):
    response = rag.generate_content_with_rag(PROJECT_ID, [test_corpus.name])
    assert response
    assert response.text


def test_quickstart():
    corpus, response = rag.quickstart(
        PROJECT_ID, "test_corpus_generate_content", [GCS_FILE]
    )
    assert response
    assert response.text
    rag.delete_corpus(PROJECT_ID, corpus.name)
