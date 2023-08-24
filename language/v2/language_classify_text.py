#
# Copyright 2023 Google LLC
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

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-language

# sample-metadata
#   title: Classify Content
#   description: Classifying Content in a String

# [START language_classify_text]
from google.cloud import language_v2


def sample_classify_text(
    text_content: str = "That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows.",
) -> None:
    """
    Classifies Content in a string.

    Args:
      text_content: The text content to analyze.
    """

    client = language_v2.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language_code = "en"
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    response = client.classify_text(request={"document": document})
    # Loop through classified categories returned from the API
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print(f"Category name: {category.name}")
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        print(f"Confidence: {category.confidence}")


# [END language_classify_text]
