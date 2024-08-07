# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START apikeys_authenticate_api_key]

from google.cloud import language_v1


def authenticate_with_api_key(api_key_string: str) -> None:
    """
    Authenticates with an API key for Google Language service.

    TODO(Developer): Replace this variable before running the sample.

    Args:
        api_key_string: The API key to authenticate to the service.
    """

    # Initialize the Language Service client and set the API key
    client = language_v1.LanguageServiceClient(
        client_options={"api_key": api_key_string}
    )

    text = "Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Make a request to analyze the sentiment of the text.
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print(f"Text: {text}")
    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")
    print("Successfully authenticated using the API key")


# [END apikeys_authenticate_api_key]
