#!/usr/bin/env python
# Copyright 2021 Google, Inc
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
#
# All Rights Reserved.

# [START recaptcha_enterprise_annotate_assessment]
from google.cloud import recaptchaenterprise_v1


def annotate_assessment(project_id: str, assessment_id: str) -> None:
    """Pre-requisite: Create an assessment before annotating.
        Annotate an assessment to provide feedback on the correctness of recaptcha prediction.
    Args:
        project_id: Google Cloud Project ID
        assessment_id: Value of the 'name' field returned from the create_assessment() call.
    """

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    assessment_name = f"projects/{project_id}/assessments/{assessment_id}"
    # Build the annotation request.
    # For more info on when/how to annotate, see:
    # https://cloud.google.com/recaptcha-enterprise/docs/annotate-assessment#when_to_annotate
    request = recaptchaenterprise_v1.AnnotateAssessmentRequest()
    request.name = assessment_name
    request.annotation = request.Annotation.FRAUDULENT
    request.reasons = [request.Reason.FAILED_TWO_FACTOR]

    # Empty response is sent back.
    client.annotate_assessment(request)
    print("Annotated response sent successfully ! ")


# [END recaptcha_enterprise_annotate_assessment]
