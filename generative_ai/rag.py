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

from typing import List, Optional


def create_corpus(
    project_id: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
):
    # [START generativeaionvertexai_rag_create_corpus]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # display_name = "test_corpus"
    # description = "Corpus Description"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    corpus = rag.create_corpus(display_name=display_name, description=description)
    print(corpus)
    # [END generativeaionvertexai_rag_create_corpus]
    return corpus


def get_corpus(project_id: str, corpus_name: str):
    # [START generativeaionvertexai_rag_get_corpus]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    corpus = rag.get_corpus(name=corpus_name)
    print(corpus)
    # [END generativeaionvertexai_rag_get_corpus]
    return corpus


def list_corpora(project_id: str):
    # [START generativeaionvertexai_rag_list_corpora]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    corpora = rag.list_corpora()
    print(corpora)
    # [END generativeaionvertexai_rag_list_corpora]
    return corpora


def upload_file(
    project_id: str,
    corpus_name: str,
    path: str,
    display_name: Optional[str] = None,
    description: Optional[str] = None,
):
    # [START generativeaionvertexai_rag_upload_file]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    # path = "path/to/local/file.txt"
    # display_name = "file_display_name"
    # description = "file description"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=path,
        display_name=display_name,
        description=description,
    )
    print(rag_file)
    # [END generativeaionvertexai_rag_upload_file]
    return rag_file


def import_files(
    project_id: str,
    corpus_name: str,
    paths: List[str],
):
    # [START generativeaionvertexai_rag_import_files]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"
    # paths = ["https://drive.google.com/file/123", "gs://my_bucket/my_files_dir"]  # Supports Google Cloud Storage and Google Drive Links

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    response = rag.import_files(
        corpus_name=corpus_name,
        paths=paths,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
    )
    print(f"Imported {response.imported_rag_files_count} files.")
    # [END generativeaionvertexai_rag_import_files]
    return response


async def import_files_async(
    project_id: str,
    corpus_name: str,
    paths: List[str],
):
    # [START generativeaionvertexai_rag_import_files_async]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Supports Google Cloud Storage and Google Drive Links
    # paths = ["https://drive.google.com/file/123", "gs://my_bucket/my_files_dir"]

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    response = await rag.import_files_async(
        corpus_name=corpus_name,
        paths=paths,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
    )

    result = await response.result()
    print(f"Imported {result.imported_rag_files_count} files.")
    # [END generativeaionvertexai_rag_import_files_async]
    return result


def get_file(project_id: str, file_name: str):
    # [START generativeaionvertexai_rag_get_file]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # file_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}/ragFiles/{rag_file_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    rag_file = rag.get_file(name=file_name)
    print(rag_file)
    # [END generativeaionvertexai_rag_get_file]

    return rag_file


def list_files(project_id: str, corpus_name: str):
    # [START generativeaionvertexai_rag_list_files]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    files = rag.list_files(corpus_name=corpus_name)
    for file in files:
        print(file)
    # [END generativeaionvertexai_rag_list_files]

    return files


def delete_file(project_id: str, file_name: str) -> None:
    # [START generativeaionvertexai_rag_delete_file]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # file_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}/ragFiles/{rag_file_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    rag.delete_file(name=file_name)
    print(f"File {file_name} deleted.")
    # [END generativeaionvertexai_rag_delete_file]


def delete_corpus(project_id: str, corpus_name: str) -> None:
    # [START generativeaionvertexai_rag_delete_corpus]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # corpus_name = "projects/{project_id}/locations/us-central1/ragCorpora/{rag_corpus_id}"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    rag.delete_corpus(name=corpus_name)
    print(f"Corpus {corpus_name} deleted.")
    # [END generativeaionvertexai_rag_delete_corpus]


def retrieval_query(
    project_id: str,
    rag_corpora: List[str],
    text: str,
):
    # [START generativeaionvertexai_rag_retrieval_query]

    from vertexai.preview import rag
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # rag_corpora = ["9183965540115283968"] # Only one corpus is supported at this time
    # text = "Your Query"

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    response = rag.retrieval_query(
        rag_corpora=rag_corpora,
        text=text,
        similarity_top_k=10,  # Optional
    )
    print(response)
    # [END generativeaionvertexai_rag_retrieval_query]

    return response


def generate_content_with_rag(
    project_id: str,
    rag_corpora: List[str],
):
    # [START generativeaionvertexai_rag_generate_content]

    from vertexai.preview import rag
    from vertexai.preview.generative_models import GenerativeModel, Tool
    import vertexai

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # rag_corpora = ["9183965540115283968"] # Only one corpus is supported at this time

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=rag_corpora,
                similarity_top_k=3,  # Optional
                # vector_distance_threshold=0.3,  # Optional
            ),
        )
    )

    rag_model = GenerativeModel(
        model_name="gemini-1.0-pro-002", tools=[rag_retrieval_tool]
    )
    response = rag_model.generate_content("Why is the sky blue?")
    print(response.text)
    # [END generativeaionvertexai_rag_generate_content]

    return response


def quickstart(
    project_id: str,
    display_name: str,
    paths: List[str],
):
    # [START generativeaionvertexai_rag_quickstart]
    from vertexai.preview import rag
    from vertexai.preview.generative_models import GenerativeModel, Tool
    import vertexai

    # Create a RAG Corpus, Import Files, and Generate a response

    # TODO(developer): Update and un-comment below lines
    # project_id = "PROJECT_ID"
    # display_name = "test_corpus"
    # paths = ["https://drive.google.com/file/123", "gs://my_bucket/my_files_dir"]  # Supports Google Cloud Storage and Google Drive Links

    # Initialize Vertex AI API once per session
    vertexai.init(project=project_id, location="us-central1")

    # Create RagCorpus
    rag_corpus = rag.create_corpus(display_name=display_name)

    # Import Files to the RagCorpus
    response = rag.import_files(
        rag_corpus.name,
        paths,
        chunk_size=512,  # Optional
        chunk_overlap=100,  # Optional
    )

    # Direct context retrieval
    response = rag.retrieval_query(
        rag_corpora=[rag_corpus.name],
        text="What is RAG and why it is helpful?",
        similarity_top_k=10,
    )
    print(response)

    # Enhance generation
    # Create a RAG retrieval tool
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_corpora=[rag_corpus.name],  # Currently only 1 corpus is allowed.
                similarity_top_k=3,  # Optional
                # vector_distance_threshold=0.4,  # Optional
            ),
        )
    )
    # Create a gemini-pro model instance
    rag_model = GenerativeModel(
        model_name="gemini-1.0-pro-002", tools=[rag_retrieval_tool]
    )

    # Generate response
    response = rag_model.generate_content("What is RAG and why it is helpful?")
    print(response.text)
    # [END generativeaionvertexai_rag_quickstart]
    return rag_corpus, response
