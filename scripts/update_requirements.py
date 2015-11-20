#!/usr/bin/env python

# Copyright (C) 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Updates dependencies in requirements.txt to the latest version.
"""

import argparse

from pip.req.req_file import parse_requirements
from pkg_resources import Requirement
import requests


def get_package_info(package):
    url = 'https://pypi.python.org/pypi/{}/json'.format(package)
    r = requests.get(url)
    r.raise_for_status()
    return r.json()['info']


def read_requirements(req_file):
    return [x.req for x in parse_requirements(req_file, session={})]


def update_req(req):
    info = get_package_info(req.project_name)
    newest_version = info['version']
    current_spec = req.specs[0] if req.specs else ('==', 'unspecified')
    new_spec = ('==', newest_version)
    if current_spec != new_spec:
        newreq = Requirement(req.unsafe_name, [new_spec], req.extras)
        print('Updated {} from {} -> {}'.format(
            req.project_name,
            current_spec[1],
            newest_version))
        return newreq
    return req


def write_requirements(reqs, req_file):
    with open(req_file, 'w') as f:
        for req in reqs:
            f.write('{}\n'.format(req))


def main(req_file):
    reqs = read_requirements(req_file)
    reqs = [update_req(req) for req in reqs]
    write_requirements(reqs, req_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'requirements_file',
        help='Path the the requirements.txt file to update.')

    args = parser.parse_args()

    main(args.requirements_file)
