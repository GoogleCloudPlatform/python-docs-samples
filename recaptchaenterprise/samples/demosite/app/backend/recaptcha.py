# Copyright 2023 Google LLC
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

import json

from flask import jsonify, Response

from backend.create_assessment import create_assessment

# Wrapper method for create assessment calls.
def execute_create_assessment(project_id, json_data: json) -> Response:
    threshold_score = 0.50

    try:
        score, reasons = create_assessment(project_id=project_id,
                                    recaptcha_site_key=json_data["recaptcha_cred"]["sitekey"],
                                    recaptcha_action=json_data["recaptcha_cred"]["action"], token=json_data["recaptcha_cred"]["token"])
        if score < threshold_score:
            verdict = "Not a human"
        else:
            verdict = "Human"
        return jsonify({'data': {"score": "{:.12f}".format(score), "verdict": verdict}, "success": "true"})

    except ValueError as e:
        return jsonify({'data': {"error_msg": str(e.__dict__)}, "success": "false"})
    except Exception as e:
        return jsonify({'data': {"error_msg": f"Something happened! Please try again ! {e.__dict__}"}, "success": "false"})

