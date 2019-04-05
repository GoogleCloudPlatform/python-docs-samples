#pylint: disable=missing-docstring, C0301

import os
from commands import (copy_files, create_file_from_template, deployment_exists,
                      gae_exists, get_or_create_client_key,
                      get_organization_display_name, subscription_exists,
                      topic_exists)

import helpers
import logger
from base import run_command, scape_to_os


def create_topic(project, name):
    if not topic_exists(project, name):
        logger.info('Creating {} topic'.format(name))
        cmd = [
            'gcloud', 'pubsub', 'topics', 'create',
            name,
            '--project', project
        ]
        run_command(cmd)
    else:
        logger.warn('{} topic already exists, skipping creation'.format(name))


def create_subscription(project, name, endpoint, topic):
    if not subscription_exists(project, name):
        logger.info('Creating {} subscription'.format(name))
        cmd = [
            'gcloud', 'pubsub', 'subscriptions', 'create',
            name,
            '--project', project,
            '--topic', 'projects/{}/topics/{}'.format(project, topic),
            '--ack-deadline', '300',
            '--push-endpoint', endpoint
        ]
        run_command(cmd)
    else:
        logger.warn('{} subscription already exists, skipping creation'.format(name))


def main_creator_commands(args):
    # project
    project = args.creator_project_name
    token = get_or_create_client_key(tool='creator', key_name='demomode')

    # pub/sub
    logger.step('Creating Pub/Sub topics and subscriptions...')
    create_topic(project, 'publish_processing')

    endpoint_url = 'https://{}.appspot.com/_ah/push-handlers/receive_message?token={}'.format(project, token)
    create_topic(project, 'demomode')
    create_subscription(project, 'demomodesubscriber', endpoint_url, 'demomode')

    status_endpoint_url = 'https://{}.appspot.com/_ah/push-handlers/set_status?token={}'.format(project, token)
    create_topic(project, 'publish_status')
    create_subscription(project, 'statussubscriber', status_endpoint_url, 'publish_status')

    # copy service account file
    logger.step('Copying service account...')
    dst_sa_path = os.path.join(
        helpers.BASE_DIR,
        'creator',
        'appflex',
        'accounts'
    )
    if not os.path.exists(dst_sa_path):
        os.makedirs(dst_sa_path)
    dst_sa_file = os.path.join(dst_sa_path, 'cscc_api_client.json')
    copy_files(args.creator_sa_file, dst_sa_file)

    dst_sa_file = os.path.join(dst_sa_path, 'publisher_sa.json')
    copy_files(args.publisher_sa_file, dst_sa_file)

    # gae
    logger.step('Deploying GAE application...')
    logger.info('Updating GAE app config file...')
    organization_display_name = get_organization_display_name(args.organization_id)
    update_creator_config(os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'app.yaml'),
                          project,
                          args.organization_id,
                          token,
                          organization_display_name,
                          args.scc_api_key)

    logger.info('Deploying...')
    cmd = [
        'gcloud', 'app', 'deploy',
        os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'app.yaml'),
        os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'cron.yaml'),
        '--quiet',
        '--project', project]
    run_command(cmd)


def main_creator(args):
    project = args.creator_project_name
    token = get_or_create_client_key(tool='creator', key_name='demomode')
    print('creator - creator application creation.')
    infra_dm_name = '-'.join(['infra', project])
    if not deployment_exists(project,infra_dm_name):
        endpoint_url = 'https://{}.appspot.com/_ah/push-handlers/receive_message?token={}'.format(project, token)
        status_endpoint_url = 'https://{}.appspot.com/_ah/push-handlers/set_status?token={}'.format(project, token)
        event_query_endpoint_url = 'https://{}.appspot.com/_ah/push-handlers/post_event_query?token={}'.format(project, token)
        infra_template = os.path.join(helpers.BASE_DIR, 'creator', 'dm', 'creatorConnectorInfra.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            infra_dm_name,
            '--template', infra_template,
            '--properties',
            ",".join([
                'project-name:' + scape_to_os(project),
                'endpoint-url:' + endpoint_url,
                'status_endpoint_url:' + status_endpoint_url,
                'event_query_endpoint_url:' + event_query_endpoint_url
            ]),
            '--project', project]
        run_command(cmd)
    creator_sa_file = args.creator_sa_file
    print('creator - copy SCC service account')
    dst_sa_path = os.path.join(
        helpers.BASE_DIR,
        'creator',
        'appflex',
        'accounts'
    )
    if not os.path.exists(dst_sa_path):
        os.makedirs(dst_sa_path)
    dst_sa_file = os.path.join(
        dst_sa_path,
        'cscc_api_client.json'
    )
    copy_files(creator_sa_file, dst_sa_file)

    dst_sa_file = os.path.join(dst_sa_path, 'publisher_sa.json')
    copy_files(args.publisher_sa_file, dst_sa_file)

    organization_display_name = get_organization_display_name(args.organization_id)
    update_creator_config(os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'app.yaml'),
                          project,
                          args.organization_id,
                          token,
                          organization_display_name,
                          args.scc_api_key)
    # deploy app
    cmd = [
        'gcloud', 'app', 'deploy',
        os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'app.yaml'),
        os.path.join(helpers.BASE_DIR, 'creator', 'appflex', 'cron.yaml'),
        '--quiet',
        '--project', project]
    run_command(cmd)


def update_creator_config(config_file, project_id, organization_id, token, organization_display_name, scc_api_key):
    context = {}

    logger.info('Overwriting organization id with: {}'.format(organization_id))
    context['organization_id'] = organization_id

    logger.info('Overwriting organization display name with: {}'.format(organization_display_name))
    context['organization_display_name'] = organization_display_name

    logger.info('Overwriting pubsub token')
    context['token'] = token

    logger.info('Overwriting project id with: {}'.format(project_id))
    context['project_id'] = project_id

    logger.info('Overwriting scc api key with: {}'.format(scc_api_key))
    context['scc_client_developer_key'] = scc_api_key

    logger.info('Creating file from templade...')
    create_file_from_template('template_creator_app_yaml.jinja', context, config_file)
