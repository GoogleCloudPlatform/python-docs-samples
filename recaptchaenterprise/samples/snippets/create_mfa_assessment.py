# Copyright 2022 Google LLC
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

from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment


def create_mfa_assessment(
    project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str, hashed_account_id: str,
        email: str, phone_number: str
) -> str:
    """  MFA contains a series of workflow steps to be completed.
          1. Trigger the usual recaptcha challenge in the UI and get the token. In addition to the token,
          supply the hashedAccountId, email and/or phone number of the user.
          2. Based on the recommended action, choose if you should trigger the MFA challenge.
          3. If you decide to trigger MFA, send the requestToken back to the UI.
          4. In the UI, call "grecaptcha.enterprise.challengeAccount" and pass the sitekey, request token,
          and container id to render the challenge.
          5. The result from this promise is sent to another call "verificationHandle.verifyAccount(pin)"
          This call verifies if the pin has been entered correct.
          6. The result from this call is sent to the backend to create a MFA assessment again.
          The result of this assessment will tell if the MFA challenge has been successful.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
        hashed_account_id: one-way hash of the user id. HMAC SHA 256 + salt
        email: email id of the user (to trigger email based MFA)
        phone_number: contact number of the user (to trigger phone based MFA)
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token
    event.hashed_account_id = hashed_account_id

    endpoint_verification_info = recaptchaenterprise_v1.EndpointVerificationInfo()
    endpoint_verification_info.email_address = email
    endpoint_verification_info.phone_number = phone_number

    account_verification_info = recaptchaenterprise_v1.AccountVerificationInfo()
    account_verification_info.endpoints = endpoint_verification_info

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event
    assessment.account_verification = account_verification_info

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)
    if not verify_response_integrity(response, recaptcha_action):
        return ""

    result = response.account_verification.latest_verification_result
    if result == recaptchaenterprise_v1.types.AccountVerificationInfo.Result.RESULT_UNSPECIFIED:
        # send request token back
        return response.account_verification.endpoints[0].request_token

    print(f"MFA result: {result}")


def verify_response_integrity(response: Assessment, recaptcha_action: str) -> bool:
    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        return False

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return False