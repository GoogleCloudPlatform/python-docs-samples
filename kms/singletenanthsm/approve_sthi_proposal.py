#!/usr/bin/env python

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gcloud_commands
import ykman_utils


def approve_proposal(sthi_proposal_resource):
    # Fetch challenges
    process = gcloud_commands.fetch_challenges(sthi_proposal_resource)
    challenges = process.stdout

    # Sign challenges
    signed_challenges = ykman_utils.sign_proposal(challenges)

    # Return signed challenges to gcloud
    process = gcloud_commands.send_signed_challenges(
        signed_challenges,
        sthi_proposal_resource
        )


if __name__ == "__main__":
    approve_proposal()

