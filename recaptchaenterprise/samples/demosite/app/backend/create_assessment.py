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

from typing import List

from flask import jsonify
from google.cloud import recaptchaenterprise_v1


def create_assessment(
        project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str
) -> [float, List[str]]:
    """ Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """
    sample_threshold_score = 0.50
    # <!-- ATTENTION: reCAPTCHA Example (Server Part 2/2) Starts -->
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        raise ValueError(
            f"The Create Assessment call failed because the token was invalid for the following reasons: "
            f"{response.token_properties.invalid_reason}")

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        raise ValueError(
            "The action attribute in your reCAPTCHA tag does not match the action you are expecting to score. "
            "Please check your action attribute !")
    # <!-- ATTENTION: reCAPTCHA Example (Server Part 2/2) Ends -->

    # Return the risk score.
    verdict = "Not a human" if response.risk_analysis.score < sample_threshold_score else "Human"
    return jsonify(
        {'data': {"score": "{:.12f}".format(response.risk_analysis.score), "verdict": verdict}, "success": "true"})
