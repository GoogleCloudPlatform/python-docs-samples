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

# DO NOT EDIT! This is a generated sample ("Request",  "language_entities_text")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-language

# sample-metadata
#   title: Analyzing Entities
#   description: Analyzing Entities in a String
#   usage: python3 samples/v1/language_entities_text.py [--text_content "California is a state."]

# [START language_entities_text]
from google.cloud import language_v1


def sample_analyze_entities(text_content):
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(
        request={"document": document, "encoding_type": encoding_type}
    )

    # Loop through entitites returned from the API
    for entity in response.entities:
        print("Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print("Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        print("Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print("{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print("Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            print(
                "Mention type: {}".format(
                    language_v1.EntityMention.Type(mention.type_).name
                )
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print("Language of the text: {}".format(response.language))


# [END language_entities_text]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text_content", type=str, default="California is a state.")
    args = parser.parse_args()

    sample_analyze_entities(args.text_content)


if __name__ == "__main__":
    main()
