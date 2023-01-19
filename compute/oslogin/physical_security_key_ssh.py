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

# [START compute_oslogin_physical_sk_script]
import argparse
import os
import subprocess

import googleapiclient.discovery


def write_ssh_key_files(security_keys, directory):
    """Store the SSH key files."""
    key_files = []
    for index, key in enumerate(security_keys):
        key_file = os.path.join(directory, "google_sk_%s" % index)
        with open(key_file, "w") as f:
            f.write(key.get("privateKey"))
            os.chmod(key_file, 0o600)
            key_files.append(key_file)
    return key_files


def ssh_command(key_files, username, ip_address):
    """Construct the SSH command for a given IP address and key files."""
    command = ["ssh"]
    for key_file in key_files:
        command.extend(["-i", key_file])
    command.append("{username}@{ip}".format(username=username, ip=ip_address))
    return command


def main(user_key, ip_address, dryrun, directory=None):
    """Configure SSH key files and print SSH command."""
    directory = directory or os.path.join(os.path.expanduser("~"), ".ssh")

    # Create the OS Login API object.
    oslogin = googleapiclient.discovery.build("oslogin", "v1beta")

    # Retrieve security keys and OS Login username from a user's Google account.
    profile = (
        oslogin.users()
        .getLoginProfile(name="users/{}".format(user_key), view="SECURITY_KEY")
        .execute()
    )
    print(profile)

    if "posixAccounts" not in profile:
        print("You don't have a POSIX account configured.")
        return

    username = profile.get("posixAccounts")[0].get("username")

    # Write the SSH private key files.
    security_keys = profile.get("securityKeys")

    if security_keys is None:
        print("It seems that the account you are using to authenticate does not have any security keys assigned to it.")
        print("Please check your Application Default Credentials (https://cloud.google.com/docs/authentication/application-default-credentials).")
        print("More info about security keys: https://support.google.com/accounts/answer/6103523?visit_id=637673282586358398-2383089289&rd=1")
        return

    key_files = write_ssh_key_files(security_keys, directory)

    # Compose the SSH command.
    command = ssh_command(key_files, username, ip_address)

    if dryrun:
        # Print the SSH command.
        print(" ".join(command))
    else:
        # Connect to the IP address over SSH.
        subprocess.call(command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--user_key", help="Your primary email address.")
    parser.add_argument(
        "--ip_address", help="The external IP address of the VM you want to connect to."
    )
    parser.add_argument("--directory", help="The directory to store SSH private keys.")
    parser.add_argument(
        "--dryrun",
        dest="dryrun",
        default=False,
        action="store_true",
        help="Turn off dryrun mode to execute the SSH command",
    )
    args = parser.parse_args()

    main(args.user_key, args.ip_address, args.dryrun, args.directory)
# [END compute_oslogin_physical_sk_script]
