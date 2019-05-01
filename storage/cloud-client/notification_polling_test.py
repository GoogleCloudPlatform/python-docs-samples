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


from google.cloud.pubsub_v1.subscriber.message import Message
import mock

from notification_polling import summarize


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
    data = (b'{'
            b'  "size": 12345,'
            b'  "contentType": "text/html",'
            b'  "metageneration": 1'
            b'}')
    message = Message(
        mock.Mock(data=data, attributes=attributes),
        MESSAGE_ID,
        mock.Mock())
    assert summarize(message) == (
        '\tEvent type: OBJECT_FINALIZE\n'
        '\tBucket ID: mybucket\n'
        '\tObject ID: myobject\n'
        '\tGeneration: 1234567\n'
        '\tContent type: text/html\n'
        '\tSize: 12345\n'
        '\tMetageneration: 1\n')
