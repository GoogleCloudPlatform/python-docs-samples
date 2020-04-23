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

from google.cloud import spanner
import pytest
import random
import string

import backup_sample


def unique_instance_id():
    """ Creates a unique id for the database. """
    return 'test-instance-{}'.format(''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(5)))


def unique_database_id():
    """ Creates a unique id for the database. """
    return 'test-db-{}'.format(''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(5)))


def unique_backup_id():
    """ Creates a unique id for the backup. """
    return 'test-backup-{}'.format(''.join(random.choice(
        string.ascii_lowercase + string.digits) for _ in range(5)))


INSTANCE_ID = unique_instance_id()
DATABASE_ID = unique_database_id()
RESTORE_DB_ID = unique_database_id()
BACKUP_ID = unique_backup_id()


@pytest.fixture(scope='module')
def spanner_instance():
    spanner_client = spanner.Client()
    instance_config = '{}/instanceConfigs/{}'.format(
        spanner_client.project_name, 'regional-us-central1')
    instance = spanner_client.instance(INSTANCE_ID, instance_config)
    op = instance.create()
    op.result(120)  # block until completion
    yield instance
    instance.delete()


@pytest.fixture(scope='module')
def database(spanner_instance):
    """ Creates a temporary database that is removed after testing. """
    db = spanner_instance.database(DATABASE_ID)
    db.create()
    yield db
    db.drop()


def test_create_backup(capsys, database):
    backup_sample.create_backup(INSTANCE_ID, DATABASE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


def test_restore_database(capsys):
    backup_sample.restore_database(INSTANCE_ID, RESTORE_DB_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert (DATABASE_ID + " restored to ") in out
    assert (RESTORE_DB_ID + " from backup ") in out
    assert BACKUP_ID in out


def test_list_backup_operations(capsys, spanner_instance):
    backup_sample.list_backup_operations(INSTANCE_ID, DATABASE_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out
    assert DATABASE_ID in out


def test_list_backups(capsys, spanner_instance):
    backup_sample.list_backups(INSTANCE_ID, DATABASE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    id_count = out.count(BACKUP_ID)
    assert id_count == 7


def test_update_backup(capsys):
    backup_sample.update_backup(INSTANCE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


def test_delete_backup(capsys, spanner_instance):
    backup_sample.delete_backup(INSTANCE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    assert BACKUP_ID in out


def test_cancel_backup(capsys):
    backup_sample.cancel_backup(INSTANCE_ID, DATABASE_ID, BACKUP_ID)
    out, _ = capsys.readouterr()
    cancel_success = "Backup creation was successfully cancelled." in out
    cancel_failure = (
        ("Backup was created before the cancel completed." in out) and
        ("Backup deleted." in out)
    )
    assert cancel_success or cancel_failure
