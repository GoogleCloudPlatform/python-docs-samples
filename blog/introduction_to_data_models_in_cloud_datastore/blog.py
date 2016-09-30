# Copyright 2015, Google, Inc.
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
    path_parts = path.strip(u'/').split(u'/')
    for n, x in enumerate(path_parts):
        name, ext = x.rsplit('.', 1)
        key_parts.extend([ext, name])

    return datastore.key(*key_parts)


def create_user(ds, username, profile):
    key = path_to_key(ds, '{0}.user'.format(username))
    entity = datastore.Entity(key)
    entity.update(profile)
    ds.put(entity)


def create_post(ds, username, post_content):
    now = datetime.datetime.utcnow()
    key = path_to_key(ds, '{0}.user/{1}.post'.format(username, now))
    entity = datastore.Entity(key)

    entity.update({
        'created': now,
        'created_by': username,
        'content': post_content
    })

    ds.put(entity)


def repost(ds, username, original):
    now = datetime.datetime.utcnow()
    new_key = path_to_key(ds, '{0}.user/{1}.post'.format(username, now))
    new = datastore.Entity(new_key)

    new.update(original)

    ds.put(new)


def list_posts_by_user(ds, username):
    user_key = path_to_key(ds, '{0}.user'.format(username))
    return ds.query(kind='post', ancestor=user_key).fetch()


def list_all_posts(ds):
    return ds.query(kind='post').fetch()


def main(project_id):
    ds = datastore.Client(project_id)

    print("Creating users...")
    create_user(ds, 'tonystark',
                {'name': 'Tony Stark', 'location': 'Stark Island'})
    create_user(ds, 'peterparker',
                {'name': 'Peter Parker', 'location': 'New York City'})

    print("Creating posts...")
    for n in range(1, 10):
        create_post(ds, 'tonystark', "Tony's post #{0}".format(n))
        create_post(ds, 'peterparker', "Peter's post #{0}".format(n))

    print("Re-posting tony's post as peter...")

    tonysposts = list_posts_by_user(ds, 'tonystark')
    for post in tonysposts:
        original_post = post
        break

    repost(ds, 'peterparker', original_post)

    print('Posts by tonystark:')
    for post in list_posts_by_user(ds, 'tonystark'):
        print("> {0} on {1}".format(post['content'], post['created']))

    print('Posts by peterparker:')
    for post in list_posts_by_user(ds, 'peterparker'):
        print("> {0} on {1}".format(post['content'], post['created']))

    print('Posts by everyone:')
    for post in list_all_posts(ds):
        print("> {0} on {1}".format(post['content'], post['created']))

    print('Cleaning up...')
    ds.delete_multi([
        path_to_key(ds, 'tonystark.user'),
        path_to_key(ds, 'peterparker.user')
    ])
    ds.delete_multi([
        x.key for x in list_all_posts(ds)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Demonstrates wiki data model.')
    parser.add_argument('project_id', help='Your cloud project ID.')

    args = parser.parse_args()

    main(args.project_id)
