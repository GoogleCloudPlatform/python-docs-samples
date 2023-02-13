#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dialogflow API Python sample showing how to manage Knowledge Documents.

Examples:
  python document_management.py -h
  python document_management.py --project-id PROJECT_ID \
  --knowledge-base-id knowledge_base_id \
  list
  python document_management.py --project-id PROJECT_ID \
  --knowledge-base-id knowledge_base_id \
  create --display-name DISPLAY_NAME --mime-type MIME_TYPE \
  --knowledge-type KNOWLEDGE_TYPE --content-uri CONTENT_URI
  python document_management.py --project-id PROJECT_ID \
  --knowledge-base-id knowledge_base_id \
  get --document-id DOCUMENT_ID
  python document_management.py --project-id PROJECT_ID \
  --knowledge-base-id knowledge_base_id \
  delete --document-id DOCUMENT_ID
"""

import argparse

KNOWLEDGE_TYPES = [
    "KNOWLEDGE_TYPE_UNSPECIFIED",
    "FAQ",
    "EXTRACTIVE_QA",
    "ARTICLE_SUGGESTION",
]


# [START dialogflow_list_document]
def list_documents(project_id, knowledge_base_id):
    """Lists the Documents belonging to a Knowledge base.

    Args:
        project_id: The GCP project linked with the agent.
        knowledge_base_id: Id of the Knowledge base."""
    from google.cloud import dialogflow_v2beta1 as dialogflow

    client = dialogflow.DocumentsClient()
    knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
        project_id, knowledge_base_id
    )

    print("Documents for Knowledge Id: {}".format(knowledge_base_id))
    response = client.list_documents(parent=knowledge_base_path)
    for document in response:
        print(" - Display Name: {}".format(document.display_name))
        print(" - Knowledge ID: {}".format(document.name))
        print(" - MIME Type: {}".format(document.mime_type))
        print(" - Knowledge Types:")
        for knowledge_type in document.knowledge_types:
            print("    - {}".format(KNOWLEDGE_TYPES[knowledge_type]))
        print(" - Source: {}\n".format(document.content_uri))
    return response


# [END dialogflow_list_document]


# [START dialogflow_create_document]]
def create_document(
    project_id, knowledge_base_id, display_name, mime_type, knowledge_type, content_uri
):
    """Creates a Document.

    Args:
        project_id: The GCP project linked with the agent.
        knowledge_base_id: Id of the Knowledge base.
        display_name: The display name of the Document.
        mime_type: The mime_type of the Document. e.g. text/csv, text/html,
            text/plain, text/pdf etc.
        knowledge_type: The Knowledge type of the Document. e.g. FAQ,
            EXTRACTIVE_QA.
        content_uri: Uri of the document, e.g. gs://path/mydoc.csv,
            http://mypage.com/faq.html."""
    from google.cloud import dialogflow_v2beta1 as dialogflow

    client = dialogflow.DocumentsClient()
    knowledge_base_path = dialogflow.KnowledgeBasesClient.knowledge_base_path(
        project_id, knowledge_base_id
    )

    document = dialogflow.Document(
        display_name=display_name, mime_type=mime_type, content_uri=content_uri
    )

    document.knowledge_types.append(
        getattr(dialogflow.Document.KnowledgeType, knowledge_type)
    )

    response = client.create_document(parent=knowledge_base_path, document=document)
    print("Waiting for results...")
    document = response.result(timeout=120)
    print("Created Document:")
    print(" - Display Name: {}".format(document.display_name))
    print(" - Knowledge ID: {}".format(document.name))
    print(" - MIME Type: {}".format(document.mime_type))
    print(" - Knowledge Types:")
    for knowledge_type in document.knowledge_types:
        print("    - {}".format(KNOWLEDGE_TYPES[knowledge_type]))
    print(" - Source: {}\n".format(document.content_uri))


# [END dialogflow_create_document]


# [START dialogflow_get_document]]
def get_document(project_id, knowledge_base_id, document_id):
    """Gets a Document.

    Args:
        project_id: The GCP project linked with the agent.
        knowledge_base_id: Id of the Knowledge base.
        document_id: Id of the Document."""
    from google.cloud import dialogflow_v2beta1 as dialogflow

    client = dialogflow.DocumentsClient()
    document_path = client.document_path(project_id, knowledge_base_id, document_id)

    response = client.get_document(name=document_path)
    print("Got Document:")
    print(" - Display Name: {}".format(response.display_name))
    print(" - Knowledge ID: {}".format(response.name))
    print(" - MIME Type: {}".format(response.mime_type))
    print(" - Knowledge Types:")
    for knowledge_type in response.knowledge_types:
        print("    - {}".format(KNOWLEDGE_TYPES[knowledge_type]))
    print(" - Source: {}\n".format(response.content_uri))
    return response


# [END dialogflow_get_document]]


# [START dialogflow_delete_document]]
def delete_document(project_id, knowledge_base_id, document_id):
    """Deletes a Document.

    Args:
        project_id: The GCP project linked with the agent.
        knowledge_base_id: Id of the Knowledge base.
        document_id: Id of the Document."""
    from google.cloud import dialogflow_v2beta1 as dialogflow

    client = dialogflow.DocumentsClient()
    document_path = client.document_path(project_id, knowledge_base_id, document_id)

    response = client.delete_document(name=document_path)
    print("operation running:\n {}".format(response.operation))
    print("Waiting for results...")
    print("Done.\n {}".format(response.result()))


# [END dialogflow_delete_document]]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--project-id", help="Project id.  Required.", required=True)
    parser.add_argument(
        "--knowledge-base-id",
        help="The id of the Knowledge Base that the Document belongs to",
        required=True,
    )

    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser(
        "list", help="List all Documents that belong to a certain Knowledge base."
    )

    create_parser = subparsers.add_parser(
        "create", help="Create a Document for a certain Knowledge base."
    )
    create_parser.add_argument(
        "--display-name",
        help="A name of the Document, mainly used for display purpose, "
        "can not be used to identify the Document.",
        default=str(""),
    )
    create_parser.add_argument(
        "--mime-type",
        help="The mime-type of the Document, e.g. text/csv, text/html, "
        "text/plain, text/pdf etc. ",
        required=True,
    )
    create_parser.add_argument(
        "--knowledge-type",
        help="The knowledge-type of the Document, e.g. FAQ, EXTRACTIVE_QA.",
        required=True,
    )
    create_parser.add_argument(
        "--content-uri",
        help="The uri of the Document, e.g. gs://path/mydoc.csv, "
        "http://mypage.com/faq.html",
        required=True,
    )

    get_parser = subparsers.add_parser(
        "get", help="Get a Document by its id and the Knowledge base id."
    )
    get_parser.add_argument(
        "--document-id", help="The id of the Document", required=True
    )

    delete_parser = subparsers.add_parser(
        "delete", help="Delete a Document by its id and the Knowledge base" "id."
    )
    delete_parser.add_argument(
        "--document-id", help="The id of the Document you want to delete", required=True
    )

    args = parser.parse_args()

    if args.command == "list":
        list_documents(args.project_id, args.knowledge_base_id)
    elif args.command == "create":
        create_document(
            args.project_id,
            args.knowledge_base_id,
            args.display_name,
            args.mime_type,
            args.knowledge_type,
            args.content_uri,
        )
    elif args.command == "get":
        get_document(args.project_id, args.knowledge_base_id, args.document_id)
    elif args.command == "delete":
        delete_document(args.project_id, args.knowledge_base_id, args.document_id)
