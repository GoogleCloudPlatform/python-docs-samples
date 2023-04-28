# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START generativeai_sdk_list_tuned_models]
from google.cloud.aiplatform.private_preview.language_models import TextGenerationModel, TextEmbeddingModel
from google.cloud import aiplatform

from typing import Union
import pandas as pd


def list_tuned_models(project_id, location):
    """List tuned models."""
    aiplatform.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("google/text-bison-001")
    tuned_model_names = model.list_tuned_model_names()
    print(tuned_model_names)
    # [END generativeai_sdk_list_tuned_models]
    return tuned_model_names


if __name__ == "__main__":
    list_tuned_models()