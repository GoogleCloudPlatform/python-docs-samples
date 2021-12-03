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

# `--only-diff-main` will only run tests on project changes on the
# last common commit from the main branch.
if [[ $* == *--only-diff-main* ]]; then
    set +e
    git diff --quiet "origin/main..." .kokoro/tests .kokoro/docker \
	.kokoro/trampoline_v2.sh
    CHANGED=$?
    set -e
    if [[ "${CHANGED}" -eq 0 ]]; then
	DIFF_FROM="origin/main..."
    else
	echo "Changes to test driver files detected. Running full tests."
    fi
fi

# `--only-diff-head` will only run tests on project changes from the
# previous commit.
if [[ $* == *--only-diff-head* ]]; then
    set +e
    git diff --quiet "HEAD~.." .kokoro/tests .kokoro/docker \
	.kokoro/trampoline_v2.sh
    CHANGED=$?
    set -e
    if [[ "${CHANGED}" -eq 0 ]]; then
	DIFF_FROM="HEAD~.."
    else
	echo "Changes to test driver files detected. Running full tests."
    fi
fi

if [[ -z "${PROJECT_ROOT:-}" ]]; then
    PROJECT_ROOT="github/python-docs-samples"
fi

cd "${PROJECT_ROOT}"

# add user's pip binary path to PATH
export PATH="${HOME}/.local/bin:${PATH}"

# install nox for testing
pip install --user -q nox

# Use secrets acessor service account to get secrets.
if [[ -f "${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" ]]; then
    gcloud auth activate-service-account \
	   --key-file="${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" \
	   --project="cloud-devrel-kokoro-resources"
    # This script will create 3 files:
    # - testing/test-env.sh
    # - testing/service-account.json
    # - testing/client-secrets.json
    ./scripts/decrypt-secrets.sh
fi

if [[ -f ./testing/test-env.sh ]]; then
    source ./testing/test-env.sh
fi
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json

# For cloud-run session, we activate the service account for gcloud sdk.
if [[ -f "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
    gcloud auth activate-service-account \
	   --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"
fi

export GOOGLE_CLIENT_SECRETS=$(pwd)/testing/client-secrets.json

# For Datalabeling samples to hit the testing endpoint
export DATALABELING_ENDPOINT="test-datalabeling.sandbox.googleapis.com:443"

# Run Cloud SQL proxy (background process exit when script does)
wget --quiet https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 \
     -O ${HOME}/cloud_sql_proxy && chmod +x ${HOME}/cloud_sql_proxy
${HOME}/cloud_sql_proxy -instances="${MYSQL_INSTANCE}"=tcp:3306 &>> \
       ${HOME}/cloud_sql_proxy.log &
${HOME}/cloud_sql_proxy -instances="${POSTGRES_INSTANCE}"=tcp:5432 &>> \
       ${HOME}/cloud_sql_proxy-postgres.log &
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

    # First we look up the environment variable `RUN_TESTS_DIRS`. If
    # the value is set, we'll iterate through the colon separated
    # directory list. If the target directory is not under any
    # directory in the list, we skip this directory.
    # This environment variables are primarily for
    # `scripts/run_tests_local.sh`.
    #
    # The value must be a colon separated list of relative paths from
    # the project root.
    #
    # Example:
    #   cdn:appengine/flexible
    #     run tests for `cdn` and `appengine/flexible` directories.
    #   logging/cloud-client
    #     only run tests for `logging/cloud-client` directory.
    #
    if [[ -n "${RUN_TESTS_DIRS:-}" ]]; then
	match=0
	for d in $(echo "${RUN_TESTS_DIRS}" | tr ":" "\n"); do
	    # If the current dir starts with one of the
	    # RUN_TESTS_DIRS, we should run the tests.
	    if [[ "${file}" = "${d}"* ]]; then
		match=1
		break
	    fi
	done
	if [[ $match -eq 0 ]]; then
	    continue
	fi
    fi
    # If $DIFF_FROM is set, use it to check for changes in this directory.
    if [[ -n "${DIFF_FROM:-}" ]]; then
        git diff --quiet "$DIFF_FROM" .
        CHANGED=$?
        if [[ "$CHANGED" -eq 0 ]]; then
          # echo -e "\n Skipping $file: no changes in folder.\n"
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
        cleanup_noxfile=1
    else
        cleanup_noxfile=0
    fi

    # Use nox to execute the tests for the project.
    nox -s "$RUN_TESTS_SESSION"
    EXIT=$?

    # If REPORT_TO_BUILD_COP_BOT is set to "true", send the test log
    # to the FlakyBot.
    # See:
    # https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.
    if [[ "${REPORT_TO_BUILD_COP_BOT:-}" == "true" ]]; then
      chmod +x $KOKORO_GFILE_DIR/linux_amd64/flakybot
      $KOKORO_GFILE_DIR/linux_amd64/flakybot
    fi

    if [[ $EXIT -ne 0 ]]; then
      RTN=1
      echo -e "\n Testing failed: Nox returned a non-zero exit code. \n"
    else
      echo -e "\n Testing completed.\n"
    fi

    # Remove noxfile.py if we copied.
    if [[ $cleanup_noxfile -eq 1 ]]; then
        rm noxfile.py
    fi

done
cd "$ROOT"

# Remove secrets if we used decrypt-secrets.sh.
if [[ -f "${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" ]]; then
    rm testing/{test-env.sh,client-secrets.json,service-account.json}
fi

exit "$RTN"
