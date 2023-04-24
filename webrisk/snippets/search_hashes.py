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

# [START webrisk_search_hash]
from google.cloud import webrisk_v1


def search_hashes(hash_prefix: bytes, threat_type: webrisk_v1.ThreatType) -> None:
    """Gets the full hashes that match the requested hash prefix.

    This is used after a hash prefix is looked up in a threatList and there is a match.
    The client side threatList only holds partial hashes so the client must query this method
    to determine if there is a full hash match of a threat.

    Args:
        hash_prefix: A hash prefix, consisting of the most significant 4-32 bytes of a SHA256 hash.
            For JSON requests, this field is base64-encoded. Note that if this parameter is provided
            by a URI, it must be encoded using the web safe base64 variant (RFC 4648).
            Example:
                uri = "http://example.com"
                sha256 = sha256()
                sha256.update(base64.urlsafe_b64encode(bytes(uri, "utf-8")))
                hex_string = sha256.digest()

        threat_type: The ThreatLists to search in. Multiple ThreatLists may be specified.
            For the list on threat types, see:
            https://cloud.google.com/web-risk/docs/reference/rpc/google.cloud.webrisk.v1#threattype
            threat_type = [webrisk_v1.ThreatType.MALWARE, webrisk_v1.ThreatType.SOCIAL_ENGINEERING]
    """
    webrisk_client = webrisk_v1.WebRiskServiceClient()

    # Set the hashPrefix and the threat types to search in.
    request = webrisk_v1.SearchHashesRequest()
    request.hash_prefix = hash_prefix
    request.threat_types = [threat_type]

    response = webrisk_client.search_hashes(request)

    # Get all the hashes that match the prefix. Cache the returned hashes until the time
    # specified in threat_hash.expire_time
    # For more information on response type, see:
    # https://cloud.google.com/web-risk/docs/reference/rpc/google.cloud.webrisk.v1#threathash
    for threat_hash in response.threats:
        print(threat_hash.hash)

    print("Completed searching threat hashes.")

# [END webrisk_search_hash]
