# Copyright 2017 Google Inc. All rights reserved.
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


from google.cloud.pubsub.message import Message

from notification_polling import GcsEvent


MESSAGE_ID = 12345


def test_parse_json_message():
    attributes = {
        'eventType': 'OBJECT_FINALIZE',
        'bucketId': 'mybucket',
        'objectId': 'myobject',
        'objectGeneration': 1234567,
        'resource': 'projects/_/buckets/mybucket/objects/myobject#1234567',
        'notificationConfig': ('projects/_/buckets/mybucket/'
                               'notificationConfigs/5'),
        'payloadFormat': 'JSON_API_V1'}
    data = ('{'
            '  "size": 12345,'
            '  "contentType": "text/html",'
            '  "metageneration": 1'
            '}')
    message = Message(data, MESSAGE_ID, attributes=attributes)
    event = GcsEvent(message)
    assert unicode(event) == (u'Object created - mybucket/myobject\n'
                              '\tGeneration: 1234567\n'
                              '\tContent type: text/html\n'
                              '\tSize: 12345\n')
    assert event.Summary() == 'Object created - mybucket/myobject'


def test_parse_no_payload_message():
    attributes = {
        'eventType': 'OBJECT_FINALIZE',
        'bucketId': 'mybucket',
        'objectId': 'myobject',
        'objectGeneration': 1234567,
        'resource': 'projects/_/buckets/mybucket/objects/myobject#1234567',
        'notificationConfig': ('projects/_/buckets/mybucket/'
                               'notificationConfigs/5'),
        'payloadFormat': 'NONE'}
    data = None
    message = Message(data, MESSAGE_ID, attributes=attributes)
    event = GcsEvent(message)
    assert unicode(event) == (u'Object created - mybucket/myobject\n'
                              '\tGeneration: 1234567\n')
    assert event.Summary() == 'Object created - mybucket/myobject'
