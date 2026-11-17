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

# [START spanner_remote_function_handler]
import flask
import functions_framework

# Spanner encodes INT64 values outside +/- 2^53 as JSON strings to preserve precision.
_MAX_LOSSLESS_JSON_INT = 9007199254740992


@functions_framework.http
def batch_add(request: flask.Request) -> tuple[dict[str, object], int]:
    """Sums integer arguments for batched Cloud Spanner Remote Function calls.

    Spanner invokes remote functions via HTTPS POST with a JSON body containing
    a `calls` list of argument arrays, and expects `{"replies": [...]}` in the
    same order or `{"errorMessage": ...}` with a non-200 status on permanent
    argument errors.

    Args:
        request: Incoming Flask HTTP request containing batched `calls`.

    Returns:
        A JSON-serializable response dictionary and HTTP status code.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or not isinstance(payload.get("calls"), list):
        return {"errorMessage": "Request JSON must include a 'calls' list."}, 400

    replies: list[int | str] = []
    try:
        for call in payload["calls"]:
            if not isinstance(call, list):
                return {"errorMessage": "Each entry in 'calls' must be a list."}, 400
            total = sum(int(item) for item in call if item is not None)
            if total > _MAX_LOSSLESS_JSON_INT or total < -_MAX_LOSSLESS_JSON_INT:
                replies.append(str(total))
            else:
                replies.append(total)
    except (TypeError, ValueError) as err:
        return {"errorMessage": f"Invalid integer argument: {err}"}, 400

    return {"replies": replies}, 200


# [END spanner_remote_function_handler]
