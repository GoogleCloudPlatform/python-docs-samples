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

# [START webrisk_compute_threatlist_diff]
from google.cloud import webrisk_v1
from google.cloud.webrisk_v1 import ComputeThreatListDiffResponse


def compute_threatlist_diff(
    threat_type: webrisk_v1.ThreatType,
    version_token: bytes,
    max_diff_entries: int,
    max_database_entries: int,
    compression_type: webrisk_v1.CompressionType,
) -> ComputeThreatListDiffResponse:
    """Gets the most recent threat list diffs.

    These diffs should be applied to a local database of hashes to keep it up-to-date.
    If the local database is empty or excessively out-of-date,
    a complete snapshot of the database will be returned. This Method only updates a
    single ThreatList at a time. To update multiple ThreatList databases, this method needs to be
    called once for each list.

    Args:
        threat_type: The threat list to update. Only a single ThreatType should be specified per request.
            threat_type = webrisk_v1.ThreatType.MALWARE

        version_token: The current version token of the client for the requested list. If the
            client does not have a version token (this is the first time calling ComputeThreatListDiff),
            this may be left empty and a full database snapshot will be returned.

        max_diff_entries: The maximum size in number of entries. The diff will not contain more entries
            than this value. This should be a power of 2 between 2**10 and 2**20.
            If zero, no diff size limit is set.
            max_diff_entries = 1024

        max_database_entries: Sets the maximum number of entries that the client is willing to have in the local database.
            This should be a power of 2 between 2**10 and 2**20. If zero, no database size limit is set.
            max_database_entries = 1024

        compression_type: The compression type supported by the client.
            compression_type = webrisk_v1.CompressionType.RAW

    Returns:
        The response which contains the diff between local and remote threat lists. In addition to the threat list,
        the response also contains the version token and the recommended time for next diff.
    """

    webrisk_client = webrisk_v1.WebRiskServiceClient()

    constraints = webrisk_v1.ComputeThreatListDiffRequest.Constraints()
    constraints.max_diff_entries = max_diff_entries
    constraints.max_database_entries = max_database_entries
    constraints.supported_compressions = [compression_type]

    request = webrisk_v1.ComputeThreatListDiffRequest()
    request.threat_type = threat_type
    request.version_token = version_token
    request.constraints = constraints

    response = webrisk_client.compute_threat_list_diff(request)

    # The returned response contains the following information:
    # https://cloud.google.com/web-risk/docs/reference/rpc/google.cloud.webrisk.v1#computethreatlistdiffresponse
    # Type of response: DIFF/ RESET/ RESPONSE_TYPE_UNSPECIFIED
    print(response.response_type)
    # New version token to be used the next time when querying.
    print(response.new_version_token)
    # Recommended next diff timestamp.
    print(response.recommended_next_diff)

    return response


# [END webrisk_compute_threatlist_diff]
