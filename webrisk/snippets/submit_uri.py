#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# [START webrisk_submit_uri]
from google.cloud import webrisk_v1
from google.cloud.webrisk_v1 import Submission


def submit_uri(project_id: str, uri: str) -> Submission:
    """Submits a URI suspected of containing malicious content to be reviewed.

    Returns a google.longrunning.Operation which, once the review is complete, is updated with its result.
    If the result verifies the existence of malicious content, the site will be added to the
    Google's Social Engineering lists in order to protect users that could get exposed to this
    threat in the future. Only allow-listed projects can use this method during Early Access.

     Args:
         project_id: The name of the project that is making the submission.
         uri: The URI that is being reported for malicious content to be analyzed.
             uri = "http://testsafebrowsing.appspot.com/s/malware.html"

    Returns:
        Submission response that contains the URI submitted.
    """
    webrisk_client = webrisk_v1.WebRiskServiceClient()

    submission = webrisk_v1.Submission()
    submission.uri = uri

    request = webrisk_v1.CreateSubmissionRequest()
    request.parent = f"projects/{project_id}"
    request.submission = submission

    response = webrisk_client.create_submission(request)
    return response


# [END webrisk_submit_uri]
