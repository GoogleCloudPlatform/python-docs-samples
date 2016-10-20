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
import datetime
import random
import uuid

from six.moves.urllib import parse
import sqlalchemy
from sqlalchemy.ext import declarative
import sqlalchemy.orm


SECONDS_IN_DAY = 24 * 60 * 60
SECONDS_IN_2016 = 366 * SECONDS_IN_DAY

# Unix timestamp for the beginning of 2016.
# http://stackoverflow.com/a/19801806/101923
TIMESTAMP_2016 = (
    datetime.datetime(2016, 1, 1, 0, 0, 0) -
    datetime.datetime.fromtimestamp(0)).total_seconds()


Base = declarative.declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    date_joined = sqlalchemy.Column(sqlalchemy.DateTime)


class UserSession(Base):
    __tablename__ = 'UserSessions'

    id = sqlalchemy.Column(sqlalchemy.String(length=36), primary_key=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('Users.id'))
    login_time = sqlalchemy.Column(sqlalchemy.DateTime)
    logout_time = sqlalchemy.Column(sqlalchemy.DateTime)
    ip_address = sqlalchemy.Column(sqlalchemy.String(length=40))


def generate_users(session, num_users):
    users = []

    for userid in range(1, num_users + 1):
        year_portion = random.random()
        date_joined = datetime.datetime.fromtimestamp(
            TIMESTAMP_2016 + SECONDS_IN_2016 * year_portion)
        user = User(id=userid, date_joined=date_joined)
        users.append(user)
        session.add(user)

    session.commit()
    return users


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


def simulate_user_session(session, user, previous_user_session=None):
    """Simulates a single session (login to logout) of a user's history."""
    login_time = user.date_joined

    if previous_user_session is not None:
        login_time = (
            previous_user_session.logout_time +
            datetime.timedelta(
                days=1, seconds=random.randrange(SECONDS_IN_DAY)))

    session_id = str(uuid.uuid4())
    user_session = UserSession(
        id=session_id,
        user_id=user.id,
        login_time=login_time,
        ip_address=random_ip())
    user_session.logout_time = (
        login_time +
        datetime.timedelta(seconds=(1 + random.randrange(59))))
    session.commit()
    session.add(user_session)
    return user_session


def simulate_user_history(session, user):
    """Simulates the entire history of activity for a single user."""
    total_sessions = random.randrange(10)
    previous_user_session = None

    for _ in range(total_sessions):
        user_session = simulate_user_session(
            session, user, previous_user_session)
        previous_user_session = user_session


def run_simulation(session, users):
    """Simulates app activity for all users."""

    for n, user in enumerate(users):
        if n % 100 == 0 and n != 0:
            print('Simulated data for {} users'.format(n))

        simulate_user_history(session, user)

    print('COMPLETE: Simulated data for {} users'.format(len(users)))


def populate_db(session, total_users=3):
    """Populate database with total_users simulated users and their actions."""
    users = generate_users(session, total_users)
    run_simulation(session, users)


def create_session(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    return Session()


def main(total_users, host, user, password, db_name):
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://{user}:{password}@{host}/{db_name}'.format(
            user=user,
            password=parse.quote_plus(password),
            host=host,
            db_name=db_name))
    session = create_session(engine)

    try:
        populate_db(session, total_users)
    finally:
        session.close()


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
