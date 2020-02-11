#!/bin/bash

# Copyright 2019 Google LLC
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

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail
# Enables `**` to include files nested inside sub-folders
shopt -s globstar

# `--only-changed` will only run tests on projects container changes from the master branch.
if [[ $* == *--only-diff* ]]; then
    ONLY_DIFF="true"
else
    ONLY_DIFF="false"
fi

cd github/python-docs-samples

# install nox for testing
pip install -q nox

# Unencrypt and extract secrets
SECRETS_PASSWORD=$(cat "${KOKORO_GFILE_DIR}/secrets-password.txt")
./scripts/decrypt-secrets.sh "${SECRETS_PASSWORD}"

source ./testing/test-env.sh
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json
export GOOGLE_CLIENT_SECRETS=$(pwd)/testing/client-secrets.json
source "${KOKORO_GFILE_DIR}/automl_secrets.txt"
cp "${KOKORO_GFILE_DIR}/functions-slack-config.json" "functions/slack/config.json"

# For Datalabeling samples to hit the testing endpoint
export DATALABELING_ENDPOINT="test-datalabeling.sandbox.googleapis.com:443"
# Required for "run/image-processing" && "functions/imagemagick"
apt-get -qq update  && apt-get -qq install libmagickwand-dev > /dev/null

# Run Cloud SQL proxy (background process exit when script does)
wget --quiet https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy && chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances="${MYSQL_INSTANCE}"=tcp:3306 &>> cloud_sql_proxy.log &
./cloud_sql_proxy -instances="${POSTGRES_INSTANCE}"=tcp:5432 &>> cloud_sql_proxy.log &
echo -e "\nCloud SQL proxy started."

echo -e "\n******************** TESTING PROJECTS ********************"
# Switch to 'fail at end' to allow all tests to complete before exiting.
set +e
# Use RTN to return a non-zero value if the test fails.
RTN=0
ROOT=$(pwd)
# Find all requirements.txt in the repository (may break on whitespace).
for file in **/requirements.txt; do
    cd "$ROOT"
    # Navigate to the project folder.
    file=$(dirname "$file")
    cd "$file"

    # If $DIFF_ONLY is true, skip projects without changes.
    if [[ "$ONLY_DIFF" = "true" ]]; then
        git diff --quiet origin/master.. .
        CHANGED=$?
        if [[ "$CHANGED" -eq 0 ]]; then
          # echo -e "\n Skipping $file: no changes in folder.\n"
          continue
        fi
    fi

    # Skip unsupported Python versions for Cloud Functions
    # (Some GCF samples' dependencies don't support them)
    if [[ "$file" == "functions/"* ]]; then
      PYTHON_VERSION="$(python --version 2>&1)"
      if [[ "$PYTHON_VERSION" == "Python 2."* || "$PYTHON_VERSION" == "Python 3.5"* ]]; then
        # echo -e "\n Skipping $file: Python $PYTHON_VERSION is not supported by Cloud Functions.\n"
        continue
      fi
    fi

    echo "------------------------------------------------------------"
    echo "- testing $file"
    echo "------------------------------------------------------------"

    # If no local noxfile exists, copy the one from root
    if [[ ! -f "noxfile.py" ]]; then
      cp "$ROOT/noxfile-template.py" "./noxfile.py"
      echo -e "\n Using noxfile from project root. \n"
    fi

    # Use nox to execute the tests for the project.
    nox -s "$RUN_TESTS_SESSION"
    EXIT=$?

    # If this is a continuous build, send the test log to the Build Cop Bot.
    # See https://github.com/googleapis/repo-automation-bots/tree/master/packages/buildcop.
    if [[ $KOKORO_BUILD_ARTIFACTS_SUBDIR = *"continuous"* ]]; then
      XML=$(base64 -w 0 sponge_log.xml)

      # See https://github.com/apps/build-cop-bot/installations/5943459.
      MESSAGE=$(cat <<EOF
      {
          "Name": "buildcop",
          "Type" : "function",
          "Location": "us-central1",
          "installation": {"id": "5943459"},
          "repo": "GoogleCloudPlatform/python-docs-samples",
          "buildID": "$KOKORO_GIT_COMMIT",
          "buildURL": "https://source.cloud.google.com/results/invocations/$KOKORO_BUILD_ID",
          "xunitXML": "$XML"
      }
EOF
      )

      # Use a service account with access to the repo-automation-bots project.
      gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
      gcloud pubsub topics publish passthrough --project=repo-automation-bots --message="$MESSAGE"
    fi

    if [[ $EXIT -ne 0 ]]; then
      RTN=1
      echo -e "\n Testing failed: Nox returned a non-zero exit code. \n"
    else
      echo -e "\n Testing completed.\n"
    fi

done
cd "$ROOT"

# Workaround for Kokoro permissions issue: delete secrets
rm testing/{test-env.sh,client-secrets.json,service-account.json}

exit "$RTN"