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

import ykman_utils
import kms.singletenanthsm.approve_proposal as approve_proposal
import gcloud_commands
import pytest
import subprocess

import sys
import argparse
from unittest.mock import patch, Mock
from unittest import mock


sample_sthi_output = """
{
  "quorumParameters": {
    "challenges": [
      {
        "challenge": "-jgoZSrRHP_1WQt6f4cx911AkWfa9WzqVuuOLd7iw6iAwdkeVcBA_Q3sBqaP_5B6",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuKbCvQEFWx65Ma57Ul24\n044s74u7H1nLQJ8WfBe33MKmOrsR31pO5dIfnJIs8d0vDFj3cm4MRRpIdI8PkOPE\noDDa9z0dz/t4qDpOKlRcxaFNZGoBs+j+TuC3rsrBxIxc+qSDn/WhDV2oAXaj3Jnw\n5DPCGljDObbzaDwTjovP3enfFCncCl76z0yGuKoyW4aqoK2ccHLRxNF69bYSzICE\nCiUxUeHJTvoLuJ8fwGUIKYsBb9tBuzGsrM+5Mj+bskvJLM3cNOkW1p1TOjLTtMk2\npDlY+9EdWMJ/6wbX88b7dl5T3aQOTzNrxjojpYPyNWdHIGXL1YwKNE3EkdN7kXkK\nyQIDAQAB\n-----END PUBLIC KEY-----\n"
      },
      {
        "challenge": "C-A4-b-ZKjpgY0EJZmDIbUsTaZs3iPq-iW9XWQ18zd_k-biw8iKiWX7eLBjwUoHk",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyrAMwX6JXw9RIH8f2+lG\nVpaqAT2nwyzbPtpoRgemX/6ig3R8W9yNWOMvK6tf0MAVeHiyQIPucNXehr1VzQ1/\nVIlA9KA7LXznXwXDZkLl1/XHeJGbd3eyEA8K7tT3bFrSTZx/mVhEuJN9eLb5tL9t\ngqes7pgYYe2iyhUCqQM3oh4K5SJGooQDX41/VXP8PxCem+71oG/LWogIVMLnU9Yu\n33oQY6xvF1YKNgfGqnyNh5rPduQplJy04o/b6Xs3mcX/NUOBMUcLXDxe6tRGyy/2\nUX+6thK9gU2dXheK03rwhMv5jmpIGP7FShSs/+9N3nUIA+g5sTgnm2xqch5jOYXV\nlwIDAQAB\n-----END PUBLIC KEY-----\n"
      },
      {
        "challenge": "Q8nT85xO8wuYguKfPSVU60rmpO67ue-CvSFXxIVzjeh2AaYPQ3Vq7Jsu2Bk4ynAC",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoidJnb4gpd8Ua/QRpwjb\nCg+0pHhQ22bv0bX66fj8niLPV4o/TaQzyYD94zA7t6ulUmxj93w2U0EEmsufrBrt\nOgorVidL6MLuEOo0lWy0DHBsFDellFA75MTTIs76odhJshVfe9OSwFAakoMHiDAY\nLTmTEcaJsanUiHhIaxF5O/cTAFlkhOLFD0becK674OAnqqmabzJx2qlTMraR3yPi\nW1uLPdPBNeokBirk4WIO8XKtQJuOrGWhAxjIvGW20paRWgs0QI34ZgYQdnIjKwMO\n0dsr/vlHjfRs0OX2oVmBqSi+TNY240BC4HshQOSPBdR2HsC9vfQ0uax8+nEcZiNG\nCQIDAQAB\n-----END PUBLIC KEY-----\n"
      }
    ]
  }
}

"""

