#!/usr/bin/env bash
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

set -euo pipefail

EVENT_NAME="${1:-local}"
BASE_REF="${2:-main}"

echo "Configuring target diff for event: $EVENT_NAME"

# Determine the target reference to diff against
if [ "$EVENT_NAME" = "pull_request" ]; then
    echo "Fetching origin/$BASE_REF metadata..."
    # Ensure we have the target branch metadata fetched.
    git fetch origin "$BASE_REF" --depth=1 --quiet
    
    # Isolate to only changes in the PR
    DIFF_COMMAND="origin/$BASE_REF..." 
else
    # Local fallback
    # diff against local main branch.
    echo "Running locally. Diffing against local $BASE_REF..."
    DIFF_COMMAND="$BASE_REF"
fi

# Gather modified/added Python files, explicitly ignoring deleted files via --diff-filter=d
DIFF_OUTPUT=$(git diff --name-only --diff-filter=d "$DIFF_COMMAND" -- '*.py' 2>/dev/null || true)

if [ -n "$DIFF_OUTPUT" ]; then
    mapfile -t CHANGED_FILES <<< "$DIFF_OUTPUT"
else
    CHANGED_FILES=()
fi

# Execute linters if changed Python files exist
if [ ${#CHANGED_FILES[@]} -gt 0 ]; then
    echo "Files to lint:"
    printf ' - %s\n' "${CHANGED_FILES[@]}"

    # Track execution success manually so both tools get a chance to run.
    # This prevents the workflow from dying on Black without showing Flake8 errors.
    BLACK_EXIT=0
    LINT_EXIT=0

    # adding -q to silence some of the extraneous logging
    echo "Running blacken..."
    nox -s blacken -- "${CHANGED_FILES[@]}" || BLACK_EXIT=$?
    
    echo "Running flake8 lint..."
    nox -s lint -- "${CHANGED_FILES[@]}" || LINT_EXIT=$?

    if [ $BLACK_EXIT -ne 0 ] || [ $LINT_EXIT -ne 0 ]; then
        echo "❌ One or more linting checks failed."
        exit 1
    fi
else
    echo "✅ No Python files changed in this scope. Skipping checks."
fi
