# Copyright 2024 Google LLC
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

import backoff

from google.api_core.exceptions import ResourceExhausted

from google.cloud import aiplatform

import pytest

from vertexai.language_models import TextGenerationModel

import pretrained_codegen_example
import pretrained_list_example
import pretrained_textgen_example


def teardown_model(tuned_model: TextGenerationModel) -> None:
    for tuned_model_name in tuned_model.list_tuned_model_names():
        model_registry = aiplatform.models.ModelRegistry(model=tuned_model_name)

        display_name = model_registry.get_version_info("1").model_display_name
        for endpoint in aiplatform.Endpoint.list():
            for _ in endpoint.list_models():
                if endpoint.display_name == display_name:
                    endpoint.undeploy_all()
                    endpoint.delete()
        aiplatform.Model(model_registry.model_resource_name).delete()


@pytest.mark.skip("Blocked on b/277959219")
def test_tuning_code_generation_model() -> None:
    """Takes approx. 20 minutes."""
    tuned_model = pretrained_codegen_example.tune_code_generation_model()
    try:
        assert tuned_model
    finally:
        teardown_model(tuned_model)


@pytest.mark.skip("Blocked on b/277959219")
def test_tuning() -> None:
    """Takes approx. 20 minutes."""
    tuned_model = pretrained_textgen_example.tuning()
    try:
        assert tuned_model
    finally:
        teardown_model(tuned_model)


@backoff.on_exception(backoff.expo, ResourceExhausted, max_time=10)
def test_list_tuned_models() -> None:
    tuned_model_names = pretrained_list_example.list_tuned_models()
    filtered_models_counter = 0
    for tuned_model_name in tuned_model_names:
        model_registry = aiplatform.models.ModelRegistry(model=tuned_model_name)
        if (
            "Vertex LLM Test Fixture "
            "(list_tuned_models_test.py::test_list_tuned_models)"
        ) in model_registry.get_version_info("1").model_display_name:
            filtered_models_counter += 1
    assert filtered_models_counter == 0
