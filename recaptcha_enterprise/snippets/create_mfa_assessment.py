# Copyright 2023 Google LLC
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

# [START recaptcha_enterprise_mfa_assessment]

from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment


def create_mfa_assessment(
        project_id: str,
        recaptcha_site_key: str,
        token: str,
        recaptcha_action: str,
        hashed_account_id: str,
        email: str,
        phone_number: str,
) -> None:
    """Creates an assessment to obtain Multi-Factor Authentication result.

    If the result is unspecified, sends the request token to the caller to initiate MFA challenge.

    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
            To get the token, integrate the recaptchaSiteKey with frontend. See,
            https://cloud.google.com/recaptcha-enterprise/docs/instrument-web-pages#frontend_integration_score
        recaptcha_action: The action name corresponding to the token.
        hashed_account_id: Create hashedAccountId from user identifier.
            It's a one-way hash of the user identifier: HMAC SHA 256 + salt
        email: Email id of the user to trigger the MFA challenge.
        phone_number: Phone number of the user to trigger the MFA challenge. Phone number must be valid
            and formatted according to the E.164 recommendation.
            See: https://www.itu.int/rec/T-REC-E.164/en
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_site_key
    event.token = token
    event.hashed_account_id = hashed_account_id

    # Set the email address and the phone number to trigger/ verify the MFA challenge.
    endpoint_verification_info = recaptchaenterprise_v1.EndpointVerificationInfo()
    endpoint_verification_info.email_address = email
    endpoint_verification_info.phone_number = phone_number

    account_verification_info = recaptchaenterprise_v1.AccountVerificationInfo()
    account_verification_info.endpoints = [endpoint_verification_info]

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event
    assessment.account_verification = account_verification_info

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    # Check integrity of the response.
    response = client.create_assessment(request)
    if not verify_response_integrity(response, recaptcha_action):
        raise RuntimeError("Failed to verify token integrity.")

    result = response.account_verification.latest_verification_result
    # If the result is unspecified, send the request token to trigger MFA in the client.
    # You can choose to send both the email and phone number's request token.
    if result == recaptchaenterprise_v1.types.AccountVerificationInfo.Result.RESULT_UNSPECIFIED:
        print("Result unspecified. Trigger MFA challenge in the client by passing the request token.")
        # Send the request token for assessment. The token is valid for 15 minutes.
        # print(response.account_verification.endpoints[0].request_token)

    # If the result is not unspecified, return the result.
    print(f"MFA result: {result}")


def verify_response_integrity(response: Assessment, recaptcha_action: str) -> bool:
    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            f"The CreateAssessment call failed because the token was "
            f"invalid for the following reasons: "
            f"{response.token_properties.invalid_reason}")
        return False

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does "
            "not match the action you are expecting to score"
        )
        return False
    return True
# [END recaptcha_enterprise_mfa_assessment]
