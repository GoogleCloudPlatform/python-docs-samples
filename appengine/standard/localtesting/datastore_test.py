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

# [START imports]
import unittest

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
# [END imports]


# [START datastore_example_1]
class TestModel(ndb.Model):
    """A model class used for testing."""
    number = ndb.IntegerProperty(default=42)
    text = ndb.StringProperty()


class TestEntityGroupRoot(ndb.Model):
    """Entity group root"""
    pass


def GetEntityViaMemcache(entity_key):
    """Get entity from memcache if available, from datastore if not."""
    entity = memcache.get(entity_key)
    if entity is not None:
        return entity
    key = ndb.Key(urlsafe=entity_key)
    entity = key.get()
    if entity is not None:
        memcache.set(entity_key, entity)
    return entity
# [END datastore_example_1]


# [START datastore_example_test]
class DatastoreTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

# [END datastore_example_test]

    # [START datastore_example_teardown]
    def tearDown(self):
        self.testbed.deactivate()
    # [END datastore_example_teardown]

    # [START datastore_example_insert]
    def testInsertEntity(self):
        TestModel().put()
        self.assertEqual(1, len(TestModel.query().fetch(2)))
    # [END datastore_example_insert]

    # [START datastore_example_filter]
    def testFilterByNumber(self):
        root = TestEntityGroupRoot(id="root")
        TestModel(parent=root.key).put()
        TestModel(number=17, parent=root.key).put()
        query = TestModel.query(ancestor=root.key).filter(
            TestModel.number == 42)
        results = query.fetch(2)
        self.assertEqual(1, len(results))
        self.assertEqual(42, results[0].number)
    # [END datastore_example_filter]

    # [START datastore_example_memcache]
    def testGetEntityViaMemcache(self):
        entity_key = TestModel(number=18).put().urlsafe()
        retrieved_entity = GetEntityViaMemcache(entity_key)
        self.assertNotEqual(None, retrieved_entity)
        self.assertEqual(18, retrieved_entity.number)
    # [END datastore_example_memcache]


# [START HRD_example_1]
from google.appengine.datastore import datastore_stub_util  # noqa


class HighReplicationTestCaseOne(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Create a consistency policy that will simulate the High Replication
        # consistency model.
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(
            probability=0)
        # Initialize the datastore stub with this policy.
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)
        # Initialize memcache stub too, since ndb also uses memcache
        self.testbed.init_memcache_stub()
        # Clear in-context cache before each test.
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def testEventuallyConsistentGlobalQueryResult(self):
        class TestModel(ndb.Model):
            pass

        user_key = ndb.Key('User', 'ryan')

        # Put two entities
        ndb.put_multi([
            TestModel(parent=user_key),
            TestModel(parent=user_key)
        ])

        # Global query doesn't see the data.
        self.assertEqual(0, TestModel.query().count(3))
        # Ancestor query does see the data.
        self.assertEqual(2, TestModel.query(ancestor=user_key).count(3))
# [END HRD_example_1]

    # [START HRD_example_2]
    def testDeterministicOutcome(self):
        # 50% chance to apply.
        self.policy.SetProbability(.5)
        # Use the pseudo random sequence derived from seed=2.
        self.policy.SetSeed(2)

        class TestModel(ndb.Model):
            pass

        TestModel().put()

        self.assertEqual(0, TestModel.query().count(3))
        self.assertEqual(0, TestModel.query().count(3))
        # Will always be applied before the third query.
        self.assertEqual(1, TestModel.query().count(3))
    # [END HRD_example_2]


# [START main]
if __name__ == '__main__':
    unittest.main()
# [END main]
