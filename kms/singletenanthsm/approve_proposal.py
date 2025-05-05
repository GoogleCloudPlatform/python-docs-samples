#!/usr/bin/env python

# Copyright 2025 Google LLC
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
import json
import logging
import os
import sys
from typing import List

import gcloud_commands
import ykman_utils


def make_directory(directory_path: str) -> None:
    """Creates a directory with the passed in path if it does not already exist.

    Args:
        directory_path: The path of the directory to be created.

    Returns:
        None
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Parsing challenges into files")
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        logger.info(f"Directory '{directory_path}' created.")
    else:
        logger.info(f"Directory '{directory_path}' already exists.")


def parse_challenges_into_files(sthi_output: str) -> List[bytes]:
    """Parses the STHI output and writes the challenges and public keys to files.

    Args:
        sthi_output: The output of the STHI command.

    Returns:
        A list of the unsigned challenges.
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info("Parsing challenges into files")
    proposal_json = json.loads(sthi_output, strict=False)
    challenges = proposal_json["quorumParameters"]["challenges"]

    make_directory("challenges")

    challenge_count = 0
    unsigned_challenges = []
    for challenge in challenges:
        challenge_count += 1
        try:
            with open("challenges/challenge{0}.txt".format(challenge_count), "wb") as f:
                binary_challenge = ykman_utils.urlsafe_base64_to_binary(
                    challenge["challenge"]
                )
                f.write(binary_challenge)
        except FileNotFoundError:
            logger.exception(
                f"File not found: challenges/challenge{challenge_count}.txt"
            )
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
        try:
            with open("challenges/public_key{0}.pem".format(challenge_count), "w") as f:
                f.write(
                    challenge["publicKeyPem"].encode("utf-8").decode("unicode_escape")
                )
        except FileNotFoundError:
            logger.exception(
                f"File not found: challenges/public_key{challenge_count}.txt"
            )
        except Exception as e:
            logger.exception(f"An error occurred: {e}")
        unsigned_challenges.append(
            ykman_utils.Challenge(binary_challenge, challenge["publicKeyPem"])
        )

    return unsigned_challenges


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal_resource", type=str, required=True)
    parser.add_argument(
        "--management_key",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--pin",
        type=str,
        required=False,
    )
    return parser.parse_args(args)


def signed_challenges_to_files(
    challenge_replies: list[ykman_utils.ChallengeReply],
) -> None:
    """Writes the signed challenges and public keys to files.

    Args:
        challenge_replies: A list of ChallengeReply objects.

    Returns:
        None
    """
    signed_challenge_files = []
    challenge_count = 0

    for challenge_reply in challenge_replies:
        challenge_count += 1
        make_directory("signed_challenges")
        with open(
            f"signed_challenges/public_key_{challenge_count}.pem", "w"
        ) as public_key_file:

            # Write public key to file
            public_key_file.write(challenge_reply.public_key_pem)
        with open(
            f"signed_challenges/signed_challenge{challenge_count}.bin", "wb"
        ) as binary_file:

            # Write signed challenge to file
            binary_file.write(challenge_reply.signed_challenge)
            signed_challenge_files.append(
                (
                    f"signed_challenges/signed_challenge{challenge_count}.bin",
                    f"signed_challenges/public_key_{challenge_count}.pem",
                )
            )
    return signed_challenge_files


def approve_proposal():
    """Approves a proposal by fetching challenges, signing them, and sending them back to gcloud."""
    parser = parse_args(sys.argv[1:])

    # Fetch challenges
    process = gcloud_commands.fetch_challenges(parser.proposal_resource)

    # Parse challenges into files
    unsigned_challenges = parse_challenges_into_files(process.stdout)

    # Sign challenges
    signed_challenges = ykman_utils.sign_challenges(
        challenges=unsigned_challenges,
        management_key=parser.management_key,
        pin=parser.pin,
    )

    # Parse signed challenges into files
    signed_challenged_files = signed_challenges_to_files(signed_challenges)

    # Return signed challenges to gcloud
    gcloud_commands.send_signed_challenges(
        signed_challenged_files, parser.proposal_resource
    )


if __name__ == "__main__":
    approve_proposal()
