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

DIFF_FROM=""

# `--only-diff-master will only run tests on project changes from the master branch.
if [[ $* == *--only-diff-master* ]]; then
    DIFF_FROM="origin/master.."
fi

# `--only-diff-master will only run tests on project changes from the previous commit.
if [[ $* == *--only-diff-head* ]]; then
    DIFF_FROM="HEAD~.."
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

    # If $DIFF_FROM is set, use it to check for changes in this directory.
    if [[ "$DIFF_FROM" != "" ]]; then
        git diff --quiet "$DIFF_FROM" .
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
      PARENT_DIR=$(cd ../ && pwd)
      while [[ "$PARENT_DIR" != "$ROOT" && ! -f "$PARENT_DIR/noxfile-template.py" ]];
      do
        PARENT_DIR=$(dirname "$PARENT_DIR")
      done
      cp "$PARENT_DIR/noxfile-template.py" "./noxfile.py"
      echo -e "\n Using noxfile-template from parent folder ($PARENT_DIR). \n"
    fi

    # Use nox to execute the tests for the project.
    nox -s "$RUN_TESTS_SESSION"
    EXIT=$?

    # If this is a periodic build, send the test log to the Build Cop Bot.
    # See https://github.com/googleapis/repo-automation-bots/tree/master/packages/buildcop.
    if [[ $KOKORO_BUILD_ARTIFACTS_SUBDIR = *"periodic"* ]]; then
      chmod +x $KOKORO_GFILE_DIR/linux_amd64/buildcop
      $KOKORO_GFILE_DIR/linux_amd64/buildcop
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