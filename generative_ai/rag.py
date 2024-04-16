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


# [START generativeaionvertexai_rag_create_corpus]
# [START generativeaionvertexai_rag_get_corpus]
# [START generativeaionvertexai_rag_list_corpora]
# [START generativeaionvertexai_rag_upload_file]
# [START generativeaionvertexai_rag_import_files]
# [START generativeaionvertexai_rag_get_file]
# [START generativeaionvertexai_rag_list_files]
# [START generativeaionvertexai_rag_delete_file]
# [START generativeaionvertexai_rag_delete_corpus]
# [START generativeaionvertexai_rag_retrieval_query]
# [START generativeaionvertexai_rag_generate_content]

from typing import List, Union, Optional

from google.cloud.aiplatform.private_preview.vertex_rag import rag
import vertexai

# [END generativeaionvertexai_rag_create_corpus]
# [END generativeaionvertexai_rag_get_corpus]
# [END generativeaionvertexai_rag_list_corpora]
# [END generativeaionvertexai_rag_upload_file]
# [END generativeaionvertexai_rag_import_files]
# [END generativeaionvertexai_rag_get_file]
# [END generativeaionvertexai_rag_list_files]
# [END generativeaionvertexai_rag_delete_file]
# [END generativeaionvertexai_rag_delete_corpus]
# [END generativeaionvertexai_rag_retrieval_query]
# [END generativeaionvertexai_rag_generate_content]


# [START generativeaionvertexai_rag_create_corpus]
def create_corpus(
    project_id: str,
    location: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    corpus = rag.create_corpus(display_name=display_name, description=description)
    print(corpus)
    return corpus


# [END generativeaionvertexai_rag_create_corpus]


# [START generativeaionvertexai_rag_get_corpus]
def get_corpus(project_id: str, location: str, corpus_name: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    corpus = rag.get_corpus(name=corpus_name)
    print(corpus)
    return corpus


# [END generativeaionvertexai_rag_get_corpus]


# [START generativeaionvertexai_rag_list_corpora]
def list_corpora(project_id: str, location: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    corpora = rag.list_corpora()
    print(corpora)
    return corpora


# [END generativeaionvertexai_rag_list_corpora]


# [START generativeaionvertexai_rag_upload_file]
def upload_file(
    project_id: str,
    location: str,
    corpus_name: str,
    path: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=path,
        display_name=display_name,
        description=description,
    )
    print(rag_file)
    return rag_file


# [END generativeaionvertexai_rag_upload_file]


# [START generativeaionvertexai_rag_import_files]
def import_files(
    project_id: str,
    location: str,
    corpus_name: str,
    path: Union[str, List[str]],
    chunk_size: Optional[int] = 1024,
    chunk_overlap: Optional[int] = 200,
):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    response = rag.import_files(
        corpus_name=corpus_name,
        path=path,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    print(f"Imported {response.imported_rag_files_count} files.")
    return response


# [END generativeaionvertexai_rag_import_files]


# [START generativeaionvertexai_rag_get_file]
def get_file(project_id: str, location: str, file_name: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    rag_file = rag.get_file(name=file_name)
    print(rag_file)
    return rag_file


# [END generativeaionvertexai_rag_get_file]


# [START generativeaionvertexai_rag_list_files]
def list_files(project_id: str, location: str, corpus_name: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    files = rag.list_files(corpus_name=corpus_name)
    for file in files:
        print(file)
    return files


# [END generativeaionvertexai_rag_list_files]


# [START generativeaionvertexai_rag_delete_file]
def delete_file(project_id: str, location: str, file_name: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    rag.delete_file(name=file_name)
    print(f"File {file_name} deleted.")


# [END generativeaionvertexai_rag_delete_file]


# [START generativeaionvertexai_rag_delete_corpus]
def delete_corpus(project_id: str, location: str, corpus_name: str):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    rag.delete_corpus(name=corpus_name)
    print(f"Corpus {corpus_name} deleted.")


# [END generativeaionvertexai_rag_delete_corpus]


# [START generativeaionvertexai_rag_retrieval_query]
def retrieval_query(
    project_id: str,
    location: str,
    rag_corpus: str,
    text: str,
    similarity_top_k: Optional[int] = 10,
):
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    response = rag.retrieval_query(
        rag_corpora=rag_corpus, text=text, similarity_top_k=similarity_top_k
    )
    print(response)
    return response


# [END generativeaionvertexai_rag_retrieval_query]


# [START generativeaionvertexai_rag_generate_content]
from vertexai.preview.generative_models import GenerativeModel, Tool


def generate_content_with_rag(
    project_id: str, location: str, corpus_display_name: str, paths: List[str]
):
    """
    Creates and loads a RAG Corpus and generates text using Gemini.

    Args:
        project_id (str): The project ID for Vertex AI.
        location (str): The location for Vertex AI resources.
        corpus_display_name (str): The display name for the corpus to be created.
        paths (List[str]): List of file paths to import into the corpus.
            Supports GCS URIs `gs://my-bucket/my_file` and Google Drive URLs
            `https://drive.google.com/file/123`
    """
    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    corpus = rag.create_corpus(display_name=corpus_display_name)

    response = rag.import_files(
        corpus.name,
        paths,
        chunk_size=1024,
        chunk_overlap=200,
    )

    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=corpus.name,  # Only 1 corpus is allowed.
                similarity_top_k=3,
            ),
        )
    )

    rag_model = GenerativeModel("gemini-1.0-pro", tools=[rag_retrieval_tool])
    response = rag_model.generate_content("Why is the sky blue?")
    print(response.text)
    return response


# [END generativeaionvertexai_rag_generate_content]
