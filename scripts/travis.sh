#!/bin/bash
# Copyright 2021 Google LLC
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


# Decrypt secrets and run tests if not on an external PR.
if [[ $TRAVIS_SECURE_ENV_VARS == "true" ]]; then
    scripts/decrypt-secrets.sh "$SECRETS_PASSWORD"
    source ${TRAVIS_BUILD_DIR}/testing/test-env.sh;
    export GOOGLE_APPLICATION_CREDENTIALS=${TRAVIS_BUILD_DIR}/testing/service-account.json
    export GOOGLE_CLIENT_SECRETS=${TRAVIS_BUILD_DIR}/testing/client-secrets.json
    nox --envdir /tmp --stop-on-first-error -s lint gae py36 -- -m "not slow";
else
    # only run lint on external PRs
    echo 'External PR: only running lint.'
    nox --envdir /tmp --stop-on-first-error -s lint;
fi
