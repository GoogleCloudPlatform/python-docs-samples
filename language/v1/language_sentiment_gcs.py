#
# Copyright 2020 Google LLC
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

# DO NOT EDIT! This is a generated sample ("Request",  "language_sentiment_gcs")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-language

# sample-metadata
#   title: Analyzing Sentiment (GCS)
#   description: Analyzing Sentiment in text file stored in Cloud Storage
#   usage: python3 samples/v1/language_sentiment_gcs.py [--gcs_content_uri "gs://cloud-samples-data/language/sentiment-positive.txt"]

# [START language_sentiment_gcs]
from google.cloud import language_v1


def sample_analyze_sentiment(gcs_content_uri):
    """
    Analyzing Sentiment in text file stored in Cloud Storage

    Args:
      gcs_content_uri Google Cloud Storage URI where the file content is located.
      e.g. gs://[Your Bucket]/[Path to File]
    """

    client = language_v1.LanguageServiceClient()

    # gcs_content_uri = 'gs://cloud-samples-data/language/sentiment-positive.txt'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {
        "gcs_content_uri": gcs_content_uri,
        "type_": type_,
        "language": language,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    # Get overall sentiment of the input document
    print(f"Document sentiment score: {response.document_sentiment.score}")
    print(
        f"Document sentiment magnitude: {response.document_sentiment.magnitude}"
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(f"Sentence text: {sentence.text.content}")
        print(f"Sentence sentiment score: {sentence.sentiment.score}")
        print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(f"Language of the text: {response.language}")


# [END language_sentiment_gcs]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gcs_content_uri",
        type=str,
        default="gs://cloud-samples-data/language/sentiment-positive.txt",
    )
    args = parser.parse_args()

    sample_analyze_sentiment(args.gcs_content_uri)


if __name__ == "__main__":
    main()
