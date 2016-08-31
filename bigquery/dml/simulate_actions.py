#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
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

"""Command-line tool to simulate user actions and write to SQL database.
"""

from __future__ import division

import argparse
import collections
import datetime
import random
import uuid

import pymysql


SECONDS_IN_DAY = 24 * 60 * 60
SECONDS_IN_2016 = 366 * SECONDS_IN_DAY

# Unix timestamp for the beginning of 2016.
# http://stackoverflow.com/a/19801806/101923
TIMESTAMP_2016 = (
    datetime.datetime(2016, 1, 1, 0, 0, 0) -
    datetime.datetime.fromtimestamp(0)).total_seconds()


User = collections.namedtuple('User', ['id', 'date_joined'])

UserSession = collections.namedtuple(
        'UserSession',
        ['id', 'login', 'logout', 'user_id', 'ip_address'])

UserAction = collections.namedtuple(
        'UserAction',
        ['session_id', 'user_id', 'type', 'time', 'message'])


def generate_users(num_users):
    users = []

    for userid in range(num_users):
        # Add more users at the end of 2016 than the beginning.
        # https://en.wikipedia.org/wiki/Beta_distribution
        year_portion = random.betavariate(3, 1)
        date_joined = datetime.datetime.fromtimestamp(
            TIMESTAMP_2016 + SECONDS_IN_2016 * year_portion)
        users.append(User(userid, date_joined))

    return users


def insert_users(connection, users):
    """Inserts rows into the Users table."""

    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM `UserActions`')
        cursor.execute('DELETE FROM `UserSessions`')
        cursor.execute('DELETE FROM `Users`')

    connection.commit()

    with connection.cursor() as cursor:
        cursor.executemany(
            'INSERT INTO `Users` (`UserID`, `DateJoined`) VALUES (%s,%s)',
            [(user.id, user.date_joined.isoformat(' ')) for user in users])

    connection.commit()


def random_ip():
    """Choose a random example IP address.

    Examples are chosen from the test networks described in
    https://tools.ietf.org/html/rfc5737
    """
    network = random.choice([
        '192.0.2',  # RFC-5737 TEST-NET-1
        '198.51.100',  # RFC-5737 TEST-NET-2
        '203.0.113',  # RFC-5737 TEST-NET-3
    ])
    ip_address = '{}.{}'.format(network, random.randrange(256))
    return ip_address


def simulate_user_session(connection, user, previous_session=None):
    """Simulates a single session (login to logout) of a user's history."""
    login_time = user.date_joined

    if previous_session is not None:
        login_time = (
            previous_session.logout +
            datetime.timedelta(
                days=1, seconds=random.randrange(SECONDS_IN_DAY)))

    session_id = str(uuid.uuid4())
    previous_action_time = login_time
    total_actions = random.randrange(10) + 1
    actions = []

    for _ in range(total_actions):
        action_type=random.choice(['CLICKED', 'PURCHASED'])
        action_time=(previous_action_time +
            datetime.timedelta(seconds=random.randrange(59) + 1))
        message='breed={}'.format(
            random.choice([
                'Albera',
                'Angus',
                'Beefalo',
                'Droughtmaster',
                'Longhorn',
                'Guernsey',
                'Highland',
                'Holstein',
                'Jersey',
                'Normande',
                'Shetland',
                'Wagyu',
            ]))
        action = UserAction(
            session_id=session_id,
            user_id=user.id,
            type=action_type,
            time=action_time,
            message=message)

        previous_action_time = action_time
        actions.append(action)

    logout_time = (
        previous_action_time +
        datetime.timedelta(seconds=(1 + random.randrange(59))))

    return (
        UserSession(
            session_id,
            login_time,
            logout_time,
            user.id,
            random_ip()),
        actions)


def simulate_user_history(connection, user):
    """Simulates the entire history of activity for a single user."""
    total_sessions = random.randrange(10)
    sessions = []
    actions = []
    previous_session = None

    for _ in range(total_sessions):
        session, user_actions = simulate_user_session(
                connection, user, previous_session)
        sessions.append(session)
        actions.extend(user_actions)
        previous_session = session

    with connection.cursor() as cursor:
        cursor.executemany(
            'INSERT INTO `UserSessions` '
            '(`SessionID`, '
            '`LoginTime`, '
            '`LogoutTime`, '
            '`UserID`, '
            '`IPAddress`) '
            'VALUES (%s,%s,%s,%s,%s)',
            [(
                session.id,
                session.login.isoformat(' '),
                session.logout.isoformat(' '),
                session.user_id,
                session.ip_address,
            ) for session in sessions])
        cursor.executemany(
            'INSERT INTO `UserActions` '
            '(`SessionID`, '
            '`UserID`, '
            '`ActionType`, '
            '`ActionTime`, '
            '`Message`) '
            'VALUES (%s,%s,%s,%s,%s)',
            [(
                action.session_id,
                action.user_id,
                action.type,
                action.time.isoformat(' '),
                action.message,
            ) for action in actions])

    connection.commit()


def run_simulation(connection, users):
    """Simulates app activity for all users."""

    for n, user in enumerate(users):

        if n % 100 == 0 and n != 0:
            print('Simulated data for {} users'.format(n))

        simulate_user_history(connection, user)

    print('COMPLETE: Simulated data for {} users'.format(len(users)))


def main(total_users, host, user, password, db_name):
    connection = pymysql.connect(
        host=host, user=user, password=password, db=db_name)

    try:
        users = generate_users(total_users)
        insert_users(connection, users)
        run_simulation(connection, users)
    finally:
        connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'total_users', help='How many simulated users to create.', type=int)
    parser.add_argument('host', help='Host of the database to write to.')
    parser.add_argument('user', help='User to connect to the database.')
    parser.add_argument('password', help='Password for the database user.')
    parser.add_argument('db', help='Name of the database to write to.')

    args = parser.parse_args()

    main(args.total_users, args.host, args.user, args.password, args.db)
