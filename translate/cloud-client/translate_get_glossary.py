# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

# DO NOT EDIT! This is a generated sample ("Request",  "translate_get_glossary")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Get Glossary
#   description: Get Glossary
#   usage: python3 samples/v3beta1/translate_get_glossary.py [--project_id "[Google Cloud Project ID]"] [--glossary_id "[Glossary ID]"]

# [START translate_get_glossary]
from google.cloud import translate_v3

def sample_get_glossary(project_id, glossary_id):
    """Get Glossary"""

    client = translate_v3.TranslationServiceClient()

    # project = '[Google Cloud Project ID]'
    # glossary_id = '[Glossary ID]'
    name = client.glossary_path(project_id, "us-central1", glossary_id)

    response = client.get_glossary(name)
    print(u"Glossary name: {}".format(response.name))
    print(u"Entry count: {}".format(response.entry_count))
    print(u"Input URI: {}".format(response.input_config.gcs_source.input_uri))

# [END translate_get_glossary]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--glossary_id", type=str, default="[Glossary ID]")
    args = parser.parse_args()

    sample_get_glossary(args.project_id, args.glossary_id)


if __name__ == "__main__":
    main()
