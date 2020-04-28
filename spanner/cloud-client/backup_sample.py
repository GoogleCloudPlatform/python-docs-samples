# Copyright 2020 Google Inc. All Rights Reserved.
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

"""This application demonstrates how to create and restore from backups
using Cloud Spanner.

For more information, see the README.rst under /spanner.
"""

import argparse
from datetime import (
    datetime,
    timedelta
)
import time

from google.cloud import spanner


# [START spanner_create_backup]
def create_backup(instance_id, database_id, backup_id):
    """Creates a backup for a database."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    # Create a backup
    expire_time = datetime.utcnow() + timedelta(days=14)
    backup = instance.backup(
        backup_id, database=database, expire_time=expire_time)
    operation = backup.create()

    # Wait for backup operation to complete.
    operation.result(1200)

    # Verify that the backup is ready.
    backup.reload()
    assert backup.is_ready() is True

    # Get the name, create time and backup size.
    backup.reload()
    print("Backup {} of size {} bytes was created at {}".format(
        backup.name, backup.size_bytes, backup.create_time))
# [END spanner_create_backup]


# [START spanner_restore_database]
def restore_database(instance_id, new_database_id, backup_id):
    """Restores a database from a backup."""
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    # Create a backup on database_id.

    # Start restoring backup to a new database.
    backup = instance.backup(backup_id)
    new_database = instance.database(new_database_id)
    operation = new_database.restore(backup)

    # Wait for restore operation to complete.
    operation.result(1200)

    # Newly created database has restore information.
    new_database.reload()
    restore_info = new_database.restore_info
    print("Database {} restored to {} from backup {}.".format(
        restore_info.backup_info.source_database,
        new_database_id,
        restore_info.backup_info.backup))
# [END spanner_restore_database]


# [START spanner_cancel_backup]
def cancel_backup(instance_id, database_id, backup_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    expire_time = datetime.utcnow() + timedelta(days=30)

    # Create a backup.
    backup = instance.backup(
        backup_id, database=database, expire_time=expire_time)
    operation = backup.create()

    # Cancel backup creation.
    operation.cancel()

    # Cancel operations are best effort so either it will complete or
    # be cancelled.
    while not operation.done():
        time.sleep(300)  # 5 mins

    # Deal with resource if the operation succeeded.
    if backup.exists():
        print("Backup was created before the cancel completed.")
        backup.delete()
        print("Backup deleted.")
    else:
        print("Backup creation was successfully cancelled.")
# [END spanner_cancel_backup]


# [START spanner_list_backup_operations]
def list_backup_operations(instance_id, database_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    # List the CreateBackup operations.
    filter_ = (
        "(metadata.database:{}) AND "
        "(metadata.@type:type.googleapis.com/"
        "google.spanner.admin.database.v1.CreateBackupMetadata)"
    ).format(database_id)
    operations = instance.list_backup_operations(filter_=filter_)
    for op in operations:
        metadata = op.metadata
        print("Backup {} on database {}: {}% complete.".format(
            metadata.name, metadata.database,
            metadata.progress.progress_percent))
# [END spanner_list_backup_operations]


# [START spanner_list_database_operations]
def list_database_operations(instance_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    # List the progress of restore.
    filter_ = (
        "(metadata.@type:type.googleapis.com/"
        "google.spanner.admin.database.v1.OptimizeRestoredDatabaseMetadata)"
    )
    operations = instance.list_database_operations(filter_=filter_)
    for op in operations:
        print("Database {} restored from backup is {}% optimized.".format(
            op.metadata.name, op.metadata.progress.progress_percent))
# [END spanner_list_database_operations]


# [START spanner_list_backups]
def list_backups(instance_id, database_id, backup_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    # List all backups.
    print("All backups:")
    for backup in instance.list_backups():
        print(backup.name)

    # List all backups that contain a name.
    print("All backups with backup name containing \"{}\":".format(backup_id))
    for backup in instance.list_backups(filter_="name:{}".format(backup_id)):
        print(backup.name)

    # List all backups for a database that contains a name.
    print("All backups with database name containing \"{}\":".format(database_id))
    for backup in instance.list_backups(filter_="database:{}".format(database_id)):
        print(backup.name)

    # List all backups that expire before a timestamp.
    expire_time = datetime.utcnow().replace(microsecond=0) + timedelta(days=30)
    print("All backups with expire_time before \"{}-{}-{}T{}:{}:{}Z\":".format(
        *expire_time.timetuple()))
    for backup in instance.list_backups(
            filter_="expire_time < \"{}-{}-{}T{}:{}:{}Z\"".format(
                *expire_time.timetuple())):
        print(backup.name)

    # List all backups with a size greater than some bytes.
    print("All backups with backup size more than 100 bytes:")
    for backup in instance.list_backups(filter_="size_bytes > 100"):
        print(backup.name)

    # List backups that were created after a timestamp that are also ready.
    create_time = datetime.utcnow().replace(microsecond=0) - timedelta(days=1)
    print("All backups created after \"{}-{}-{}T{}:{}:{}Z\" and are READY:".format(
        *create_time.timetuple()))
    for backup in instance.list_backups(
            filter_="create_time >= \"{}-{}-{}T{}:{}:{}Z\" AND state:READY".format(
                *create_time.timetuple())):
        print(backup.name)

    print("All backups with pagination")
    for page in instance.list_backups(page_size=2).pages:
        for backup in page:
            print(backup.name)
# [END spanner_list_backups]


# [START spanner_delete_backup]
def delete_backup(instance_id, backup_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    backup = instance.backup(backup_id)
    backup.reload()

    # Wait for databases that reference this backup to finish optimizing.
    while backup.referencing_databases:
        time.sleep(30)
        backup.reload()

    # Delete the backup.
    backup.delete()

    # Verify that the backup is deleted.
    assert backup.exists() is False
    print("Backup {} has been deleted.".format(backup.name))
# [END spanner_delete_backup]


# [START spanner_update_backup]
def update_backup(instance_id, backup_id):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    backup = instance.backup(backup_id)
    backup.reload()

    # Expire time must be within 366 days of the create time of the backup.
    old_expire_time = backup.expire_time
    new_expire_time = old_expire_time + timedelta(days=30)
    backup.update_expire_time(new_expire_time)
    print("Backup {} expire time was updated from {} to {}.".format(
        backup.name, old_expire_time, new_expire_time))
# [END spanner_update_backup]


if __name__ == '__main__':  # noqa: C901
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'instance_id', help='Your Cloud Spanner instance ID.')
    parser.add_argument(
        '--database-id', help='Your Cloud Spanner database ID.',
        default='example_db')
    parser.add_argument(
        '--backup-id', help='Your Cloud Spanner backup ID.',
        default='example_backup')

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('create_backup', help=create_backup.__doc__)
    subparsers.add_parser('cancel_backup', help=cancel_backup.__doc__)
    subparsers.add_parser('update_backup', help=update_backup.__doc__)
    subparsers.add_parser('restore_database', help=restore_database.__doc__)
    subparsers.add_parser('list_backups', help=list_backups.__doc__)
    subparsers.add_parser('list_backup_operations', help=list_backup_operations.__doc__)
    subparsers.add_parser('list_database_operations',
                          help=list_database_operations.__doc__)
    subparsers.add_parser('delete_backup', help=delete_backup.__doc__)

    args = parser.parse_args()

    if args.command == 'create_backup':
        create_backup(args.instance_id, args.database_id, args.backup_id)
    elif args.command == 'cancel_backup':
        cancel_backup(args.instance_id, args.database_id, args.backup_id)
    elif args.command == 'update_backup':
        update_backup(args.instance_id, args.backup_id)
    elif args.command == 'restore_database':
        restore_database(args.instance_id, args.database_id, args.backup_id)
    elif args.command == 'list_backups':
        list_backups(args.instance_id, args.database_id, args.backup_id)
    elif args.command == 'list_backup_operations':
        list_backup_operations(args.instance_id, args.database_id)
    elif args.command == 'list_database_operations':
        list_database_operations(args.instance_id)
    elif args.command == 'delete_backup':
        delete_backup(args.instance_id, args.backup_id)
    else:
        print("Command {} did not match expected commands.".format(args.command))
