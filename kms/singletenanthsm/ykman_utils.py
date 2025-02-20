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

import ykman
import cryptography.exceptions


from cryptography.hazmat.primitives import _serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.serialization import load_pem_public_key


from ykman import piv
from ykman.device import list_all_devices
from yubikit.piv import hashes
from yubikit.piv import PIN_POLICY, TOUCH_POLICY, hashes
from yubikit.piv import SmartCardConnection

DEFAULT_MANAGEMENT_KEY = "010203040506070801020304050607080102030405060708"
DEFAULT_PIN = "123456"


def generate_private_key(
    key_type=piv.KEY_TYPE.RSA2048,
    management_key=DEFAULT_MANAGEMENT_KEY,
    pin=DEFAULT_PIN,
):
  """Generates a private key on the yubikey"""

  devices = list_all_devices()
  if not devices:
    raise Exception("no yubikeys found")
  print(f"{len(devices)} yubikeys detected")
  for yubikey, device_info in devices:
    with yubikey.open_connection(SmartCardConnection) as connection:
      piv_session = piv.PivSession(connection)
      piv_session.authenticate(
          piv.MANAGEMENT_KEY_TYPE.TDES,
          bytes.fromhex(management_key),
      )
      piv_session.verify_pin(pin)

      public_key = piv_session.generate_key(
          piv.SLOT.RETIRED1,
          key_type=key_type,
          pin_policy=PIN_POLICY.DEFAULT,
          touch_policy=TOUCH_POLICY.ALWAYS,
      )
      if not public_key:
        raise Exception("failed to generate public key")
      with open(
          f"public_key_{device_info.serial}_slot_{piv.SLOT.RETIRED1}.pem", "wb"
      ) as binary_file:

        # Write bytes to file
        binary_file.write(
            public_key.public_bytes(
                encoding=_serialization.Encoding.PEM,
                format=_serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
      print(
          f"Private key pair generated on device {device_info.serial} on key"
          f" slot: {piv.SLOT.RETIRED1}"
      )

class ChallengeReply:
  
    def __init__(self, signed_challenge, public_key_pem):
        self.signed_challenge = signed_challenge
        self.public_key_pem = public_key_pem


def sign_proposal(challenges):
  """Signs a proposal's challenges using a Yubikey."""
  if not challenges:
    raise Exception("Challenge list empty: No challenges to sign.")
  signed_challenges = []
  devices = list_all_devices()
  if not devices:
    raise Exception("no yubikeys found")
  for yubikey, _ in devices:
    with yubikey.open_connection(SmartCardConnection) as connection:
      # Make PivSession and fetch public key from Signature slot.
      piv_session = piv.PivSession(connection)
      # authenticate
      piv_session.authenticate(
          piv.MANAGEMENT_KEY_TYPE.TDES,
          bytes.fromhex("010203040506070801020304050607080102030405060708"),
      )
      piv_session.verify_pin("123456")

      # Get the public key from slot 82.
      slot_metadata = piv_session.get_slot_metadata(slot=piv.SLOT.RETIRED1)
      print(slot_metadata.public_key.public_bytes)

      # Check to see if any of the challenge public keys matches with the
      # public key from slot 82.
      for challenge in challenges:
        key_public_bytes = slot_metadata.public_key.public_bytes(
            encoding=_serialization.Encoding.PEM,
            format=_serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        if key_public_bytes == challenge.public_key_pem.encode():

          # sign the challenge
          print("Press Yubikey to sign challenge")
          signed_challenges.append(
            ChallengeReply(
              piv_session.sign(
                  slot=piv.SLOT.RETIRED1,
                  key_type=slot_metadata.key_type,
                  message=challenge.challenge,
                  hash_algorithm=hashes.SHA256(),
                  padding=padding.PKCS1v15(),
              ),
              challenge.public_key_pem
            )
          )
          print("Challenge signed successfully")
  if not signed_challenges:
    raise Exception(
        "No matching public keys between Yubikey and challenges. Make sure"
        " key is generated in correct slot"
    )
  return signed_challenges


def verify_challenge_signatures(challenge_replies, data):
  if not challenge_replies:
    raise Exception("No signed challenges to verify")
  for challenge_reply in challenge_replies:
    public_key = load_pem_public_key(
        challenge_reply.public_key_pem.encode()
    )
    try:
      public_key.verify(
          challenge_reply.signed_challenge,
          data,
          padding.PKCS1v15(),
          hashes.SHA256(),
      )
      print(f"Signature verification success")
    except cryptography.exceptions.InvalidSignature as e:
      raise cryptography.exceptions.InvalidSignature((f"Signature verification failed: {e}"))
