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
BEFORE_SHA="${3:-}"

echo "Configuring target diff for event: $EVENT_NAME"

# Determine the base branch/commit to diff against
if [ "$EVENT_NAME" = "pull_request" ]; then
    # Ensure we have the target branch metadata fetched.
    git fetch origin "$BASE_REF" --depth=1 --quiet
    BASE_SHA="origin/$BASE_REF"
else
    BASE_SHA="$BEFORE_SHA"
    # Fallback if it's a direct push without a prior SHA, or a local run
    if [ "$BASE_SHA" = "0000000000000000000000000000000000000000" ] || [ -z "$BASE_SHA" ]; then
        BASE_SHA="HEAD~1"
    fi
fi

DIFF_OUTPUT=$(git diff --name-only --diff-filter=d "$BASE_SHA" -- '*.py' 2>/dev/null || true)

if [ -n "$DIFF_OUTPUT" ]; then
    mapfile -t CHANGED_FILES <<< "$DIFF_OUTPUT"
else
    CHANGED_FILES=()
fi

# Execute linters if files exist
if [ ${#CHANGED_FILES[@]} -gt 0 ]; then
    echo "Files to lint:"
    printf ' - %s\n' "${CHANGED_FILES[@]}"

    # Track execution success manually so both tools get a chance to run
    BLACK_EXIT=0
    LINT_EXIT=0

    # Pass the array safely using "${CHANGED_FILES[@]}"
    nox -s blacken -- "${CHANGED_FILES[@]}" || BLACK_EXIT=$?
    nox -s lint -- "${CHANGED_FILES[@]}" || LINT_EXIT=$?

    if [ $BLACK_EXIT -ne 0 ] || [ $LINT_EXIT -ne 0 ]; then
        echo "❌ One or more linting checks failed."
        exit 1
    fi
else
    echo "✅ No Python files changed in this scope. Skipping checks."
fi
