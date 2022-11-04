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

from google.appengine.ext import ndb

import snippets


def test_set_in_process_cache_policy(testbed):
    def policy(key):
        return 1 == 1

    snippets.set_in_process_cache_policy(policy)
    assert policy == ndb.get_context().get_cache_policy()


def test_set_memcache_policy(testbed):
    def policy(key):
        return 1 == 2

    snippets.set_memcache_policy(policy)
    assert policy == ndb.get_context().get_memcache_policy()


def test_bypass_in_process_cache_for_account_entities(testbed):
    context = ndb.get_context()
    assert context.get_cache_policy() == context.default_cache_policy
    snippets.bypass_in_process_cache_for_account_entities()
    assert context.get_cache_policy() != context.default_cache_policy


def test_set_datastore_policy(testbed):
    def policy(key):
        return key is None

    snippets.set_datastore_policy(policy)
    assert ndb.get_context().get_datastore_policy() == policy


def test_set_memcache_timeout_policy(testbed):
    def policy(key):
        return 1

    snippets.set_memcache_timeout_policy(policy)
    assert ndb.get_context().get_memcache_timeout_policy() == policy


def test_clear_cache(testbed):
    snippets.clear_cache()
