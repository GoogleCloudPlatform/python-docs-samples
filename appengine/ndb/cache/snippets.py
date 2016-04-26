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


def set_in_process_cache_policy(func):
    context = ndb.get_context()
    context.set_cache_policy(func)


def set_memcache_policy(func):
    context = ndb.get_context()
    context.set_memcache_policy(func)


def bypass_in_process_cache_for_account_entities():
    context = ndb.get_context()
    context.set_cache_policy(lambda key: key.kind() != 'Account')


def set_datastore_policy(func):
    context = ndb.get_context()
    context.set_datastore_policy(func)


def set_memcache_timeout_policy(func):
    context = ndb.get_context()
    context.set_memcache_timeout_policy(func)


def clear_cache():
    context = ndb.get_context()
    context.clear_cache()
