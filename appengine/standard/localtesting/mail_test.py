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

# [START mail_example]
import unittest

from google.appengine.api import mail
from google.appengine.ext import testbed


class MailTestCase(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        self.testbed.deactivate()

    def testMailSent(self):
        mail.send_mail(to='alice@example.com',
                       subject='This is a test',
                       sender='bob@example.com',
                       body='This is a test e-mail')
        messages = self.mail_stub.get_sent_messages(to='alice@example.com')
        self.assertEqual(1, len(messages))
        self.assertEqual('alice@example.com', messages[0].to)
# [END mail_example]


if __name__ == '__main__':
    unittest.main()
