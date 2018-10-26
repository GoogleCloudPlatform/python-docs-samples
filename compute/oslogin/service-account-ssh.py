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
import time
import subprocess
import uuid
import logging
import requests
import googleapiclient.discovery

#  Global variables
PROJECT = 'my-project-id'
INSTANCE = 'my-instance-name'
ZONE = 'us-central1-a'
SERVICE_ACCOUNT_METADATA_URL = (
    'http://metadata.google.internal/computeMetadata/v1/instance/'
    'service-accounts/default/email')
HEADERS = {'Metadata-Flavor': 'Google'}
CMD = 'uname -a' # The command to run on the remote instance.

# [END imports_and_variables]

# [START run_command_local]
def execute(cmd, cwd=None, capture_output=False, env=None, raise_errors=True):
    """Execute an external command (wrapper for Python subprocess)."""
    logging.info('Executing command: %s' % str(cmd))
    stdout = subprocess.PIPE if capture_output else None
    process = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=stdout)
    output = process.communicate()[0]
    returncode = process.returncode
    if returncode != 0:
        # Error
        if raise_errors:
            raise subprocess.CalledProcessError(returncode, CMD)
        else:
            logging.info('Command returned error status %d' % returncode)
    if output:
        logging.info(output)
    return returncode, output
# [END run_command_local]

# [START create_key]
def create_ssh_key(oslogin, account, private_key_file=None, expire_time=300):
    """Generate an SSH key pair and apply it to the specified account."""
    private_key_file = private_key_file or '/tmp/ssh-key-%s' % str(uuid.uuid4())
    execute(['ssh-keygen', '-t', 'rsa', '-N', '', '-f', private_key_file])

    with open(private_key_file + '.pub', 'r') as original:
        public_key = original.read().strip()

    # Expiration time is in microseconds.
    expiration = int((time.time() + expire_time) * 1000000)

    body = {
        'key': public_key,
        'expirationTimeUsec': expiration
    }
    oslogin.users().importSshPublicKey(parent=account, body=body).execute()
    return private_key_file
# [END create_key]

# [START run_command_remote]
def run_ssh(cmd, private_key_file, username, hostname):
    """Run a command on a remote system."""
    ssh_command = [
        'ssh', '-i', private_key_file, '-o', 'StrictHostKeyChecking=no',
        '%s@%s' % (username, hostname), cmd,
    ]
    ssh = subprocess.Popen(
        ssh_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = ssh.stdout.readlines()
    if result == []:
        error = ssh.stderr.readlines()
        print(error)
    else:
        print(result[0].decode('utf-8'))
# [END run_command_remote]

# [START main]
def main():
    """Run a command on a remote system."""

    # Get the service account name from instance metadata values.
    response = requests.get(SERVICE_ACCOUNT_METADATA_URL, headers=HEADERS)
    account = 'users/' + response.text

    # Create the OS Login API object.
    oslogin = googleapiclient.discovery.build('oslogin', 'v1')

    # Create the SSH key pair and return the private key file path as a variable.
    private_key_file = create_ssh_key(oslogin, account)

    # Using the OS Login API, get the POSIX user name from the login profile for
    # the service account.
    profile = oslogin.users().getLoginProfile(name=account).execute()
    username = profile.get('posixAccounts')[0].get('username')

    # Create the hostname of the target instance using the instance name,
    # the zone where the instance is located, and the project that owns the
    # instance.
    hostname = '{instance}.{zone}.c.{project}.internal'.format(
        instance=INSTANCE, zone=ZONE, project=PROJECT)

    # Run a command on the remote instance over SSH.
    run_ssh(CMD, private_key_file, username, hostname)

    # Shred the private key and delete the pair.
    execute(['shred', private_key_file])
    execute(['rm', private_key_file])
    execute(['rm', private_key_file + ".pub"])

if __name__ == '__main__':

    main()
# [END main]
