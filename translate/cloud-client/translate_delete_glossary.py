# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START translate_delete_glossary]
from google.cloud import translate_v3


def delete_glossary(project_id, glossary_id):
    """Delete Glossary"""
    client = translate_v3.TranslationServiceClient()

    # project_id = 'YOUR_PROJECT_ID'
    # glossary_id = 'GLOSSARY_ID'

    parent = client.glossary_path(project_id, "us-central1", glossary_id)

    operation = client.delete_glossary(parent)
    result = operation.result(timeout=90)
    print("Deleted: {}".format(result.name))


# [END translate_delete_glossary]
