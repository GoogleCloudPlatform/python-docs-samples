# Copyright 2018, Google, LLC.
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

# [START functions_slack_setup]
import hashlib
import hmac
import os

import googleapiclient.discovery
from flask import jsonify


kgsearch = googleapiclient.discovery.build(
    'kgsearch',
    'v1',
    developerKey=os.environ['KG_API_KEY'],
    cache_discovery=False)
# [END functions_slack_setup]


# [START functions_verify_webhook]
# Python 3+ version of https://github.com/slackapi/python-slack-events-api/blob/master/slackeventsapi/server.py
def verify_signature(request):
    timestamp = request.headers.get('X-Slack-Request-Timestamp', '')
    signature = request.headers.get('X-Slack-Signature', '')

    req = str.encode('v0:{}:'.format(timestamp)) + request.get_data()
    request_digest = hmac.new(
        str.encode(os.environ['SLACK_SECRET']),
        req, hashlib.sha256
    ).hexdigest()
    request_hash = 'v0={}'.format(request_digest)

    if not hmac.compare_digest(request_hash, signature):
        raise ValueError('Invalid request/credentials.')
# [END functions_verify_webhook]


# [START functions_slack_format]
def format_slack_message(query, response):
    entity = None
    if response and response.get('itemListElement') is not None and \
       len(response['itemListElement']) > 0:
        entity = response['itemListElement'][0]['result']

    message = {
        'response_type': 'in_channel',
        'text': 'Query: {}'.format(query),
        'attachments': []
    }

    attachment = {}
    if entity:
        name = entity.get('name', '')
        description = entity.get('description', '')
        detailed_desc = entity.get('detailedDescription', {})
        url = detailed_desc.get('url')
        article = detailed_desc.get('articleBody')
        image_url = entity.get('image', {}).get('contentUrl')

        attachment['color'] = '#3367d6'
        if name and description:
            attachment['title'] = '{}: {}'.format(entity["name"],
                                                  entity["description"])
        elif name:
            attachment['title'] = name
        if url:
            attachment['title_link'] = url
        if article:
            attachment['text'] = article
        if image_url:
            attachment['image_url'] = image_url
    else:
        attachment['text'] = 'No results match your query.'
    message['attachments'].append(attachment)

    return message
# [END functions_slack_format]


# [START functions_slack_request]
def make_search_request(query):
    req = kgsearch.entities().search(query=query, limit=1)
    res = req.execute()
    return format_slack_message(query, res)
# [END functions_slack_request]


# [START functions_slack_search]
def kg_search(request):
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    verify_signature(request)
    kg_search_response = make_search_request(request.form['text'])
    return jsonify(kg_search_response)
# [END functions_slack_search]
