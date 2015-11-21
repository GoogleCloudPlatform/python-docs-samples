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
Checks dependencies in requirements.txt to ensure they are the latest version.
"""

import argparse
import sys

from update_requirements import get_package_info, read_requirements


def check_req(req):
    info = get_package_info(req.project_name)
    newest_version = info['version']
    current_spec = req.specs[0] if req.specs else ('==', 'unspecified')
    if current_spec[1] != newest_version:
        return req, newest_version


def main(req_file):
    reqs = read_requirements(req_file)
    outdated_reqs = filter(None, [check_req(req) for req in reqs])

    if outdated_reqs:
        for req in outdated_reqs:
            print("{} is out of date, latest version is {}".format(*req))
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'requirements_file',
        help='Path the the requirements.txt file to check.')

    args = parser.parse_args()

    main(args.requirements_file)
