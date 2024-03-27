# Copyright 2024 Google LLC
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

# [START translate_v3_create_adaptive_mt_dataset]
from google.cloud import translate_v3 as translate


def create_adaptive_mt_dataset(
    project_id: str = "YOUR_PROJECT_ID",
    dataset_id: str = "YOUR_DATASET_ID",
    display_name: str = "YOUR_DATASET_DISPLAY_NAME",
    timeout: int = 180,
) -> translate.AdaptiveMtDataset:
    """
    Create an Adaptive MT dataset.
    https://cloud.google.com/translate/docs/advanced/glossary#format-glossary
    """
    client = translate.TranslationServiceClient()

    # Supported language codes: https://cloud.google.com/translate/docs/languages#adaptive_translation
    source_lang_code = "en"
    target_lang_code = "es"
    location = "us-central1"  # The location of the glossary

    name = client.adaptive_mt_dataset_path(project_id, location, dataset_id)

    parent = f"projects/{project_id}/locations/{location}"
    adaptive_mt_dataset = translate.AdaptiveMtDataset(
        name=name,
        display_name=display_name,
        source_language_code=source_lang_code,
        target_language_code=target_lang_code,
        timeout=timeout
    )

    response = client.create_adaptive_mt_dataset(
        parent=parent, adaptive_mt_dataset=adaptive_mt_dataset
    )

    print(f"Created: {response}")
    return response


# [END translate_v3_create_adaptive_mt_dataset]
