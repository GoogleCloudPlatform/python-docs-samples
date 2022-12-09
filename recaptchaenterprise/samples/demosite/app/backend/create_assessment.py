from typing import List

from google.cloud import recaptchaenterprise_v1


def get_result(
        project_id: str, recaptcha_site_key: str, token: str, recaptcha_action: str
) -> [float, List[str]]:
    """ Create an assessment to analyze the risk of a UI action.
    Args:
        project_id: GCloud Project ID
        recaptcha_site_key: Site key obtained by registering a domain/app to use recaptcha services.
        token: The token obtained from the client on passing the recaptchaSiteKey.
        recaptcha_action: Action name corresponding to the token.
    """
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
        raise ValueError(f"The Create Assessment call failed because the token was invalid for the following reasons: {response.token_properties.invalid_reason}")

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        raise ValueError(f"The action attribute in your reCAPTCHA tag does not match the action you are expecting to score. Please check your action attribute !")
    else:
        # Get the risk score and the reason(s)
        # For more information on interpreting the assessment,
        # see: https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
    return response.risk_analysis.score, response.risk_analysis.reasons
