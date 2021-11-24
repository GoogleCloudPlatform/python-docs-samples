#!/bin/bash
# Copyright 2020 Google LLC
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

# Run the test, assuming it's already in the target directory.
# Requirements:
# The current directory is the test target directory.
# Env var `PROJECT_ROOT` is defined.

echo "------------------------------------------------------------"
echo "- testing ${PWD}"
echo "------------------------------------------------------------"

# If no local noxfile exists, copy the one from root
if [[ ! -f "noxfile.py" ]]; then
    PARENT_DIR=$(cd ../ && pwd)
    while [[ "$PARENT_DIR" != "${PROJECT_ROOT}" && \
		 ! -f "$PARENT_DIR/noxfile-template.py" ]];
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

echo "PWD: ${PWD}"

# Inject region tag data into the test log
set +e  # Don't fail the entire test if this step fails
if [[ "${INJECT_REGION_TAGS:-}" == "true" ]]; then

    export XUNIT_PATH="$PWD/sponge_log.xml"
    export XUNIT_TMP_PATH="$(mktemp)"

    # We use `python3.8` because it is the version pip3 installs to.
    export PYTHON_CMD="python3"

    if [[ -f "$XUNIT_PATH" ]]; then
        echo "=== Injecting region tags into XUnit output ==="
        echo "Processing XUnit output file: $XUNIT_PATH (saving output to $XUNIT_TMP_PATH)"

        TARGET_DIR=$PWD

        # First, we generate a Python-specific "polyglot_snippet_data.json" file
        # (cd'ing into script's working dir is necessary for imports to work)
        echo "Calling $PYTHON_CMD ${PYTHON_PARSER_PATH} ${TARGET_DIR}"
        pushd $(dirname $PYTHON_PARSER_PATH)
        $PYTHON_CMD "$PYTHON_PARSER_PATH" "$TARGET_DIR"
        popd

        # Then, we pass the "polyglot_snippet_data.json" file and the XUnit output
        # to the "polyglot" parser.
        #   This outputs the XUnit input with the snippet-test map added
        #   Again, we use `python3` for pip3 support.
        echo "Calling: cat $XUNIT_PATH | $PYTHON_CMD ${POLYGLOT_PARSER_PATH} inject-snippet-mapping --output_file ${XUNIT_TMP_PATH} ${TARGET_DIR}"
        pushd $(dirname $POLYGLOT_PARSER_PATH)
        cat "$XUNIT_PATH" | \
        $PYTHON_CMD "$POLYGLOT_PARSER_PATH" --output_file "$XUNIT_TMP_PATH" inject-snippet-mapping "$TARGET_DIR"
        if [[ $? -eq 0 ]] && [[ -s "$XUNIT_PATH" ]]; then
            mv $XUNIT_TMP_PATH $XUNIT_PATH
        else
            echo "Region tag injection FAILED; XUnit file not modified."
        fi
        popd
    else
        echo "No XUnit output file found!"
    fi
    echo "=== Region tag injection complete! ==="
fi
set -e

# If REPORT_TO_BUILD_COP_BOT is set to "true", send the test log
# to the FlakyBot.
# See:
# https://github.com/googleapis/repo-automation-bots/tree/main/packages/flakybot.
if [[ "${REPORT_TO_BUILD_COP_BOT:-}" == "true" ]]; then
    chmod +x $KOKORO_GFILE_DIR/linux_amd64/flakybot
    $KOKORO_GFILE_DIR/linux_amd64/flakybot
fi

if [[ "${EXIT}" -ne 0 ]]; then
    echo -e "\n Testing failed: Nox returned a non-zero exit code. \n"
else
    echo -e "\n Testing completed.\n"
fi

# Remove noxfile.py if we copied.
if [[ $cleanup_noxfile -eq 1 ]]; then
    rm noxfile.py
fi

exit ${EXIT}
