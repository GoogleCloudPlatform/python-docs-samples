#!/usr/bin/env python

# Copyright (C) 2016 Google Inc.
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

"""Example of using the Compute Engine API to manage a set of rolling
disk snapshots.

./manage-backups.py  --disk <disk1>,<zone1> \
    --disk <disk2>,<zone2> \
    --project <project>

"""

import argparse
import datetime
import json
import re
import sys

from googleapiclient import discovery
import iso8601
from oauth2client.client import GoogleCredentials
import pytz


DISK_ZONE_MAP = {}


def list_snapshots(compute, project, filter=None, pageToken=None):
    return compute.snapshots().list(
        project=project, pageToken=pageToken, filter=filter).execute()


def should_snapshot(items, minimum_delta):
    """Given a list of snapshot items, return True if a snapshot should be
    taken, False if not.
    """
    sorted_items = items[:]
    sorted_items.sort(key=lambda x: x['creationTimestamp'])
    sorted_items.reverse()

    now = datetime.datetime.now(pytz.utc)
    created = iso8601.parse_date(sorted_items[0]['creationTimestamp'])

    if now > created + minimum_delta:
        return True

    return False


def deletable_items(items):
    """Given a list of snapshot items, return the snapshots than can be
    deleted.
    """
    _items = items[:]
    _items.sort(key=lambda x: x['creationTimestamp'])
    _items.reverse()

    result = []
    now = datetime.datetime.now(pytz.utc)
    one_week = datetime.timedelta(days=7)
    three_months = datetime.timedelta(weeks=13)
    one_year = datetime.timedelta(weeks=52)
    minimum_number = 1

    # Strategy: look for a reason not to delete. If none found,
    # add to list.

    # Global reasons

    if len(items) < minimum_number:
        print('Fewer than {0} snapshots, not deleting any'.format(
            minimum_number))
        return result

    # Item-specific reasons

    for item in _items[1:]: #always skip newest snapshot

        item_timestamp = iso8601.parse_date(item['creationTimestamp'])
        snapshot_age = now - item_timestamp

        if snapshot_age < one_week:
            print('Snapshot "{0}" too new, not deleting.'.format(item['name']))
            continue

        if item_timestamp.weekday() == 1 and snapshot_age < three_months:
            message = 'Snapshot "{}" is weekly timestamp and too new,'
            message += ' not deleting.'
            print(message.format(item['name']))
            continue

        if item_timestamp.day == 1 and snapshot_age < one_year:
            message = 'Snapshot "{}" is monthly timestamp and too new,'
            message += ' not deleting.'
            print(message.format(item['name']))
            continue

        print('Adding snapshot "{}" to the delete list'.format(item['name']))
        result.append(item)

    return result


def create_snapshot(compute, project, disk, dry_run):
    now = datetime.datetime.now(pytz.utc)
    name = '{}-{}'.format(disk, now.strftime('%Y-%m-%d'))
    zone = zone_from_disk(disk)
    print('Creating snapshot "{}" in zone "{}"'.format(disk, zone))

    if not dry_run:
        result = compute.disks().createSnapshot(project=project, disk=disk,
            body={'name':name}, zone=zone).execute()


def delete_snapshots(compute, project, snapshots, dry_run):
    for snapshot in snapshots:
        print('Deleting snapshot "{0}"'.format(snapshot['name']))

        if not dry_run:
            result = compute.snapshots().delete(project=project,
                snapshot=snapshot['name']).execute()


def zone_from_disk(disk):
    return DISK_ZONE_MAP[disk]


def update_snapshots(compute, project, disk, dry_run):

    filter = 'name eq {}-[0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}}'.format(disk)
    result = list_snapshots(compute, project, filter=filter)

    if not result.has_key('items'):
        message = 'Disk "{}" has no snapshots.'
        message += ' Possibly it\'s new or you have a typo.'
        print(message.format(disk))
        snapshot_p = True
        items_to_delete = []
    else:
        snapshot_p = should_snapshot(result['items'],
            datetime.timedelta(days=1))
        items_to_delete = deletable_items(result['items'])

    if snapshot_p:
        create_snapshot(compute, project, disk, dry_run)

    if len(items_to_delete):
        delete_snapshots(compute, project, items_to_delete, dry_run)


def main(args):

    disks = []
    for diskzone in args.disk:
        disk, zone = diskzone.split(',')
        DISK_ZONE_MAP[disk] = zone
        disks.append(disk)

    credentials = GoogleCredentials.get_application_default()
    compute = discovery.build('compute', 'v1', credentials=credentials)
    project = args.project

    for disk in disks:
        update_snapshots(compute, project, disk, args.dry_run)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('--dry-run',
        help='Show what actions would be run, but don\'t actually run them.',
        action='store_true')
    parser.add_argument('--project', help='GCE project.', required=True)
    parser.add_argument('--disk', help='Disk and zone, comma-separated.',
                        action='append', required=True)

    args = parser.parse_args()

    for diskzone in args.disk:
        try:
            diskzone.index(',')
        except ValueError:
            message = 'Disk "{}" has no comma.  Should be <disk,zone>.'
            print(message.format(disk))
            sys.exit(1)

    main(args)
