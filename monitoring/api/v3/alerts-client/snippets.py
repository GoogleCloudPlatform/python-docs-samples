# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import json
import os

from google.cloud import monitoring_v3
import google.protobuf.json_format
import tabulate


# [START monitoring_alert_list_policies]
def list_alert_policies(project_name):
    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(project_name)
    print(tabulate.tabulate(
        [(policy.name, policy.display_name) for policy in policies],
        ('name', 'display_name')))
# [END monitoring_alert_list_policies]


# [START monitoring_alert_list_channels]
def list_notification_channels(project_name):
    client = monitoring_v3.NotificationChannelServiceClient()
    channels = client.list_notification_channels(project_name)
    print(tabulate.tabulate(
        [(channel.name, channel.display_name) for channel in channels],
        ('name', 'display_name')))
# [END monitoring_alert_list_channels]


# [START monitoring_alert_enable_policies]
def enable_alert_policies(project_name, enable, filter_=None):
    """Enable or disable alert policies in a project.

    Arguments:
        project_name (str)
        enable (bool): Enable or disable the policies.
        filter_ (str, optional): Only enable/disable alert policies that match
            this filter_.  See
            https://cloud.google.com/monitoring/api/v3/sorting-and-filtering
    """

    client = monitoring_v3.AlertPolicyServiceClient()
    policies = client.list_alert_policies(project_name, filter_=filter_)

    for policy in policies:
        if bool(enable) == policy.enabled.value:
            print('Policy', policy.name, 'is already',
                  'enabled' if policy.enabled.value else 'disabled')
        else:
            policy.enabled.value = bool(enable)
            mask = monitoring_v3.types.field_mask_pb2.FieldMask()
            mask.paths.append('enabled')
            client.update_alert_policy(policy, mask)
            print('Enabled' if enable else 'Disabled', policy.name)
# [END monitoring_alert_enable_policies]


# [START monitoring_alert_replace_channels]
def replace_notification_channels(project_name, alert_policy_id, channel_ids):
    _, project_id = project_name.split('/')
    alert_client = monitoring_v3.AlertPolicyServiceClient()
    channel_client = monitoring_v3.NotificationChannelServiceClient()
    policy = monitoring_v3.types.alert_pb2.AlertPolicy()
    policy.name = alert_client.alert_policy_path(project_id, alert_policy_id)

    for channel_id in channel_ids:
        policy.notification_channels.append(
            channel_client.notification_channel_path(project_id, channel_id))

    mask = monitoring_v3.types.field_mask_pb2.FieldMask()
    mask.paths.append('notification_channels')
    updated_policy = alert_client.update_alert_policy(policy, mask)
    print('Updated', updated_policy.name)
# [END monitoring_alert_replace_channels]


# [START monitoring_alert_backup_policies]
def backup(project_name):
    alert_client = monitoring_v3.AlertPolicyServiceClient()
    channel_client = monitoring_v3.NotificationChannelServiceClient()
    record = {'project_name': project_name,
              'policies': list(alert_client.list_alert_policies(project_name)),
              'channels': list(channel_client.list_notification_channels(
                  project_name))}
    json.dump(record, open('backup.json', 'wt'), cls=ProtoEncoder, indent=2)
    print('Backed up alert policies and notification channels to backup.json.')


class ProtoEncoder(json.JSONEncoder):
    """Uses google.protobuf.json_format to encode protobufs as json."""
    def default(self, obj):
        if type(obj) in (monitoring_v3.types.alert_pb2.AlertPolicy,
                         monitoring_v3.types.notification_pb2.
                         NotificationChannel):
            text = google.protobuf.json_format.MessageToJson(obj)
            return json.loads(text)
        return super(ProtoEncoder, self).default(obj)
# [END monitoring_alert_backup_policies]


