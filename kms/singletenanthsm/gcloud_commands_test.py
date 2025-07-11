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

import subprocess
from unittest import mock

import pytest

import gcloud_commands


test_proposal_resource = """projects/test_project/locations/\
us-central1/singleTenantHsmInstances/my_sthi/proposals/my_proposal
  """
sample_fetch_challenge_output = """
{
 "quorumParameters": {
    "challenges": [
      {
        "challenge": "tiOz64M_rJ34yOvweHBBltRrm3k34bou4m2JKlz9BmhrR7yU6S6ram8o1VQhyPU1",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3WK/NpZ4DJ68lOR7JINL\nyODwrRanATJNepJi1LYDDO4ZqQvaOvbv8RR47YBlHYAwEDuUC0Vy9g03T0G7V/TV\nTFNQU+I2wIm6VQFFbhjFYYCECILHPNwRp8XN0VKSiTqj5ilPa2wdPsBEgwNKlILn\nv9iTx9IdyFeMmCqIWgeFX5sHddvgq5Dep7kBRVh7ZM1+hOS8kw2qmZgKX8Zwgz3E\n0En/2r+3YgWtMxTz6iqW/Op0UagrlR5EgysjrNgakJEJQA/x23SataJOpVvSE9pH\nSCyzrIaseg1gtz5huDVO5GOK3Xg/VUr2n3sk98MQtHWWaEfcpstSrrefjTC4IYN5\n2QIDAQAB\n-----END PUBLIC KEY-----\n"
      },
      {
        "challenge": "6bfZOoD9L35qO1GIzVHcv9sX0UEzKCTru8yz1U7NK4o7y0gnXoU3Ak47sFFY4Yzb",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwpxT5iX72pkd/m8Fb3mg\nMkCQMoWb3FKAjHsutKpUEMA0ts1atZe7WFBRcCxV2mTDeWFpSwWjuYYSNNrEgk9e\nBRiLJ/36hCewnzw9PZMPcnWv+QLbyLsr4jAEVHk2pWln2HkVbAmK2OWEhvlUjxyT\nfB0b1UsBP3uy5f+SLb8iltvwWZGauT64JrLpbIwhk6SbXOCZSZtsXVZ5mVPEIxik\nZ4iBT3r+9Fc3fgKN/16bjdHw+qbWxovEYejG10Yp1yO4QjSzkxQsXTFvsWxaTKF2\ncZa5GF19b9ZkY3SRxHF6emA720F+N4oeGuV0Zu/ACYfMqRUSkh5GiOpv6VxvuXRD\n0wIDAQAB\n-----END PUBLIC KEY-----\n"
      },
      {
        "challenge": "NNH3Pt3F-OvaeYR_Dynp_nbHMuLaVYBnkG7uJtwz2-lShyLaHNjOyjBnL-eGjoRY",
        "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsrrPGkxbk08x5CpkUk5y\nfWBmfiE4qU4IWaSO9HCBv5uRWJvDqXkKjkcBptwmGFsnzT+owfSe+21nWLOLZqwW\nmPbV0bW3e7l3ZUw/4fUga+KJDR5OfkkXWSos1cEMhxsSMnGykhx2/ge9bqY0Edbr\nzckOT2un87ThdawveS3hOxTczE+JcgzoI+CUxlPV0c9yJ5iNFZXf1p7wj3Rq2I8X\nAl4XyMP/+0TLR5+UTrrxLC4ds4m9EjMPRv4aNJFqzBfb3WBM/DFVvNR82Mt2pfF8\nlv6RyZU/vls6vjDl42NK3hckOhEGqQpPmifKgPCaOwdLHg68CjQZ54GWGqyFGzNx\nHwIDAQAB\n-----END PUBLIC KEY-----\n"
      }
    ],
    "requiredApproverCount": 3
  }
}

"""


