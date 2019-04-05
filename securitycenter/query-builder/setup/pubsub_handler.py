""""Pubsub setup methods"""

import logging
import os
from datetime import datetime

import helpers
from base import run_command

LOGGER = logging.getLogger(__name__)


def create_and_subscribe(project, topic_name, subscription_name, use_dm=False):
    """
    Create a pubsub infra with Topic linked to Subscription
    :param project: project id to host topic/subscription
    :param topic_name: name of the topic
    :param subscription_name: name of the subscription
    :return:
    """
    deployment_name = '-'.join([
        'dm',
        'pubsub',
        project,
        datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ])

    if use_dm:
        pubsub_template = os.path.join(helpers.BASE_DIR, 'dm', 'pubsub_infra.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            deployment_name,
            '--template', pubsub_template,
            '--properties',
            ",".join([
                'project:' + project,
                'topic_name:' + topic_name,
                'subscription_name:' + subscription_name
            ]),
            '--project', project
        ]
        run_command(cmd)
    else:
        cmd = [
            'gcloud', 'pubsub', 'topics', 'create',
            topic_name,
            '--project', project
        ]
        run_command(cmd)

        cmd = [
            'gcloud', 'pubsub', 'subscriptions', 'create',
            subscription_name,
            '--project', project,
            '--topic', 'projects/{}/topics/{}'.format(project, topic_name)
        ]
        run_command(cmd)


def list_subscriptions():
    """Get the list of subscriptions of current project"""
    cmd = [
        'gcloud', 'pubsub', 'subscriptions', 'list'
    ]
    if not helpers.DRY_RUN:
        return str(run_command(cmd).decode('utf8'))
    else:
        return 'Subscription List'
