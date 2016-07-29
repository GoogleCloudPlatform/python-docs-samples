#!/usr/bin/python
# Copyright 2015 Google Inc
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# [START runner]
import optparse
import os
import sys
import unittest


USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to Google Cloud or Google App Engine SDK installation, usually
            ~/google_cloud_sdk
TEST_PATH   Path to package containing test modules"""


def append_or_insert_path(path):
    """Adds GAE path to system path, or appends it to the google path
    if that already exists.

    Not all Google packages are inside namespaced packages, which means
    there might be another named `google` on the path, and simply appending
    the App Engine SDK to the path will not work since the other package
    will get discovered and used first. This ugly hack emulates namespace
    packages by first searching if a `google` package already exists by
    importing it, and if so appending to its path, otherwise it just
    inserts it into the import path by itself.
    """
    try:
        import google
        google.__path__.append("{0}/google".format(path))
    except ImportError:
        sys.path.insert(0, path)


def main(sdk_path, test_path):
    # If the sdk path points to a google cloud sdk installation
    # then we should alter it to point to the GAE platform location.

    if os.path.exists(os.path.join(sdk_path, 'platform/google_appengine')):
        append_or_insert_path(
            os.path.join(sdk_path, 'platform/google_appengine'))
    else:
        append_or_insert_path(sdk_path)

    # Ensure that the google.appengine.* packages are available
    # in tests as well as all bundled third-party packages.
    import dev_appserver
    dev_appserver.fix_sys_path()

    # Loading appengine_config from the current project ensures that any
    # changes to configuration there are available to all tests (e.g.
    # sys.path modifications, namespaces, etc.)
    try:
        import appengine_config
        (appengine_config)
    except ImportError:
        print "Note: unable to import appengine_config."

    # Discover and run tests.
    suite = unittest.loader.TestLoader().discover(test_path, "*_test.py")
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 2:
        print 'Error: Exactly 2 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    main(SDK_PATH, TEST_PATH)

# [END runner]