# Test case 1: Successful build and components add
def test_build_custom_gcloud_success(mock_subprocess_run):
    # Setup: Mock successful gcloud execution
    mock_subprocess_run.side_effect = [
        subprocess.CompletedProcess(
            args=gcloud_commands.command_build_custom_gcloud,
            returncode=0,
            stdout="gcloud build successful!",
            stderr="",
        ),
        subprocess.CompletedProcess(
            args=gcloud_commands.command_add_components,
            returncode=0,
            stdout="gcloud components add successful.",
            stderr="",
        ),
    ]

    # Action: Call the function
    result = gcloud_commands.build_custom_gcloud()

    # Assert: Verify the return value and that subprocess.run was called correctly
    assert result.returncode == 0
    assert result.stdout == "gcloud components add successful."
    assert mock_subprocess_run.call_count == 2
    mock_subprocess_run.assert_has_calls(
        [
            mock.call(
                gcloud_commands.command_build_custom_gcloud,
                check=True,
                shell=True,
                capture_output=True,
                text=True,
            ),
            mock.call(
                gcloud_commands.command_add_components,
                check=True,
                shell=True,
                capture_output=True,
                text=True,
            ),
        ]
    )


# Test case 2: gcloud build fails
def test_build_custom_gcloud_build_error(mock_subprocess_run):
    # Setup: Mock gcloud build command with a non-zero return code
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1,
        cmd=gcloud_commands.command_build_custom_gcloud,
        output="",
        stderr="Error: Build failed",
    )

    # Action & Assert: Call the function and verify that the
    # CalledProcessError is re-raised
    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        gcloud_commands.build_custom_gcloud()

    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Error: Build failed"
    assert exc_info.value.cmd == gcloud_commands.command_build_custom_gcloud
    assert mock_subprocess_run.call_count == 1


# Test case 3: gcloud components add fails
def test_build_custom_gcloud_components_error(mock_subprocess_run):
    # Setup: Mock gcloud build success and components add with error
    mock_subprocess_run.side_effect = [
        subprocess.CompletedProcess(
            args=gcloud_commands.command_build_custom_gcloud,
            returncode=0,
            stdout="gcloud build successful!",
            stderr="",
        ),
        subprocess.CalledProcessError(
            returncode=1,
            cmd=gcloud_commands.command_add_components,
            output="",
            stderr="Error: Components add failed",
        ),
    ]

    # Action & Assert: Call the function and verify that the
    # CalledProcessError is re-raised
    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        gcloud_commands.build_custom_gcloud()

    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Error: Components add failed"
    assert exc_info.value.cmd == gcloud_commands.command_add_components
    assert mock_subprocess_run.call_count == 2


@pytest.fixture
def mock_subprocess_run(monkeypatch):
    mock_run = mock.create_autospec(subprocess.run)
    monkeypatch.setattr(subprocess, "run", mock_run)
    return mock_run


def test_fetch_challenges_success(mock_subprocess_run):
    # Setup: Configure the mock to simulate a successful gcloud command
    mock_process_result = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout=sample_fetch_challenge_output,
        stderr="",
    )
    mock_subprocess_run.return_value = mock_process_result

    # Action: Call the function
    resource = test_proposal_resource
    result = gcloud_commands.fetch_challenges(resource)

    # Assertions: Verify the results
    mock_subprocess_run.assert_called_once_with(
        gcloud_commands.command_gcloud_describe_proposal + resource + " --format=json",
        capture_output=True,
        check=True,
        text=True,
        shell=True,
    )
    assert result == mock_process_result
    assert result.returncode == 0
    assert result.stdout == sample_fetch_challenge_output
    assert not result.stderr


def test_fetch_challenges_error(mock_subprocess_run):
    # Setup: Configure the mock to simulate a failed gcloud command
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="", output="", stderr="Error: Invalid resource"
    )

    # Action & Assert: Call the function and check for the expected exception
    resource = "invalid-resource"
    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        gcloud_commands.fetch_challenges(resource)

    # Verify the exception details
    assert exc_info.value.returncode == 1
    assert exc_info.value.stderr == "Error: Invalid resource"


