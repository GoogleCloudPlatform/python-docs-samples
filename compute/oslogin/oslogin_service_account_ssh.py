#!/usr/bin/env python
#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# [START compute_oslogin_ssh]
"""
Example of using the OS Login API to apply public SSH keys for a service
account, and use that service account to execute commands on a remote
instance over SSH. This example uses zonal DNS names to address instances
on the same internal VPC network.
"""
import argparse
import subprocess
import time
from typing import List, Optional, Tuple
import uuid

from google.cloud import oslogin_v1
import requests

SERVICE_ACCOUNT_METADATA_URL = (
    'http://metadata.google.internal/computeMetadata/v1/instance/'
    'service-accounts/default/email')
HEADERS = {'Metadata-Flavor': 'Google'}


def execute(
    cmd: List[str],
    cwd: Optional[str] = None,
    capture_output: Optional[bool] = False,
    env: Optional[dict] = None,
    raise_errors: Optional[bool] = True
) -> Tuple[int, str]:
    """
    Executes an external command (wrapper for Python subprocess).

    Args:
        cmd: The command to be executed.
        cwd: Directory in which to execute the command.
        capture_output: Should the command output be captured and returned or just ignored.
        env: Environmental variables passed to the child process.
        raise_errors: Should errors in executed command raise exceptions.

    Returns:
        Return code and captured output.
    """
    print(f'Executing command: {cmd}')
    process = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE if capture_output else subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        check=raise_errors
    )
    output = process.stdout
    returncode = process.returncode

    if returncode:
        print(f'Command returned error status {returncode}')
        if capture_output:
            print(f"With output: {output}")

    return returncode, output


def create_ssh_key(oslogin_client: oslogin_v1.OsLoginServiceClient,
                   account: str, expire_time: int = 300) -> str:
    """
    Generates a temporary SSH key pair and apply it to the specified account.

    Args:
        oslogin_client: OS Login client object.
        account: Name of the service account this key will be assigned to.
            This should be in form of `user/<service_account_username>`.
        expire_time: How many seconds from now should this key be valid.

    Returns:
        The path to private SSH key. Public key can be found by appending `.pub`
        to the file name.

    """
    private_key_file = f'/tmp/key-{uuid.uuid4()}'
    execute(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', private_key_file])

    with open(f'{private_key_file}.pub', 'r') as original:
        public_key = original.read().strip()

    # Expiration time is in microseconds.
    expiration = int((time.time() + expire_time) * 1000000)

    request = oslogin_v1.ImportSshPublicKeyRequest()
    request.parent = account
    request.ssh_public_key.key = public_key
    request.ssh_public_key.expiration_time_usec = expiration

    print(f'Setting key for {account}...')
    oslogin_client.import_ssh_public_key(request)

    # Let the key properly propagate
    time.sleep(5)

    return private_key_file


def run_ssh(cmd: str, private_key_file: str, username: str, hostname: str) -> str:
    """
    Runs a command on a remote system.

    Args:
        cmd: Command to be run.
        private_key_file: Private SSH key to be used for authentication.
        username: Username to be used for authentication.
        hostname: Hostname of the machine you want to run the command on.

    Returns:
        Output of the executed command.
    """
    ssh_command = [
        'ssh',
        '-i', private_key_file,
        '-o', 'StrictHostKeyChecking=no',
        '-o', 'UserKnownHostsFile=/dev/null',
        f'{username}@{hostname}',
        cmd,
    ]
    print(f"Executing ssh command: {' '.join(ssh_command)}")
    tries = 0
    while tries < 3:
        try:
            ssh = subprocess.run(
                ssh_command,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True,
                env={'SSH_AUTH_SOCK': ''},
                timeout=10
            )
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as err:
            time.sleep(30)
            tries += 1
            if tries == 3:
                if isinstance(subprocess.CalledProcessError, err):
                    print(f"Failed to execute SSH command (return code: {err.returncode}. Output received: {err.output}")
                else:
                    print("Failed to execute SSH - timed out.")
                raise err
        else:
            return ssh.stdout


def main(
    cmd,
    project: str,
    instance: Optional[str] = None,
    zone: Optional[str] = None,
    account: Optional[str] = None,
    hostname: Optional[str] = None,
    oslogin: Optional[oslogin_v1.OsLoginServiceClient] = None
) -> None:
    """Runs a command on a remote system."""

    # Create the OS Login API object.
    if oslogin is None:
        oslogin = oslogin_v1.OsLoginServiceClient()

    # Identify the service account ID if it is not already provided.
    account = account or requests.get(
        SERVICE_ACCOUNT_METADATA_URL, headers=HEADERS).text

    if not account.startswith('users/'):
        account = f'users/{account}'

    # Create a new SSH key pair and associate it with the service account.
    private_key_file = create_ssh_key(oslogin, account)
    try:
        # Using the OS Login API, get the POSIX username from the login profile
        # for the service account.
        profile = oslogin.get_login_profile(name=account)
        username = profile.posix_accounts[0].username

        # Create the hostname of the target instance using the instance name,
        # the zone where the instance is located, and the project that owns the
        # instance.
        hostname = hostname or f'{instance}.{zone}.c.{project}.internal'

        # Run a command on the remote instance over SSH.
        result = run_ssh(cmd, private_key_file, username, hostname)

        # Print the command line output from the remote instance.
        print(result)
    finally:
        # Shred the private key and delete the pair.
        execute(['shred', private_key_file])
        execute(['rm', private_key_file])
        execute(['rm', f'{private_key_file}.pub'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--cmd', default='uname -a',
        help='The command to run on the remote instance.')
    parser.add_argument(
        '--project',
        help='Your Google Cloud project ID.')
    parser.add_argument(
        '--zone',
        help='The zone where the target instance is located.')
    parser.add_argument(
        '--instance',
        help='The target instance for the ssh command.')
    parser.add_argument(
        '--account',
        help='The service account email.')
    parser.add_argument(
        '--hostname',
        help='The external IP address or hostname for the target instance.')
    args = parser.parse_args()

    main(args.cmd, args.project, instance=args.instance, zone=args.zone,
         account=args.account, hostname=args.hostname)
# [END compute_oslogin_ssh]