sample_approved_challenges_output = """
quorumParameters:
  approvedTwoFactorPublicKeyPems:
  - |
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoidJnb4gpd8Ua/QRpwjb
    Cg+0pHhQ22bv0bX66fj8niLPV4o/TaQzyYD94zA7t6ulUmxj93w2U0EEmsufrBrt
    OgorVidL6MLuEOo0lWy0DHBsFDellFA75MTTIs76odhJshVfe9OSwFAakoMHiDAY
    LTmTEcaJsanUiHhIaxF5O/cTAFlkhOLFD0becK674OAnqqmabzJx2qlTMraR3yPi
    W1uLPdPBNeokBirk4WIO8XKtQJuOrGWhAxjIvGW20paRWgs0QI34ZgYQdnIjKwMO
    0dsr/vlHjfRs0OX2oVmBqSi+TNY240BC4HshQOSPBdR2HsC9vfQ0uax8+nEcZiNG
    CQIDAQAB
    -----END PUBLIC KEY-----
  - |
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuKbCvQEFWx65Ma57Ul24
    044s74u7H1nLQJ8WfBe33MKmOrsR31pO5dIfnJIs8d0vDFj3cm4MRRpIdI8PkOPE
    oDDa9z0dz/t4qDpOKlRcxaFNZGoBs+j+TuC3rsrBxIxc+qSDn/WhDV2oAXaj3Jnw
    5DPCGljDObbzaDwTjovP3enfFCncCl76z0yGuKoyW4aqoK2ccHLRxNF69bYSzICE
    CiUxUeHJTvoLuJ8fwGUIKYsBb9tBuzGsrM+5Mj+bskvJLM3cNOkW1p1TOjLTtMk2
    pDlY+9EdWMJ/6wbX88b7dl5T3aQOTzNrxjojpYPyNWdHIGXL1YwKNE3EkdN7kXkK
    yQIDAQAB
    -----END PUBLIC KEY-----
  - |
    -----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyrAMwX6JXw9RIH8f2+lG
    VpaqAT2nwyzbPtpoRgemX/6ig3R8W9yNWOMvK6tf0MAVeHiyQIPucNXehr1VzQ1/
    VIlA9KA7LXznXwXDZkLl1/XHeJGbd3eyEA8K7tT3bFrSTZx/mVhEuJN9eLb5tL9t
    gqes7pgYYe2iyhUCqQM3oh4K5SJGooQDX41/VXP8PxCem+71oG/LWogIVMLnU9Yu
    33oQY6xvF1YKNgfGqnyNh5rPduQplJy04o/b6Xs3mcX/NUOBMUcLXDxe6tRGyy/2
    UX+6thK9gU2dXheK03rwhMv5jmpIGP7FShSs/+9N3nUIA+g5sTgnm2xqch5jOYXV
    lwIDAQAB
    -----END PUBLIC KEY-----
"""

# def create_parser():
#     parser = argparse.ArgumentParser(...)
#     parser.add_argument...
#     return parser

@pytest.fixture()
def setup():
    parser = approve_proposal.parse_args(["proposal_resource", "my_proposal"])

def approve_mock_proposal():
    approve_proposal.approve_proposal()

test_resource = "projects/my-project/locations/us-east1/singleTenantHsmInstances/mysthi/proposals/my_proposal"

mock_completed_process = subprocess.CompletedProcess

def test_get_challenges_mocked(mocker):
    mock_response = mocker.MagicMock()
    mock_response.stdout = sample_sthi_output

    # mock the challenge string returned by service
    mocker.patch("subprocess.run", return_value=mock_response)
    result = gcloud_commands.fetch_challenges(test_resource)
    assert result.stdout == sample_sthi_output
    assert type(result.stdout) is str

    # mock the creation of the challenges directory


    # sign challenges


    # mock sneding the signed challenges to gcloud

# @patch("subprocess.run")
# def test_fetch_challenges_and_sign():
#     with patch.object(sys, "argv", ["approve_sthi_proposal.py",  test_resource]):
#         approve_sthi_proposal.approve_proposal()

#         mock_result = Mock()
#         mock_result.returncode = 0
#         mock_result.stdout = sample_sthi_output
#         mock_run.return_value = mock_result

#         self.assertEqual()

    # approve_sthi_proposal.approve_proposal()

if __name__ == "__main__":
    approve_proposal.parse_only_challenges(sample_sthi_output)
    challenges = ykman_utils.populate_challenges_from_files()
    for challenge in challenges:
        print(challenge.challenge)
        print(challenge.public_key_pem)
    signed_challenged_files = []
    signed_challenges = ykman_utils.sign_proposal(challenges, signed_challenged_files)
    for signed_files in signed_challenged_files:
        print(signed_files)
    # banana = 1 + 1
    

