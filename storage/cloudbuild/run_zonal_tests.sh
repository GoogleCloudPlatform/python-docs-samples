#!/bin/bash

# Copyright 2026 Google LLC
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
#


set -euxo pipefail
echo '--- Installing git and cloning repository on VM ---'
sudo apt-get update && sudo apt-get install -y git python3-pip python3-venv

# Clone the repository and checkout the specific commit from the build trigger.
git clone --no-checkout --depth 1 --sparse --filter=blob:none https://github.com/GoogleCloudPlatform/python-docs-samples
cd python-docs-samples
git sparse-checkout set storage
git fetch origin "refs/pull/${_PR_NUMBER}/head"
git checkout ${COMMIT_SHA}
cd storage


echo '--- Installing Python and dependencies on VM ---'
python3 -m venv env
source env/bin/activate

echo 'Install testing libraries explicitly, as they are not in setup.py'
pip install --upgrade pip
pip install pytest pytest-timeout pytest-subtests pytest-asyncio
pip install google-cloud-testutils google-cloud-kms
pip install google-cloud-storage[grpc,testing]

echo '--- Setting up environment variables on VM ---'
export ZONAL_BUCKET=${_ZONAL_BUCKET}
export RUN_ZONAL_SYSTEM_TESTS=True
export GCE_METADATA_MTLS_MODE=None
CURRENT_ULIMIT=$(ulimit -n)
echo '--- Running Zonal tests on VM with ulimit set to ---' $CURRENT_ULIMIT
pytest -vv -s --log-format='%(asctime)s %(levelname)s %(message)s' --log-date-format='%H:%M:%S' samples/snippets/zonal_buckets/zonal_snippets_test.py
