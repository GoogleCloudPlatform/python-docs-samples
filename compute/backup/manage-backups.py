#!/usr/bin/python

# pip install --upgrade google-api-python-client
# pip install --upgrade iso8601
# pip install --upgrade rfc3339
# pip install --upgrade pytz

import simplejson as json
import iso8601
import datetime
import pytz
import sys
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
import re
import argparse

DISK_ZONE_MAP = {}

def list_snapshots(compute, project, filter=None, pageToken=None):
    result = compute.snapshots().list(project=project, pageToken=pageToken, filter=filter).execute()
    return result

# Given a list of snapshot items, return True if a snapshot should be
# taken, False if not.
def should_snapshot(items, minimum_delta):
    _items = items[:]
    _items.sort(key=lambda x: x['creationTimestamp'])
    _items.reverse()
    if datetime.datetime.now(pytz.utc) > iso8601.parse_date(_items[0]['creationTimestamp']) \
        + minimum_delta:
        return True
    return False


# Given a list of snapshot items, return the snapshots than can be
# deleted.
def deletable_items(items):
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
        print "Fewer than %d snapshots, not deleting any" % minimum_number
        return result

    # Item-specific reasons

    for item in _items[1:]: #always skip newest snapshot

        item_timestamp = iso8601.parse_date(item['creationTimestamp'])

        if now - item_timestamp < one_week:
            print "Snapshot '%s' too new, not deleting." % item['name']
            continue

        if item_timestamp.weekday() == 1 and now - item_timestamp < three_months:
            print "Snapshot '%s' is weekly timestamp and too new, not deleting." % item['name']
            continue

        if item_timestamp.day == 1 and now - item_timestamp < one_year:
            print "Snapshot '%s' is monthly timestamp and too new, not deleting." % item['name']
            continue

        print "Adding snapshot '%s' to the delete list" % item['name']
        result.append(item)

    return result

def create_snapshot(compute,project,disk,dry_run):

    now = datetime.datetime.now(pytz.utc)
    name = "%s-%s" % (disk,now.strftime('%Y-%m-%d'))
    zone = zone_from_disk(disk)
    print "Creating snapshot '%s' in zone '%s'" % (disk,zone)
    if not dry_run:
        result = compute.disks().createSnapshot(project=project, disk=disk, body={"name":name}, zone=zone).execute()

def delete_snapshots(compute,project,snapshots,dry_run):
    for snapshot in snapshots:
        print "Deleting snapshot '%s'" % snapshot['name']
        if not dry_run:
            result = compute.snapshots().delete(project=project, snapshot=snapshot['name']).execute()

def zone_from_disk(disk):
    return DISK_ZONE_MAP[disk]

def update_snapshots(compute,project,disk,dry_run):

    filter = "name eq %s-[0-9]{4}-[0-9]{2}-[0-9]{2}" % disk
    result = list_snapshots(compute,project,filter=filter)

    if not result.has_key('items'):
        print "Disk '%s' has no snapshots. Possibly it's new or you have a typo." % disk
        snapshot_p = True
        items_to_delete = []
    else:
        snapshot_p = should_snapshot(result['items'],datetime.timedelta(days=1))
        items_to_delete = deletable_items(result['items'])

    if snapshot_p:
        create_snapshot(compute,project,disk,dry_run)

    if len(items_to_delete):
        delete_snapshots(compute,project,items_to_deelete,dry_run)

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
        update_snapshots(compute,project,disk,args.dry_run)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Make and manage disk snapshots.')
    parser.add_argument('--dry-run', help="Show what actions would be run, but don't actually run them.",
                        action="store_true")
    parser.add_argument('--project', help="GCE project.", required=True)
    parser.add_argument('--disk', help="Disk and zone, comma-separated.",
                        action="append", required=True)

    args = parser.parse_args()

    for diskzone in args.disk:
        try:
            diskzone.index(',')
        except ValueError:
            print "Disk '%s' has no comma.  Should be <disk,zone>." % disk
            sys.exit(1)

    main(args)
