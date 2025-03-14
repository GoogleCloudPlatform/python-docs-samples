# Copyright 2025 Google LLC
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


import list_deployable_models_example
import list_deployment_options_example
import default_deploy_example


def test_list_deployable_models() -> None:
	models = list_deployable_models_example.list_deployable_models(model_filter="gemma")
	assert len(models) > 0
	assert "gemma" in models[0]


def test_list_deploy_options() -> None:
	deploy_options = list_deployment_options_example.list_deploy_options(model="google/gemma3@gemma-3-1b-it")
	assert len(deploy_options) > 0


def test_default_deploy() -> None:
	endpoint = default_deploy_example.default_deploy()
	assert endpoint
