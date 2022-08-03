#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
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

"""Example of using the OS Login API to apply public SSH keys for a service
account, and use that service account to execute commands on a remote
instance over SSH. This example uses zonal DNS names to address instances
on the same internal VPC network.
"""

# [START imports_and_variables]
import argparse
import logging
import subprocess
import time
import uuid

from google.auth.exceptions import RefreshError
import googleapiclient.discovery
import requests

SERVICE_ACCOUNT_METADATA_URL = (
    'http://metadata.google.internal/computeMetadata/v1/instance/'
    'service-accounts/default/email')
HEADERS = {'Metadata-Flavor': 'Google'}

# [END imports_and_variables]


# [START run_command_local]
def execute(cmd, cwd=None, capture_output=False, env=None, raise_errors=True):
    """Execute an external command (wrapper for Python subprocess)."""
    logging.info('Executing command: {cmd}'.format(cmd=str(cmd)))
    stdout = subprocess.PIPE if capture_output else None
    process = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=stdout)
    output = process.communicate()[0]
    returncode = process.returncode
    if returncode:
        # Error
        if raise_errors:
            raise subprocess.CalledProcessError(returncode, cmd)
        else:
            logging.info('Command returned error status %s', returncode)
    if output:
        logging.info(output)
    return returncode, output
# [END run_command_local]


# [START create_key]
def create_ssh_key(oslogin, account, private_key_file=None, expire_time=300):
    """Generate an SSH key pair and apply it to the specified account."""
    private_key_file = private_key_file or '/tmp/key-' + str(uuid.uuid4())
    execute(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', private_key_file])

    with open(private_key_file + '.pub', 'r') as original:
        public_key = original.read().strip()

    # Expiration time is in microseconds.
    expiration = int((time.time() + expire_time) * 1000000)

    body = {
        'key': public_key,
        'expirationTimeUsec': expiration,
    }
    print(f'Creating key {account} and {body}')
    for attempt_no in range(1, 4):
        try:
            # This method sometimes failed to work causing issues like #7277
            # Maybe retrying it with some delay will make things better
            oslogin.users().importSshPublicKey(parent=account, body=body).execute()
        except RefreshError as err:
            if attempt_no == 3:
                raise err
            time.sleep(attempt_no)
        else:
            break

    return private_key_file
# [END create_key]


# [START run_command_remote]
def run_ssh(cmd, private_key_file, username, hostname):
    """Run a command on a remote system."""
    ssh_command = [
        'ssh', '-i', private_key_file, '-o', 'StrictHostKeyChecking=no',
        '{username}@{hostname}'.format(username=username, hostname=hostname),
        cmd,
    ]
    ssh = subprocess.Popen(
        ssh_command, shell=False, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    return result if result else ssh.stderr.readlines()

# [END run_command_remote]


# [START main]
def main(cmd, project, instance=None, zone=None,
         oslogin=None, account=None, hostname=None):
    """Run a command on a remote system."""

    # Create the OS Login API object.
    oslogin = oslogin or googleapiclient.discovery.build('oslogin', 'v1')

    # Identify the service account ID if it is not already provided.
    account = account or requests.get(
        SERVICE_ACCOUNT_METADATA_URL, headers=HEADERS).text
    if not account.startswith('users/'):
        account = 'users/' + account

    # Create a new SSH key pair and associate it with the service account.
    private_key_file = create_ssh_key(oslogin, account)

    # Using the OS Login API, get the POSIX username from the login profile
    # for the service account.
    for attempt_no in range(1, 4):
        try:
            profile = oslogin.users().getLoginProfile(name=account).execute()
        except RefreshError as err:
            if attempt_no == 3:
                raise err
            time.sleep(attempt_no)
        else:
            username = profile.get('posixAccounts')[0].get('username')
            break

    # Create the hostname of the target instance using the instance name,
    # the zone where the instance is located, and the project that owns the
    # instance.
    hostname = hostname or '{instance}.{zone}.c.{project}.internal'.format(
        instance=instance, zone=zone, project=project)

    # Run a command on the remote instance over SSH.
    result = run_ssh(cmd, private_key_file, username, hostname)

    # Print the command line output from the remote instance.
    # Use .rstrip() rather than end='' for Python 2 compatability.
    for line in result:
        print(line.decode('utf-8').rstrip('\n\r'))

    # Shred the private key and delete the pair.
    execute(['shred', private_key_file])
    execute(['rm', private_key_file])
    execute(['rm', private_key_file + '.pub'])


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

# [END main]
