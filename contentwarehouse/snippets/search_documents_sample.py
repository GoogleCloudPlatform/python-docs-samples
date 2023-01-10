# Copyright 2023 Google LLC
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


# [START contentwarehouse_search_documents]

from typing import MutableSequence

from google.cloud import contentwarehouse

# TODO(developer): Uncomment these variables before running the sample.
# project_number = 'YOUR_PROJECT_NUMBER'
# location = 'YOUR_PROJECT_LOCATION' # Format is 'us' or 'eu'
# document_query_text = 'YOUR_DOCUMENT_QUERY'
# file_type = contentwarehouse.FileTypeFilter.FileType.DOCUMENT # Options: DOCUMENT, FOLDER
# histogram_query_text = 'YOUR_HISTOGRAM_QUERY' # e.g. 'count(\"DocumentSchemaId\")'


def search_documents_sample(
    project_number: str,
    location: str,
    document_query_text: str,
    file_type: contentwarehouse.FileTypeFilter.FileType,
    histogram_query_text: str,
) -> None:

    # Create a client
    client = contentwarehouse.DocumentServiceClient()

    # The full resource name of the location, e.g.:
    # projects/{project_number}/locations/{location}
    parent = client.common_location_path(project=project_number, location=location)

    # File Type Filter
    file_type_filter = contentwarehouse.FileTypeFilter(file_type=file_type)

    # Document Text Query
    document_query = contentwarehouse.DocumentQuery(
        query=document_query_text,
        file_type_filter=file_type_filter,
    )

    # Histogram Query
    histogram_query = contentwarehouse.HistogramQuery(
        histogram_query=histogram_query_text
    )

    # Define request
    request = contentwarehouse.SearchDocumentsRequest(
        parent=parent,
        document_query=document_query,
        histogram_queries=[histogram_query],
    )

    # Make the request
    response = client.search_documents(request=request)

    # Handle the response
    print_search_results(response.matching_documents)
    print_histogram_results(response.histogram_query_results)


def print_search_results(
    matching_documents: MutableSequence[
        contentwarehouse.SearchDocumentsResponse.MatchingDocument
    ],
) -> None:
    for matching_document in matching_documents:
        document = matching_document.document
        # Display name - schema display name.
        # Name.
        # Create date.
        # Snippet - keywords are highlighted with <b> & </b>.
        print(
            f"{document.display_name} - {document.document_schema_name}\n"
            f"{document.name}\n"
            f"{document.create_time}\n"
            f"{matching_document.search_text_snippet}\n"
        )


def print_histogram_results(
    histogram_query_results: MutableSequence[contentwarehouse.HistogramQueryResult],
) -> None:
    for histogram_query_result in histogram_query_results:
        print(
            f"Histogram Query: {histogram_query_result.histogram_query}\n"
            f"| {'Schema':<70} | {'Count':<15} |"
        )
        for key, value in histogram_query_result.histogram.items():
            print(f"| {key:<70} | {value:<15} |")


# [END contentwarehouse_search_documents]