# [START monitoring_alert_restore_policies]
# [START monitoring_alert_create_policy]
# [START monitoring_alert_create_channel]
# [START monitoring_alert_update_channel]
def restore(project_name):
    print('Loading alert policies and notification channels from backup.json.')
    record = json.load(open('backup.json', 'rt'))
    is_same_project = project_name == record['project_name']
    # Convert dicts to AlertPolicies.
    policies_json = [json.dumps(policy) for policy in record['policies']]
    policies = [google.protobuf.json_format.Parse(
        policy_json, monitoring_v3.types.alert_pb2.AlertPolicy())
        for policy_json in policies_json]
    # Convert dicts to NotificationChannels
    channels_json = [json.dumps(channel) for channel in record['channels']]
    channels = [google.protobuf.json_format.Parse(
        channel_json, monitoring_v3.types.notification_pb2.
        NotificationChannel()) for channel_json in channels_json]

    # Restore the channels.
    channel_client = monitoring_v3.NotificationChannelServiceClient()
    channel_name_map = {}

    for channel in channels:
        updated = False
        print('Updating channel', channel.display_name)
        # This field is immutable and it is illegal to specify a
        # non-default value (UNVERIFIED or VERIFIED) in the
        # Create() or Update() operations.
        channel.verification_status = monitoring_v3.enums.NotificationChannel.\
            VerificationStatus.VERIFICATION_STATUS_UNSPECIFIED

        if is_same_project:
            try:
                channel_client.update_notification_channel(channel)
                updated = True
            except google.api_core.exceptions.NotFound:
                pass  # The channel was deleted.  Create it below.

        if not updated:
            # The channel no longer exists.  Recreate it.
            old_name = channel.name
            channel.ClearField("name")
            new_channel = channel_client.create_notification_channel(
                project_name, channel)
            channel_name_map[old_name] = new_channel.name

    # Restore the alerts
    alert_client = monitoring_v3.AlertPolicyServiceClient()

    for policy in policies:
        print('Updating policy', policy.display_name)
        # These two fields cannot be set directly, so clear them.
        policy.ClearField('creation_record')
        policy.ClearField('mutation_record')

        # Update old channel names with new channel names.
        for i, channel in enumerate(policy.notification_channels):
            new_channel = channel_name_map.get(channel)
            if new_channel:
                policy.notification_channels[i] = new_channel

        updated = False

        if is_same_project:
            try:
                alert_client.update_alert_policy(policy)
                updated = True
            except google.api_core.exceptions.NotFound:
                pass  # The policy was deleted.  Create it below.
            except google.api_core.exceptions.InvalidArgument:
                # Annoying that API throws InvalidArgument when the policy
                # does not exist.  Seems like it should throw NotFound.
                pass  # The policy was deleted.  Create it below.

        if not updated:
            # The policy no longer exists.  Recreate it.
            old_name = policy.name
            policy.ClearField("name")
            for condition in policy.conditions:
                condition.ClearField("name")
            policy = alert_client.create_alert_policy(project_name, policy)
        print('Updated', policy.name)
# [END monitoring_alert_restore_policies]
# [END monitoring_alert_create_policy]
# [END monitoring_alert_create_channel]
# [END monitoring_alert_update_channel]


class MissingProjectIdError(Exception):
    pass


def project_id():
    """Retreieves the project id from the environment variable.

    Raises:
        MissingProjectIdError -- When not set.

    Returns:
        str -- the project name
    """
    project_id = os.environ['GCLOUD_PROJECT']

    if not project_id:
        raise MissingProjectIdError(
            'Set the environment variable ' +
            'GCLOUD_PROJECT to your Google Cloud Project Id.')
    return project_id


def project_name():
    return 'projects/' + project_id()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Demonstrates AlertPolicy API operations.')

    subparsers = parser.add_subparsers(dest='command')

    list_alert_policies_parser = subparsers.add_parser(
        'list-alert-policies',
        help=list_alert_policies.__doc__
    )

    list_notification_channels_parser = subparsers.add_parser(
        'list-notification-channels',
        help=list_alert_policies.__doc__
    )

    enable_alert_policies_parser = subparsers.add_parser(
        'enable-alert-policies',
        help=enable_alert_policies.__doc__
    )
    enable_alert_policies_parser.add_argument(
        '--filter',
    )

    disable_alert_policies_parser = subparsers.add_parser(
        'disable-alert-policies',
        help=enable_alert_policies.__doc__
    )
    disable_alert_policies_parser.add_argument(
        '--filter',
    )

    replace_notification_channels_parser = subparsers.add_parser(
        'replace-notification-channels',
        help=replace_notification_channels.__doc__
    )
    replace_notification_channels_parser.add_argument(
        '-p', '--alert_policy_id',
        required=True
    )
    replace_notification_channels_parser.add_argument(
        '-c', '--notification_channel_id',
        required=True,
        action='append'
    )

    backup_parser = subparsers.add_parser(
        'backup',
        help=backup.__doc__
    )

    restore_parser = subparsers.add_parser(
        'restore',
        help=restore.__doc__
    )

    args = parser.parse_args()

    if args.command == 'list-alert-policies':
        list_alert_policies(project_name())

    elif args.command == 'list-notification-channels':
        list_notification_channels(project_name())

    elif args.command == 'enable-alert-policies':
        enable_alert_policies(project_name(), enable=True, filter_=args.filter)

    elif args.command == 'disable-alert-policies':
        enable_alert_policies(project_name(), enable=False,
                              filter_=args.filter)

    elif args.command == 'replace-notification-channels':
        replace_notification_channels(project_name(), args.alert_policy_id,
                                      args.notification_channel_id)

    elif args.command == 'backup':
        backup(project_name())

    elif args.command == 'restore':
        restore(project_name())
