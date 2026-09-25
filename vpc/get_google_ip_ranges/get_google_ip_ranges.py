# Copyright 2026 Google LLC
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

# [START vpc_get_google_ip_ranges]
from __future__ import annotations

import json
from urllib.error import URLError
from urllib.request import urlopen

import netaddr

# Google publishes two official IP range feeds:
# - goog: Complete list of all Google-owned IP ranges (Search, YouTube, APIs, etc.)
# - cloud: External IP ranges allocated for customer Google Cloud resources
IPRANGE_URLS: dict[str, str] = {
    "goog": "https://www.gstatic.com/ipranges/goog.json",
    "cloud": "https://www.gstatic.com/ipranges/cloud.json",
}


def get_data(url: str) -> netaddr.IPSet | None:
    """Fetches JSON IP range data from a URL and converts prefixes into an IPSet.

    Args:
        url: The public URL of the JSON IP ranges feed.

    Returns:
        A netaddr.IPSet containing all parsed IPv4 and IPv6 network prefixes,
        or None if the network request or JSON parsing fails.
    """
    # Step 1: Download and parse the JSON feed
    try:
        with urlopen(url, timeout=30) as response:
            data = json.load(response)
    except (URLError, json.JSONDecodeError, TimeoutError) as error:
        print(f"ERROR: Failed to fetch or parse {url}: {error}")
        return None

    # Verify root payload is a JSON object
    if not isinstance(data, dict):
        print(f"ERROR: Expected JSON object from {url}, got {type(data).__name__}")
        return None

    creation_time = data.get("creationTime", "Unknown")
    print(f"Fetched {url} (published: {creation_time})")

    # Step 2: Extract both IPv4 and IPv6 CIDR prefixes into an IPSet
    cidr_set = netaddr.IPSet()
    prefixes = data.get("prefixes", [])
    if isinstance(prefixes, list):
        for prefix_entry in prefixes:
            if not isinstance(prefix_entry, dict):
                continue
            try:
                if "ipv4Prefix" in prefix_entry:
                    cidr_set.add(prefix_entry["ipv4Prefix"])
                if "ipv6Prefix" in prefix_entry:
                    cidr_set.add(prefix_entry["ipv6Prefix"])
            except (netaddr.AddrFormatError, ValueError) as error:
                print(f"WARNING: Skipping invalid prefix in {url}: {error}")

    return cidr_set


def main() -> None:
    """Calculates and displays CIDR ranges for Google APIs and default domain services.

    By subtracting customer Google Cloud IP ranges ('cloud') from all Google IP
    ranges ('goog'), we isolate the IP ranges used exclusively for Google APIs
    and default services (such as *.googleapis.com).
    """
    # Step 1: Fetch and parse IP ranges for both 'goog' and 'cloud' feeds
    cidrs: dict[str, netaddr.IPSet] = {}
    for feed_name, url in IPRANGE_URLS.items():
        feed_cidrs = get_data(url)

        if feed_cidrs is None:
            raise ValueError(f"ERROR: Could not process data from {url}")

        cidrs[feed_name] = feed_cidrs

    # Step 2: Compute set difference (goog - cloud)
    # This removes customer cloud IPs, leaving only default Google APIs/services
    default_domain_cidrs = cidrs["goog"] - cidrs["cloud"]

    # Step 3: Print the aggregated CIDR list
    print("IP ranges for Google APIs and services default domains:")
    for cidr in default_domain_cidrs.iter_cidrs():
        print(cidr)


if __name__ == "__main__":
    main()
# [END vpc_get_google_ip_ranges]