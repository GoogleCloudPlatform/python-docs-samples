#!/bin/bash

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT=$( dirname "$DIR" )

# Work from the project root.
cd $ROOT

# Use SECRET_MANAGER_PROJECT if set, fallback to cloud-devrel-kokoro-resources.
PROJECT_ID="${SECRET_MANAGER_PROJECT:-cloud-devrel-kokoro-resources}"

gcloud secrets versions add "python-docs-samples-test-env" \
       --project="${PROJECT_ID}" \
       --data-file="testing/test-env.sh"

gcloud secrets versions add "python-docs-samples-service-account" \
       --project="${PROJECT_ID}" \
       --data-file="testing/service-account.json"

gcloud secrets versions add "python-docs-samples-client-secrets" \
       --project="${PROJECT_ID}" \
       --data-file="testing/client-secrets.json"
