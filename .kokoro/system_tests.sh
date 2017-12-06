#!/bin/bash

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eo pipefail

cd github/python-docs-samples

# Unencrypt and extract secrets
SECRETS_PASSWORD=$(cat "${KOKORO_GFILE_DIR}/secrets-password.txt")
./scripts/decrypt-secrets.sh "${SECRETS_PASSWORD}"

source ./testing/test-env.sh
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json
export GOOGLE_CLIENT_SECRETS=$(pwd)/testing/client-secrets.json

# Run tests
nox -k "${NOX_SESSION}" || ret_code=$?

# Workaround for Kokoro permissions issue: delete secrets
rm testing/{test-env.sh,client-secrets.json,service-account.json}

exit ${ret_code}
