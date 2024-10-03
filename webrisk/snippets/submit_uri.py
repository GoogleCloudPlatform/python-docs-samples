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
from google.api_core.operation import Operation
from google.cloud import webrisk_v1


def submit_uri(project_id: str, uri: str) -> Operation:
    """Submits a URI suspected of containing malicious content to be reviewed.

    Returns a google.longrunning.Operation which, once the review is complete, is updated with its result.
    You can use the [Pub/Sub API] (https://cloud.google.com/pubsub) to receive notifications for the
    returned Operation.
    If the result verifies the existence of malicious content, the site will be added to the
    Google's Social Engineering lists in order to protect users that could get exposed to this
    threat in the future. Only allow-listed projects can use this method during Early Access.

     Args:
         project_id: The name of the project that is making the submission.
         uri: The URI that is being reported for malicious content to be analyzed.
             uri = "http://testsafebrowsing.appspot.com/s/malware.html"

    Returns:
        A Long Running Operation ID similar to `projects/1234/operations/5678`.
    """
    webrisk_client = webrisk_v1.WebRiskServiceClient()

    # Set the URI to be submitted.
    submission = webrisk_v1.Submission()
    submission.uri = uri

    # Confidence that a URI is unsafe.
    threat_confidence = webrisk_v1.ThreatInfo.Confidence(
        level=webrisk_v1.ThreatInfo.Confidence.ConfidenceLevel.MEDIUM
    )

    # Context about why the URI is unsafe.
    threat_justification = webrisk_v1.ThreatInfo.ThreatJustification(
        # Labels that explain how the URI was classified.
        labels=[
            webrisk_v1.ThreatInfo.ThreatJustification.JustificationLabel.AUTOMATED_REPORT
        ],
        # Free-form context on why this URI is unsafe.
        comments=["Testing submission"],
    )

    # Set the context about the submission including the type of abuse found on the URI and
    # supporting details.
    threat_info = webrisk_v1.ThreatInfo(
        # The abuse type found on the URI.
        abuse_type=webrisk_v1.types.ThreatType.SOCIAL_ENGINEERING,
        threat_confidence=threat_confidence,
        threat_justification=threat_justification,
    )

    # Set the details about how the threat was discovered.
    threat_discovery = webrisk_v1.ThreatDiscovery(
        # Platform on which the threat was discovered.
        platform=webrisk_v1.ThreatDiscovery.Platform.MACOS,
        # CLDR region code of the countries/regions the URI poses a threat ordered
        # from most impact to least impact. Example: "US" for United States.
        region_codes=["US"],
    )

    request = webrisk_v1.SubmitUriRequest(
        parent=f"projects/{project_id}",
        submission=submission,
        threat_info=threat_info,
        threat_discovery=threat_discovery,
    )

    response = webrisk_client.submit_uri(request)
    return response.operation


# [END webrisk_submit_uri]
