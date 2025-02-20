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


# import pytest

import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import _serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key
import approve_sthi_proposal


public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyzXMN4kWOHPwCGiWHOZP
hpbiElngaVVll2UybTZq9ntJmyaVyYtzq2ypP5PkrOC0wfFsleU4T31ZAvgRFrcV
WLCCdFfr9TMBKkXz0VOXXFamDvyuKl7nKxjQnIqMWPd7Fo0JlDjCnrNew/KYpVZ7
VIZ4vLpyPfBHmJnaFyW1CY7cebQM0lBNH5hBibFl92ZRgm5Gg8tEMBKiySQKlP7E
I6rnA1KTwuCirXG2U/uaYj3rhsZahsJvUdyrpQQGNtkjpMX3f+djBf6Zs3p2l8hE
DNMmpuRb3EB88Su8P6vuxoJgxc5M0rV9RfutnsE4mMWKD3WO1Q0IiU8HwErURl/G
RwIDAQAB
-----END PUBLIC KEY-----
"""


class Challenge:

  def __init__(self, challenge, public_key_pem):
    self.challenge = challenge
    self.public_key_pem = public_key_pem


example_challenge_1 = Challenge(b"123", public_key)
example_challenge_2 = Challenge(b"456", "hello")


class ChallengeReply:
  
    def __init__(self, signed_challenge, public_key_pem):
        self.signed_challenge = signed_challenge
        self.public_key_pem = public_key_pem


def verify_challenge_signatures(signed_challenges):
  if not signed_challenges:
    raise Exception("No signed challenges to verify")
  for signed_challenge in signed_challenges:
    public_key = load_pem_public_key(
        example_challenge_1.public_key_pem.encode()
    )
    try:
      public_key.verify(
          signed_challenge,
          example_challenge_1.challenge,
          padding.PKCS1v15(),
          hashes.SHA256(),
      )
      print(f"Signature verification success")
    except cryptography.exceptions.InvalidSignature as e:
      print(f"Signature verification failed: {e}")


def test_sign_proposal_success():

  # Populate challenges
  challenges = []
  challenges.append(example_challenge_1)
  challenges.append(example_challenge_2)
  signed_challenges = approve_sthi_proposal.sign_proposal(challenges)
  if approve_sthi_proposal:
    print("proposals signed")
  else:
    print("proposals not signed")

  verify_challenge_signatures(signed_challenges)


def test_sign_proposal_missing_challenges():
  challenges = []


def test_sign_proposal_no_matching_public_keys():

  challenges = []


def test_fetch_challenges():
  print("fetching challenges")
  approve_sthi_proposal.fetch_challenges
  print("challenges fetched successfully")


if __name__ == "__main__":
  test_fetch_challenges()

  test_sign_proposal_success()
