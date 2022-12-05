#!/usr/bin/env python

# Copyright 2016 Google LLC
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


def run_quickstart():
    # [START language_quickstart]
    # Imports the Google Cloud client library
    # [START language_python_migration_imports]
    from google.cloud import language_v1

    # [END language_python_migration_imports]
    # Instantiates a client
    # [START language_python_migration_client]
    client = language_v1.LanguageServiceClient()
    # [END language_python_migration_client]

    # The text to analyze
    text = "Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    # [END language_quickstart]


if __name__ == "__main__":
    run_quickstart()
