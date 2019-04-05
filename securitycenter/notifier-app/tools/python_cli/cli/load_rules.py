"""Load rules."""
from __future__ import print_function

import logging
import sys

import yaml
import os
import os.path

import api_client
from api_client.rest import ApiException

from python_cli.cli.cli_utils import read_file, setup_api_instance

ALLOWED = {
            'notificationType': [
              'SCAN-CONFIGURATIONS',
              'SCAN-FINDINGS',
              'ASSETS',
              'FINDINGS',
              'CLOUD-FUNCTION'
            ],
            'eventType': [
              'ANY-CREATED',
              'ANY-MODIFIED',
              'ANY-DELETED',
              'ANY-ACTIVE',
              'ANY-OPENED',
              'ANY-RESOLVED',
              'ALL'
            ]
          }

errors = {'notificationType': [],
          'eventType': []}


def load_rules(yaml_file, gcpid, token, api_endpoints_url):
    if os.path.isfile(yaml_file):
        content = read_file(yaml_file)
        stream = yaml.load(content)
        rules = from_yaml_to_json(stream)
        call_api(rules, token, api_endpoints_url)


def from_yaml_to_json(content):
    """Transform rules from YAML to JSON."""
    api_rules = []
    rules = content['rules']

    for rule in rules:
        actions = rule.get('actions')
        api_actions = []
        if actions:
            for action in actions:
                if action['type'].upper() not in ALLOWED['eventType']:
                    errors['eventType'].append(action['type'])
                else:
                    api_action = api_client.Action(type=action['type'])
                    api_actions.append(api_action)
        
            if rule['type'].upper() not in ALLOWED['notificationType']:
                errors['notificationType'].append(rule['type'])
            else:
                api_rule = api_client.Rule(
                    type=rule['type'],
                    actions=api_actions
                )
                api_rules.append(api_rule)
        else:
            if rule['type'].upper() not in ALLOWED['notificationType']:
                errors['notificationType'].append(rule['type'])
            else:
                api_rule = api_client.Rule(type=rule['type'])
                api_rules.append(api_rule)
    if errors['notificationType'] or errors['eventType']:
        logging.warn(('The YAML file contains invalid '
                      'notification and/or event type(s):\n'
                      'Invalid notification type: %s\n'
                      'Invalid event type: %s\n'
                      'These are the valid notification and event types:\n'
                      'Valid notification types: %s\n'
                      'Valid event types: %s\n'),
                     errors['notificationType'], errors['eventType'],
                     ALLOWED['notificationType'], ALLOWED['eventType'])
        sys.exit(1)
    else:
        return api_rules


def call_api(rules, token, api_endpoint_url):
    """Call Endpoints API."""
    api_instance = setup_api_instance(api_client, api_endpoint_url, token)
    body = api_client.RulesRequestBody()
    body.rules = rules
    try:
        api_instance.gcp_noti_api_rules_with_http_info(body=body)
    except ApiException as ex:
        logging.warn(("Exception when calling "
                      "DefaultApi->gcp_noti_api_rules_with_http_info: %s\n"),
                     ex)
