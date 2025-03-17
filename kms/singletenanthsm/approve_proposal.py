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

import argparse
import sys
import gcloud_commands
import json
import os
import ykman_utils


def parse_only_challenges(sthi_output):
    proposal_json = json.loads(sthi_output, strict= False)
    challenges = proposal_json["quorumParameters"]["challenges"]

    directory_path = "challenges"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")

    challenge_count = 0
    for challenge in challenges:
        challenge_count += 1
        print(challenge["challenge"]+ "\n")
        print(challenge["publicKeyPem"].encode('utf-8').decode('unicode_escape'))
        f = open("challenges/challenge{0}.txt".format(challenge_count), "w")
        f.write(challenge["challenge"])
        f.close
        
        f = open("challenges/public_key{0}.pem".format(challenge_count), "w")
        f.write(challenge["publicKeyPem"].encode('utf-8').decode('unicode_escape'))
        f.close()
    




def parse_challenges(fetch_string):
    text_list = fetch_string.split("requiredApproverCount")
    challenge_list = text_list[0].split("challenge:")
    
    directory_path = "challenges"
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        print(f"Directory '{directory_path}' created.")
    else:
        print(f"Directory '{directory_path}' already exists.")
    
    
    print("PRINTING CHALLENGES")
    challenge_count = 0
    for challenge in challenge_list[1:]:

        challenge_count += 1
        elem_list = challenge.split(" ", 12)
        print("challenge: " + elem_list[1])
        print("public key: " + elem_list[-1])
        
        f = open("challenges/challenge{0}.txt".format(challenge_count), "w")
        f.write(elem_list[1])
        f.close
        
        f = open("challenges/public_key{0}.pem".format(challenge_count), "w")
        f.write(elem_list[-1])
        f.close()


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal_resource", type=str, required=True)
    return parser.parse_args(args)


def approve_proposal():
    parser = parse_args(sys.argv[1:])

    # Fetch challenges
    process = gcloud_commands.fetch_challenges(parser.proposal_resource)

    # Parse challenges into files
    parse_only_challenges(process.stdout)

    # Sign challenges
    challenges = ykman_utils.populate_challenges_from_files()
    signed_challenged_files = []
    signed_challenges = ykman_utils.sign_proposal(challenges, signed_challenged_files)

    # Return signed challenges to gcloud
    process = gcloud_commands.send_signed_challenges(
        signed_challenges,
        args.proposal_resource
        )


if __name__ == "__main__":
    approve_proposal()

