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

import pathlib

import cryptography.exceptions

import pytest

import ykman_utils


class Challenge:

    def __init__(self, challenge, public_key_pem):
        self.challenge = challenge
        self.public_key_pem = public_key_pem


class ChallengeReply:

    def __init__(self, signed_challenge, public_key_pem):
        self.signed_challenge = signed_challenge
        self.public_key_pem = public_key_pem


challenge_test_data = b"test_data"


def generate_test_challenge_files():
    # Create challenges list from challenges directory
    challenges = ykman_utils.populate_challenges_from_files()
    for challenge in challenges:
        print(challenge.challenge)
        print(challenge.public_key_pem)
    # Sign challenges
    signed_challenges = ykman_utils.sign_challenges(challenges)
    # Use a sample challenge from the HSM
    ykman_utils.verify_challenge_signatures(
        signed_challenges,
        b"rddK-SCLvik55PPoxOxgjoZEnQ7kTttvtYg2-zYhpGsDjpsPEFw_2OKau1EFf3nN",
    )


# A yubikey connected to your local machine will be needed to run these tests.
# The generate_private_key() method will rewrite the key saved on slot 82(Retired1).
@pytest.fixture(autouse=True)
def key_setup():
    ykman_utils.generate_private_key()


def challenges():
    public_key_files = [
        key_file
        for key_file in pathlib.Path.cwd().glob("generated_public_keys/public_key*.pem")
    ]
    challenges = []

    for public_key_file in public_key_files:
        file = open(public_key_file, "r")
        public_key_pem = file.read()
        challenges.append(Challenge(challenge_test_data, public_key_pem))
    return challenges


def test_sign_and_verify_challenges():
    signed_challenges = ykman_utils.sign_challenges(challenges())
    ykman_utils.verify_challenge_signatures(signed_challenges)


def test_verify_mismatching_data_fail():
    with pytest.raises(cryptography.exceptions.InvalidSignature) as exec_info:
        signed_challenges = ykman_utils.sign_challenges(challenges())
        signed_challenges[0].signed_challenge = b"mismatched_data"
        ykman_utils.verify_challenge_signatures(signed_challenges)
    assert "Signature verification failed" in str(exec_info.value)


def test_sign_empty_challenge_list_fail():
    with pytest.raises(Exception) as exec_info:
        ykman_utils.sign_challenges([])
    assert "Challenge list empty" in str(exec_info.value)


def test_sign_no_matching_public_keys_fail():
    modified_challenges = challenges()
    for challenge in modified_challenges:
        challenge.public_key_pem = "modified_public_key"
    with pytest.raises(Exception) as exec_info:
        ykman_utils.sign_challenges(modified_challenges)
    assert "No matching public keys" in str(exec_info.value)


def test_verify_empty_challenge_replies_fail():
    with pytest.raises(Exception) as exec_info:
        ykman_utils.verify_challenge_signatures([])
    assert "No signed challenges to verify" in str(exec_info)
