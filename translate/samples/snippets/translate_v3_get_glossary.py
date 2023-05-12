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

# [START translate_v3_get_glossary]
from google.cloud import translate_v3 as translate


def get_glossary(project_id="YOUR_PROJECT_ID", glossary_id="YOUR_GLOSSARY_ID"):
    """Get a particular glossary based on the glossary ID."""

    client = translate.TranslationServiceClient()

    name = client.glossary_path(project_id, "us-central1", glossary_id)

    response = client.get_glossary(name=name)
    print(f"Glossary name: {response.name}")
    print(f"Entry count: {response.entry_count}")
    print(f"Input URI: {response.input_config.gcs_source.input_uri}")


# [END translate_v3_get_glossary]
