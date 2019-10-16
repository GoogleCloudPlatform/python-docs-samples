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

# DO NOT EDIT! This is a generated sample ("LongRunningPromise",  "translate_v3_delete_glossary")

# To install the latest published package dependency, execute the following:
#   pip install google-cloud-translate

# sample-metadata
#   title: Delete Glossary
#   description: Delete Glossary
#   usage: python3 translate_v3_delete_glossary.py [--project_id "[Google Cloud Project ID]"] [--glossary_id "[Glossary ID]"]

# [START translate_v3_delete_glossary]
from google.cloud import translate_v3 as translate

def sample_delete_glossary(project_id, glossary_id):
    """Delete Glossary"""
    client = translate.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'GLOSSARY_ID'

    parent = client.glossary_path(
        project_id,
        'us-central1',
        glossary_id)

    operation = client.delete_glossary(parent)
    result = operation.result(timeout=90)
    print('Deleted: {}'.format(result.name))

# [END translate_v3_delete_glossary]


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--project_id", type=str, default="[Google Cloud Project ID]")
    parser.add_argument("--glossary_id", type=str, default="[Glossary ID]")
    args = parser.parse_args()

    sample_delete_glossary(args.project_id, args.glossary_id)


if __name__ == "__main__":
    main()