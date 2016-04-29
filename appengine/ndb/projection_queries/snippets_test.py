# Copyright 2016 Google Inc. All rights reserved.
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

import snippets


def test_print_author_tags(testbed, capsys):
    snippets.Article(title="one", author="Two", tags=["three"]).put()

    snippets.print_author_tags()

    stdout, _ = capsys.readouterr()
    assert 'Two' in stdout
    assert 'three' in stdout
    assert 'one' not in stdout


def test_fetch_sub_properties(testbed):
    address = snippets.Address(type="home", street="college", city="staten")
    address.put()
    address2 = snippets.Address(type="home", street="brighton", city="staten")
    address2.put()
    snippets.Contact(name="one", addresses=[address, address2]).put()

    snippets.fetch_sub_properties()


def test_demonstrate_ndb_grouping(testbed):
    snippets.Article(title="one", author="Two", tags=["three"]).put()

    snippets.demonstrate_ndb_grouping()


def test_declare_multiple_valued_property(testbed):
    snippets.declare_multiple_valued_property()
