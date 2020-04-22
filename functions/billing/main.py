# Copyright 2018 Google LLC
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

# [START functions_billing_limit]
# [START functions_billing_limit_appengine]
# [START functions_billing_stop]
import base64
import json
import os
# [END functions_billing_stop]
# [END functions_billing_limit]
# [END functions_billing_limit_appengine]

# [START functions_billing_limit]
# [START functions_billing_limit_appengine]
# [START functions_billing_stop]
from googleapiclient import discovery
# [END functions_billing_stop]
# [END functions_billing_limit]
# [END functions_billing_limit_appengine]

# [START functions_billing_slack]
import slack
# [END functions_billing_slack]

# [START functions_billing_limit]
# [START functions_billing_stop]
PROJECT_ID = os.getenv('GCP_PROJECT')
PROJECT_NAME = f'projects/{PROJECT_ID}'
# [END functions_billing_stop]
# [END functions_billing_limit]

# [START functions_billing_slack]

# See https://api.slack.com/docs/token-types#bot for more info
BOT_ACCESS_TOKEN = 'xxxx-111111111111-abcdefghidklmnopq'

CHANNEL_ID = 'C0XXXXXX'

slack_client = slack.WebClient(token=BOT_ACCESS_TOKEN)


def notify_slack(data, context):
    pubsub_message = data

    notification_attrs = json.dumps(pubsub_message['attributes'])
    notification_data = base64.b64decode(data['data']).decode('utf-8')
    budget_notification_text = f'{notification_attrs}, {notification_data}'

    slack_client.api_call(
      'chat.postMessage',
      channel=CHANNEL_ID,
      text=budget_notification_text)
# [END functions_billing_slack]


# [START functions_billing_stop]
def stop_billing(data, context):
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    pubsub_json = json.loads(pubsub_data)
    cost_amount = pubsub_json['costAmount']
    budget_amount = pubsub_json['budgetAmount']
    if cost_amount <= budget_amount:
        print(f'No action necessary. (Current cost: {cost_amount})')
        return

    billing = discovery.build(
        'cloudbilling',
        'v1',
        cache_discovery=False,
    )

    projects = billing.projects()

    if __is_billing_enabled(PROJECT_NAME, projects):
        print(__disable_billing_for_project(PROJECT_NAME, projects))
    else:
        print('Billing already disabled')


def __is_billing_enabled(project_name, projects):
    """
    Determine whether billing is enabled for a project
    @param {string} project_name Name of project to check if billing is enabled
    @return {bool} Whether project has billing enabled or not
    """
    res = projects.getBillingInfo(name=project_name).execute()
    return res['billingEnabled']


def __disable_billing_for_project(project_name, projects):
    """
    Disable billing for a project by removing its billing account
    @param {string} project_name Name of project disable billing on
    @return {string} Text containing response from disabling billing
    """
    body = {'billingAccountName': ''}  # Disable billing
    res = projects.updateBillingInfo(name=project_name, body=body).execute()
    print(f'Billing disabled: {json.dumps(res)}')
# [END functions_billing_stop]


# [START functions_billing_limit]
ZONE = 'us-west1-b'


def limit_use(data, context):
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    pubsub_json = json.loads(pubsub_data)
    cost_amount = pubsub_json['costAmount']
    budget_amount = pubsub_json['budgetAmount']
    if cost_amount <= budget_amount:
        print(f'No action necessary. (Current cost: {cost_amount})')
        return

    compute = discovery.build(
        'compute',
        'v1',
        cache_discovery=False,
    )
    instances = compute.instances()

    instance_names = __list_running_instances(PROJECT_ID, ZONE, instances)
    __stop_instances(PROJECT_ID, ZONE, instance_names, instances)


def __list_running_instances(project_id, zone, instances):
    """
    @param {string} project_id ID of project that contains instances to stop
    @param {string} zone Zone that contains instances to stop
    @return {Promise} Array of names of running instances
    """
    res = instances.list(project=project_id, zone=zone).execute()

    if 'items' not in res:
        return []

    items = res['items']
    running_names = [i['name'] for i in items if i['status'] == 'RUNNING']
    return running_names


def __stop_instances(project_id, zone, instance_names, instances):
    """
    @param {string} project_id ID of project that contains instances to stop
    @param {string} zone Zone that contains instances to stop
    @param {Array} instance_names Names of instance to stop
    @return {Promise} Response from stopping instances
    """
    if not len(instance_names):
        print('No running instances were found.')
        return

    for name in instance_names:
        instances.stop(
          project=project_id,
          zone=zone,
          instance=name).execute()
        print(f'Instance stopped successfully: {name}')
# [END functions_billing_limit]


# [START functions_billing_limit_appengine]
APP_NAME = os.getenv('GCP_PROJECT')


def limit_use_appengine(data, context):
    pubsub_data = base64.b64decode(data['data']).decode('utf-8')
    pubsub_json = json.loads(pubsub_data)
    cost_amount = pubsub_json['costAmount']
    budget_amount = pubsub_json['budgetAmount']
    if cost_amount <= budget_amount:
        print(f'No action necessary. (Current cost: {cost_amount})')
        return

    appengine = discovery.build(
        'appengine',
        'v1',
        cache_discovery=False
    )
    apps = appengine.apps()

    # Get the target app's serving status
    target_app = apps.get(appsId=APP_NAME).execute()
    current_status = target_app['servingStatus']

    # Disable target app, if necessary
    if current_status == 'SERVING':
        print(f'Attempting to disable app {APP_NAME}...')
        body = {'servingStatus': 'USER_DISABLED'}
        apps.patch(appsId=APP_NAME, updateMask='serving_status', body=body).execute()
# [END functions_billing_limit_appengine]