def test_fetch_challenges_command_construction(mock_subprocess_run):
    # Setup:
    mock_process_result = subprocess.CompletedProcess(
        args=[],
        returncode=0,
        stdout="{}",
        stderr="",
    )
    mock_subprocess_run.return_value = mock_process_result
    resource = test_proposal_resource

    # Action: Call the function
    gcloud_commands.fetch_challenges(resource)

    # Assertions: Verify the command
    mock_subprocess_run.assert_called_once_with(
        gcloud_commands.command_gcloud_describe_proposal + resource + " --format=json",
        capture_output=True,
        check=True,
        text=True,
        shell=True,
    )


def test_fetch_challenges_output_capture(mock_subprocess_run):
    # Setup:
    expected_stdout = "Expected Output"
    expected_stderr = "Expected Error"
    expected_returncode = 0
    mock_process_result = subprocess.CompletedProcess(
        args=[],
        returncode=expected_returncode,
        stdout=expected_stdout,
        stderr=expected_stderr,
    )
    mock_subprocess_run.return_value = mock_process_result
    resource = test_proposal_resource
    # Action: Call the function
    result = gcloud_commands.fetch_challenges(resource)

    # Assertions: Verify the captured output
    assert result.stdout == expected_stdout
    assert result.stderr == expected_stderr
    assert result.returncode == expected_returncode


# Test case 1: Successful gcloud command
def test_send_signed_challenges_success(mock_subprocess_run):
    # Setup: Mock successful gcloud execution
    signed_files = [("signed_challenge.bin", "public_key_1.pem")]
    proposal = "my-proposal"
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=[],  # Not checked in this test, but good practice to include
        returncode=0,
        stdout="gcloud command successful!",
        stderr="",
    )

    # Action: Call the function
    result = gcloud_commands.send_signed_challenges(signed_files, proposal)

    # Assert: Verify the return value and that subprocess.run was called correctly
    assert result.returncode == 0
    assert result.stdout == "gcloud command successful!"
    expected_command = " ".join(
        gcloud_commands.command_gcloud_approve_proposal
        + [proposal]
        + ["--challenge_replies=\"[('signed_challenge.bin'," " 'public_key_1.pem')]\""]
    )
    mock_subprocess_run.assert_called_once_with(
        expected_command,
        capture_output=True,
        check=True,
        text=True,
        shell=True,
    )


# Test case 2: gcloud command returns an error code
def test_send_signed_challenges_gcloud_error(mock_subprocess_run):
    # Setup: Mock gcloud command with a non-zero return code and stderr
    signed_files = [("signed_challenge.bin", "public_key_1.pem")]
    proposal = "my-proposal"
    mock_subprocess_run.return_value = subprocess.CompletedProcess(
        args=[],
        returncode=1,
        stdout="",
        stderr="Error: Invalid proposal resource",
    )

    # Action: Call the function
    result = gcloud_commands.send_signed_challenges(signed_files, proposal)

    # Assert: Verify the return value
    assert result.returncode == 1
    assert result.stderr == "Error: Invalid proposal resource"


# Test case 3: subprocess.run raises a CalledProcessError
def test_send_signed_challenges_called_process_error(mock_subprocess_run):
    # Setup: Mock subprocess.run to raise a CalledProcessError
    signed_files = [("signed_challenge.bin", "public_key_1.pem")]
    proposal = "my-proposal"
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        returncode=2,
        cmd="test_command",
        output="",
        stderr="Called process error",
    )

    # Action & Assert: Call the function and verify that the
    # CalledProcessError is re-raised
    with pytest.raises(subprocess.CalledProcessError) as exc_info:
        gcloud_commands.send_signed_challenges(signed_files, proposal)

    assert exc_info.value.returncode == 2
    assert exc_info.value.stderr == "Called process error"
    assert exc_info.value.cmd == "test_command"


# Test case 4: Signed challenge file list is empty.
def test_send_signed_challenges_empty_list(mock_subprocess_run):

    # Action: Call the function
    with pytest.raises(ValueError, match="signed_challenged_files is empty"):
        gcloud_commands.send_signed_challenges([], test_proposal_resource)
