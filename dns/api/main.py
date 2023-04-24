# Copyright 2016 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from google.cloud import dns
from google.cloud.exceptions import NotFound


# [START create_zone]
def create_zone(project_id, name, dns_name, description):
    client = dns.Client(project=project_id)
    zone = client.zone(
        name,  # examplezonename
        dns_name=dns_name,  # example.com.
        description=description)
    zone.create()
    return zone
# [END create_zone]


# [START get_zone]
def get_zone(project_id, name):
    client = dns.Client(project=project_id)
    zone = client.zone(name=name)

    try:
        zone.reload()
        return zone
    except NotFound:
        return None
# [END get_zone]


# [START list_zones]
def list_zones(project_id):
    client = dns.Client(project=project_id)
    zones = client.list_zones()
    return [zone.name for zone in zones]
# [END list_zones]


# [START delete_zone]
def delete_zone(project_id, name):
    client = dns.Client(project=project_id)
    zone = client.zone(name)
    zone.delete()
# [END delete_zone]


# [START list_resource_records]
def list_resource_records(project_id, zone_name):
    client = dns.Client(project=project_id)
    zone = client.zone(zone_name)

    records = zone.list_resource_record_sets()

    return [(record.name, record.record_type, record.ttl, record.rrdatas)
            for record in records]
# [END list_resource_records]


# [START changes]
def list_changes(project_id, zone_name):
    client = dns.Client(project=project_id)
    zone = client.zone(zone_name)

    changes = zone.list_changes()

    return [(change.started, change.status) for change in changes]
# [END changes]


def create_command(args):
    """Adds a zone with the given name, DNS name, and description."""
    zone = create_zone(
        args.project_id, args.name, args.dns_name, args.description)
    print(f'Zone {zone.name} added.')


def get_command(args):
    """Gets a zone by name."""
    zone = get_zone(args.project_id, args.name)
    if not zone:
        print('Zone not found.')
    else:
        print('Zone: {}, {}, {}'.format(
            zone.name, zone.dns_name, zone.description))


def list_command(args):
    """Lists all zones."""
    print(list_zones(args.project_id))


def delete_command(args):
    """Deletes a zone."""
    delete_zone(args.project_id, args.name)
    print(f'Zone {args.name} deleted.')


def list_resource_records_command(args):
    """List all resource records for a zone."""
    records = list_resource_records(args.project_id, args.name)
    for record in records:
        print(record)


def changes_command(args):
    """List all changes records for a zone."""
    changes = list_changes(args.project_id, args.name)
    for change in changes:
        print(change)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.add_argument('--project-id', help='Your cloud project ID.')

    create_parser = subparsers.add_parser(
        'create', help=create_command.__doc__)
    create_parser.set_defaults(func=create_command)
    create_parser.add_argument('name', help='New zone name, e.g. "azonename".')
    create_parser.add_argument(
        'dns_name', help='New zone dns name, e.g. "example.com."')
    create_parser.add_argument('description', help='New zone description.')

    get_parser = subparsers.add_parser('get', help=get_command.__doc__)
    get_parser.add_argument('name', help='Zone name, e.g. "azonename".')
    get_parser.set_defaults(func=get_command)

    list_parser = subparsers.add_parser('list', help=list_command.__doc__)
    list_parser.set_defaults(func=list_command)

    delete_parser = subparsers.add_parser(
        'delete', help=delete_command.__doc__)
    delete_parser.add_argument('name', help='Zone name, e.g. "azonename".')
    delete_parser.set_defaults(func=delete_command)

    list_rr_parser = subparsers.add_parser(
        'list-resource-records', help=list_resource_records_command.__doc__)
    list_rr_parser.add_argument('name', help='Zone name, e.g. "azonename".')
    list_rr_parser.set_defaults(func=list_resource_records_command)

    changes_parser = subparsers.add_parser(
        'changes', help=changes_command.__doc__)
    changes_parser.add_argument('name', help='Zone name, e.g. "azonename".')
    changes_parser.set_defaults(func=changes_command)

    args = parser.parse_args()

    args.func(args)
