# Copyright 2015 Google, LLC.
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

import argparse
import datetime

from google.cloud import datastore


def path_to_key(datastore, path):
    """
    Translates a file system path to a datastore key. The basename becomes the
    key name and the extension becomes the kind.

    Examples:
        /file.ext -> key(ext, file)
        /parent.ext/file.ext -> key(ext, parent, ext, file)
    """
    key_parts = []
    path_parts = path.strip('/').split('/')
    for n, x in enumerate(path_parts):
        name, ext = x.rsplit('.', 1)
        key_parts.extend([ext, name])

    return datastore.key(*key_parts)


def save_page(ds, page, content):
    with ds.transaction():
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        current_key = path_to_key(ds, f'{page}.page/current.revision')
        revision_key = path_to_key(ds, f'{page}.page/{now}.revision')

        if ds.get(revision_key):
            raise AssertionError("Revision %s already exists" % revision_key)

        current = ds.get(current_key)

        if current:
            revision = datastore.Entity(key=revision_key)
            revision.update(current)
            ds.put(revision)
        else:
            current = datastore.Entity(key=current_key)

        current['content'] = content

        ds.put(current)


def restore_revision(ds, page, revision):
    save_page(ds, page, revision['content'])


def list_pages(ds):
    return ds.query(kind='page').fetch()


def list_revisions(ds, page):
    page_key = path_to_key(ds, f'{page}.page')
    return ds.query(kind='revision', ancestor=page_key).fetch()


def main(project_id):
    ds = datastore.Client(project_id)

    save_page(ds, 'page1', '1')
    save_page(ds, 'page1', '2')
    save_page(ds, 'page1', '3')

    print('Revisions for page1:')
    first_revision = None
    for revision in list_revisions(ds, 'page1'):
        if not first_revision:
            first_revision = revision
        print("{}: {}".format(revision.key.name, revision['content']))

    print(f'restoring revision {first_revision.key.name}:')
    restore_revision(ds, 'page1', first_revision)

    print('Revisions for page1:')
    for revision in list_revisions(ds, 'page1'):
        print("{}: {}".format(revision.key.name, revision['content']))

    print('Cleaning up')
    ds.delete_multi([path_to_key(ds, 'page1.page')])
    ds.delete_multi([x.key for x in list_revisions(ds, 'page1')])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Demonstrates wiki data model.')
    parser.add_argument('project_id', help='Your cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)
