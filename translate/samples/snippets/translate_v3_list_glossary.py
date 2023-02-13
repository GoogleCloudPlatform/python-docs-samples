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

# [START translate_v3_list_glossary]
from google.cloud import translate


def list_glossaries(project_id="YOUR_PROJECT_ID"):
    """List Glossaries."""

    client = translate.TranslationServiceClient()

    location = "us-central1"

    parent = f"projects/{project_id}/locations/{location}"

    # Iterate over all results
    for glossary in client.list_glossaries(parent=parent):
        print("Name: {}".format(glossary.name))
        print("Entry count: {}".format(glossary.entry_count))
        print("Input uri: {}".format(glossary.input_config.gcs_source.input_uri))

        # Note: You can create a glossary using one of two modes:
        # language_code_set or language_pair. When listing the information for
        # a glossary, you can only get information for the mode you used
        # when creating the glossary.
        for language_code in glossary.language_codes_set.language_codes:
            print("Language code: {}".format(language_code))


# [END translate_v3_list_glossary]
