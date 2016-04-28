# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.appengine.api import mail

import handle_incoming_email


def test_handle_bounced_email(testbed):
    handler = handle_incoming_email.LogSenderHandler()
    handler.request = 'request'
    message = mail.EmailMessage(
        sender='support@example.com',
        subject='Your account has been approved')
    message.to = 'Albert Johnson <Albert.Johnson@example.com>'
    message.body = 'Dear Albert.'
    handler.receive(message)
