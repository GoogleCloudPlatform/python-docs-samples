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

# [START env_example]
import os
import unittest

from google.appengine.ext import testbed


class EnvVarsTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(
            app_id='your-app-id',
            my_config_setting='example',
            overwrite=True)

    def tearDown(self):
        self.testbed.deactivate()

    def testEnvVars(self):
        self.assertEqual(os.environ['APPLICATION_ID'], 'your-app-id')
        self.assertEqual(os.environ['MY_CONFIG_SETTING'], 'example')
# [END env_example]


if __name__ == '__main__':
    unittest.main()
