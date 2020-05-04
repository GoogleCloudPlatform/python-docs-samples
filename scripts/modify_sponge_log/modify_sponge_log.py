#!/usr/bin/env python
#
# Copyright 2020 Google, LLC
#
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

# This sample creates a secure two-service application running on Cloud Run.
# This test builds and deploys the two secure services
# to test that they interact properly together.

import sys
from xml.etree import ElementTree


"""Inject region tags into the test names in sponge_log.xml.

It will parse an xml file named `sponge_log.xml` and extracts
`region_tags` properties and inject the region tags into the test names, then overwrite the original file.

The only command line argument is the filename for the xml file.
"""


def extract_region_tags(t):
    ret = []
    props = t.findall('.//property[@name="region_tags"]')
    for prop in props:
        ret += [x.strip() for x in prop.attrib['value'].split(',')]
    return ret


def inject_region_tags(t):
    region_tags = extract_region_tags(t)
    if not region_tags:
        # region tags not found, just return
        return
    # `_plus_` is a separator between region tags. Double underscore
    # is the terminator.
    # This reminds me of Perl CGIs before the dotcom bubble.
    region_tags_string = '_plus_'.join(region_tags) + '__'
    if t.attrib['name'].startswith('test_'):
        t.attrib['name'] = t.attrib['name'].replace(
            'test_', 'test_{}'.format(region_tags_string), 1)
    else:
        t.attrib['name'] = 'test_{}{}'.format(
            region_tags_string, t.attrib['name'])


def main(filename='sponge_log.xml'):
    tree = ElementTree.parse(filename)
    root = tree.getroot()

    for testcase in root.findall('.//testcase'):
        inject_region_tags(testcase)

    tree.write(filename, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main()
