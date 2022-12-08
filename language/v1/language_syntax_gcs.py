# -*- coding: utf-8 -*-
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

# DO NOT EDIT! This is a generated sample ("Request",  "language_syntax_gcs")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-language

# sample-metadata
#   title: Analyzing Syntax (GCS)
#   description: Analyzing Syntax in text file stored in Cloud Storage
#   usage: python3 samples/v1/language_syntax_gcs.py [--gcs_content_uri "gs://cloud-samples-data/language/syntax-sentence.txt"]

# [START language_syntax_gcs]
from google.cloud import language_v1


def sample_analyze_syntax(gcs_content_uri):
    """
    Analyzing Syntax in text file stored in Cloud Storage

    Args:
      gcs_content_uri Google Cloud Storage URI where the file content is located.
      e.g. gs://[Your Bucket]/[Path to File]
    """

    client = language_v1.LanguageServiceClient()

    # gcs_content_uri = 'gs://cloud-samples-data/language/syntax-sentence.txt'

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

    response = client.analyze_syntax(
        request={"document": document, "encoding_type": encoding_type}
    )
    # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        print("Token text: {}".format(text.content))
        print(
            "Location of this token in overall document: {}".format(text.begin_offset)
        )
        # Get the part of speech information for this token.
        # Part of speech is defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        print(
            "Part of Speech tag: {}".format(
                language_v1.PartOfSpeech.Tag(part_of_speech.tag).name
            )
        )
        # Get the voice, e.g. ACTIVE or PASSIVE
        print(
            "Voice: {}".format(
                language_v1.PartOfSpeech.Voice(part_of_speech.voice).name
            )
        )
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        print(
            "Tense: {}".format(
                language_v1.PartOfSpeech.Tense(part_of_speech.tense).name
            )
        )
        # See API reference for additional Part of Speech information available
        # Get the lemma of the token. Wikipedia lemma description
        # https://en.wikipedia.org/wiki/Lemma_(morphology)
        print("Lemma: {}".format(token.lemma))
        # Get the dependency tree parse information for this token.
        # For more information on dependency labels:
        # http://www.aclweb.org/anthology/P13-2017
        dependency_edge = token.dependency_edge
        print("Head token index: {}".format(dependency_edge.head_token_index))
        print(
            "Label: {}".format(
                language_v1.DependencyEdge.Label(dependency_edge.label).name
            )
        )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print("Language of the text: {}".format(response.language))


# [END language_syntax_gcs]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gcs_content_uri",
        type=str,
        default="gs://cloud-samples-data/language/syntax-sentence.txt",
    )
    args = parser.parse_args()

    sample_analyze_syntax(args.gcs_content_uri)


if __name__ == "__main__":
    main()
