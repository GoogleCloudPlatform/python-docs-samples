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

import argparse
import subprocess
import sys

import pytest # flake8: noqa
import _pytest.main


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--junit', action='store_true', help='Output junit test report.')
    parser.add_argument('--run-slow', action='store_true', help='Run slow tests.')
    parser.add_argument(
        'directories', nargs='+', help='Directories to run py.test on.')
    args = parser.parse_args()

    extra_args = []

    if not args.run_slow:
        extra_args.append('-m not slow and not flaky')
        extra_args.append('--no-flaky-report')

    for directory in args.directories:
        per_directory_args = []

        if args.junit:
            per_directory_args.append(
                '--junitxml={}/junit.xml'.format(directory))

        # We could use pytest.main, however, we need import isolatation between
        # test runs. Without using subprocess, any test files that are named
        # the same will cause pytest to fail. Rather than do sys.module magic
        # between runs, it's cleaner to just do a subprocess.
        code = subprocess.call(
            ['py.test'] + extra_args + per_directory_args + [directory])

        if code not in (
                _pytest.main.EXIT_OK, _pytest.main.EXIT_NOTESTSCOLLECTED):
            sys.exit(code)

if __name__ == '__main__':
    main()
