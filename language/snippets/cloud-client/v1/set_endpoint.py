# Copyright 2019 Google LLC
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


def set_endpoint():
    """Change your endpoint"""
    # [START language_set_endpoint]
    # Imports the Google Cloud client library
    from google.cloud import language_v1

    client_options = {"api_endpoint": "eu-language.googleapis.com:443"}

    # Instantiates a client
    client = language_v1.LanguageServiceClient(client_options=client_options)
    # [END language_set_endpoint]

    # The text to analyze
    document = language_v1.Document(
        content="Hello, world!", type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))


if __name__ == "__main__":
    set_endpoint()
