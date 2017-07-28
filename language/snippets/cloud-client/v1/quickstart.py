#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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
    # [START migration_import]
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    # [END migration_import]

    # Instantiates a client
    # [START migration_client]
    client = language.LanguageServiceClient()
    # [END migration_client]

    # The text to analyze
    text = u'Hello, world!'
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    # [END language_quickstart]


if __name__ == '__main__':
    run_quickstart()
