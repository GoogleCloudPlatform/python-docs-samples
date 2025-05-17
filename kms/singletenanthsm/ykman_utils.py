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

import base64
from dataclasses import dataclass
import os
import pathlib
import re

import cryptography.exceptions
from cryptography.hazmat.primitives import _serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from ykman import piv
from ykman.device import list_all_devices
from yubikit.piv import hashes, PIN_POLICY, TOUCH_POLICY
from yubikit.piv import SmartCardConnection

DEFAULT_MANAGEMENT_KEY = "010203040506070801020304050607080102030405060708"
DEFAULT_PIN = "123456"


def generate_private_key(
    key_type=piv.KEY_TYPE.RSA2048,
    management_key=DEFAULT_MANAGEMENT_KEY,
    pin=DEFAULT_PIN,
):
    """Generates a private key on the yubikey."""

    devices = list_all_devices()
    if not devices:
        raise ValueError("no yubikeys found")
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
                raise RuntimeError("failed to generate public key")
            directory_path = "generated_public_keys"
            if not os.path.exists(directory_path):
                os.mkdir(directory_path)
                print(f"Directory '{directory_path}' created.")

            with open(
                f"generated_public_keys/public_key_{device_info.serial}.pem", "wb"
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


@dataclass
class Challenge:
    """Represents a challenge with its associated public key."""

    challenge: bytes
    public_key_pem: str

    def to_dict(self):
        return {
            "challenge": base64.b64encode(self.challenge).decode("utf-8"),
            "public_key_pem": self.public_key_pem,
        }

    @staticmethod
    def from_dict(data):
        if not isinstance(data, dict):
            return None
        return Challenge(
            challenge=base64.b64decode(data["challenge"]),
            public_key_pem=data["public_key_pem"],
        )


class ChallengeReply:

    def __init__(self, unsigned_challenge, signed_challenge, public_key_pem):
        self.unsigned_challenge = unsigned_challenge
        self.signed_challenge = signed_challenge
        self.public_key_pem = public_key_pem


def populate_challenges_from_files() -> list[Challenge]:
    """Populates challenges and their corresponding public keys from files.

    This function searches for files matching the patterns
    "challenges/public_key*.pem"
    and "challenges/challenge*.bin" in the current working directory. It then
    pairs each challenge with its corresponding public key based on matching
    numeric IDs in the filenames.

    Returns:
        list[Challenge]: A list of Challenge objects, each containing a challenge
        and its associated public key.
    """
    public_key_files = list(pathlib.Path.cwd().glob("challenges/public_key*.pem"))
    print(public_key_files)
    challenge_files = list(pathlib.Path.cwd().glob("challenges/challenge*.bin"))
    print(challenge_files)

    challenges = []

    for public_key_file in public_key_files:
        challenge_id = re.findall(r"\d+", str(public_key_file))
        for challenge_file in challenge_files:
            if challenge_id == re.findall(r"\d+", str(challenge_file)):
                print(public_key_file)
                file = open(public_key_file, "r")
                public_key_pem = file.read()
                file.close()
                file = open(challenge_file, "rb")
                challenge = file.read()
                file.close()
                challenges.append(Challenge(challenge, public_key_pem))
    return challenges


def sign_challenges(
    challenges: list[Challenge], management_key=DEFAULT_MANAGEMENT_KEY, pin=DEFAULT_PIN
) -> list[ChallengeReply]:
    """Signs a proposal's challenges using a Yubikey."""
    if not challenges:
        raise ValueError("Challenge list empty: No challenges to sign.")
    signed_challenges = []
    devices = list_all_devices()
    if not devices:
        raise ValueError("no yubikeys found")
    for yubikey, _ in devices:
        with yubikey.open_connection(SmartCardConnection) as connection:
            # Make PivSession and fetch public key from Signature slot.
            piv_session = piv.PivSession(connection)
            # authenticate
            piv_session.authenticate(
                piv.MANAGEMENT_KEY_TYPE.TDES,
                bytes.fromhex(management_key),
            )
            piv_session.verify_pin(pin)

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
                print(key_public_bytes.decode())
                print(challenge.public_key_pem)
                if key_public_bytes == challenge.public_key_pem.encode():

                    # sign the challenge
                    print("Press Yubikey to sign challenge")
                    signed_challenge = piv_session.sign(
                        slot=piv.SLOT.RETIRED1,
                        key_type=slot_metadata.key_type,
                        message=challenge.challenge,
                        hash_algorithm=hashes.SHA256(),
                        padding=padding.PKCS1v15(),
                    )

                    signed_challenges.append(
                        ChallengeReply(
                            challenge.challenge,
                            signed_challenge,
                            challenge.public_key_pem,
                        )
                    )
                    print("Challenge signed successfully")
    if not signed_challenges:
        raise RuntimeError(
            "No matching public keys between Yubikey and challenges. Make sure"
            " key is generated in correct slot"
        )
    return signed_challenges


def urlsafe_base64_to_binary(urlsafe_string: str) -> bytes:
    """Converts a URL-safe base64 encoded string to its binary equivalent.

    Args:
        urlsafe_string: The URL-safe base64 encoded string.

    Returns:
        The binary data as bytes, or None if an error occurs.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the input string is not valid URL-safe base64.
    """
    try:
        if not isinstance(urlsafe_string, str):
            raise TypeError("Input must be a string")
        # Check if the input string contains only URL-safe base64 characters
        if not re.match(r"^[a-zA-Z0-9_-]*$", urlsafe_string):
            raise ValueError("Input string contains invalid characters")
        # Add padding if necessary. Base64 requires padding to be a multiple of 4
        missing_padding = len(urlsafe_string) % 4
        if missing_padding:
            urlsafe_string += "=" * (4 - missing_padding)
        return base64.urlsafe_b64decode(urlsafe_string)
    except base64.binascii.Error as e:
        raise ValueError(f"Invalid URL-safe base64 string: {e}") from e


def verify_challenge_signatures(challenge_replies: list[ChallengeReply]):
    """Verifies the signatures of a list of challenge replies.

    Args:
        challenge_replies: A list of ChallengeReply objects.

    Raises:
        ValueError: If the list of challenge replies is empty.
        cryptography.exceptions.InvalidSignature: If a signature is invalid.
    """
    if not challenge_replies:
        raise ValueError("No signed challenges to verify")
    for challenge_reply in challenge_replies:
        public_key = load_pem_public_key(challenge_reply.public_key_pem.encode())
        try:
            public_key.verify(
                challenge_reply.signed_challenge,
                challenge_reply.unsigned_challenge,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            print("Signature verification success")
        except cryptography.exceptions.InvalidSignature as e:
            raise cryptography.exceptions.InvalidSignature(
                f"Signature verification failed: {e}"
            )
