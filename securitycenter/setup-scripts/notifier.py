#pylint: disable=missing-docstring, C0301

import base64
import os
import tempfile
import time
import zipfile
from commands import (bucket_status, deployment_exists, gae_exists,
                      get_or_create_client_key, subscription_exists,
                      topic_exists)

import helpers
import logger
from base import get_sdk_path, run_command, scape_to_os


def main_notifier_commands(args):
    # project
    project = args.notifier_project
    notifier_path = helpers.BASE_DIR

    # bucket
    logger.step('Creating buckets to store cloud functions...')
    cf_bucket_name = args.notifier_bucket or bucket_name()
    cf_bucket_status = bucket_status(cf_bucket_name)
    if cf_bucket_status == 'NotFound':
        logger.info('Bucket not found, creating...')
        cmd = [
            'gsutil', 'mb',
            '-p', project,
            '-c', 'REGIONAL',
            '-l', args.region,
            'gs://{}/'.format(cf_bucket_name)
        ]
        run_command(cmd)
    else:
        logger.warn('Bucket already exists, skipping creation')

    # cloud function
    logger.step('Deploying cloud function...')
    appengine_version = args.notifier_appengine_version
    function_name = appengine_version + '_notifyDefaultHttp'

    logger.info('Generating application config file...')
    generate_config_json(notifier_path, appengine_version)

    logger.info('Uploading cloud function to bucket...')
    upload_cf(function_name, notifier_path, cf_bucket_name)

    logger.info('Deploying cloud function...')
    cmd = [
        'gcloud', 'functions', 'deploy', function_name,
        '--project', project,
        '--source', 'gs://{}/{}.zip'.format(cf_bucket_name, function_name),
        '--region', args.region,
        '--trigger-http',
        '--runtime', 'nodejs6',
        '--timeout', '180',
        '--memory', '256MB'
    ]
    run_command(cmd)

    # pubsub
    logger.step('Creating Pub/Sub topics and subscriptions...')
    if not args.notifier_skip_pubsub:
        topic_name = appengine_version + '-test'
        create_topic(project, topic_name)

        subscription_name = appengine_version + '-noti-subscription'
        endpoint_url = 'https://' + appengine_version + '-pubsub-dot-' + project + '.appspot.com/_ah/push-handlers/receive_message'
        create_subscription(project, subscription_name, endpoint_url, topic_name)
    else:
        logger.warn('Skipping creation since notifier_skip_pubsub parameter is present')

    # gae
    logger.step('Deploying GAE application...')
    logger.info('Testing and Building application projects...')
    cmd = [
        'mvn', '-f', os.path.join(notifier_path, 'notifier', 'app', 'pom.xml'),
        'clean',
        'install',
        '-DskipTests=true'
    ]
    run_command(cmd)

    logger.info('Deploying pubsub cron service...')
    gcloud_path = get_sdk_path()
    cmd = [
        'mvn', '-f', os.path.join(notifier_path, 'notifier', 'app', 'dispatcher', 'pom.xml'),
        'appengine:deploy',
        'appengine:deployQueue',
        'appengine:deployCron',
        '-DskipTests=true',
        '-Dapp.deploy.project=' + project,
        '-Dapp.deploy.promote=False',
        '-Dapp.deploy.stopPreviousVersion=False',
        '-Dapp.deploy.version=' + appengine_version + '-pubsub',
        '-Dnotification.namespace=' + appengine_version,
        '-Dhash.mechanism=' + args.notifier_hash_mecanism,
        '-DcloudSdkPath=' + gcloud_path
    ]
    run_command(cmd)

    logger.info('Deploying application...')
    cmd = [
        'mvn', '-f', os.path.join(notifier_path, 'notifier', 'app', 'api', 'pom.xml'),
        'exec:java',
        '-DskipTests',
        '-DGetOpenApiDoc',
        '-Dendpoints.service.prefix=' + appengine_version + '-api',
        '-Dendpoints.project.id=' + project]
    run_command(cmd)

    logger.info('Creating GAE API endpoint...')
    cmd = [
        'gcloud', 'endpoints', 'services', 'deploy', 'openapi.json',
        '--project', project
    ]
    run_command(cmd)

    logger.info('Deploying API endpoint...')
    cmd = [
        'mvn', '-f',
        os.path.join(notifier_path, 'notifier', 'app', 'api', 'pom.xml'),
        'appengine:deploy',
        '-DskipTests=true',
        '-Dapp.deploy.project=' + project,
        '-Dapp.deploy.promote=False',
        '-Dapp.deploy.stopPreviousVersion=False',
        '-Dapp.deploy.version=' + appengine_version + '-api',
        '-Dnotification.namespace=' + appengine_version,
        '-DcloudSdkPath=' + gcloud_path,
        '-Dendpoints.service.prefix=' + appengine_version + '-api',
        '-Dendpoints.project.id=' + project
    ]
    run_command(cmd)


def main_notifier(args):
    notifier_path = helpers.BASE_DIR
    project = args.notifier_project
    appengine_version = args.notifier_appengine_version

    print('notifier - cloud function bucket creation.')
    cf_bucket = args.notifier_bucket or bucket_name()
    cf_bucket_status = bucket_status(cf_bucket)
    if cf_bucket_status == 'NotFound':
        bucket_template = os.path.join(helpers.BASE_DIR, 'notifier', 'dm', 'bucket.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            '-'.join(['bucket-cf', project]),
            '--template', bucket_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'bucketname:' + cf_bucket,
            ]),
            '--project', project]
        run_command(cmd)

    print('notifier - notifier application creation.')
    infra_dm_name = '-'.join(['infra', project])
    if not deployment_exists(project, infra_dm_name):
        # Configure CF
        function_name = appengine_version + '_notifyDefaultHttp'
        generate_config_json(notifier_path, appengine_version)
        upload_cf(function_name, notifier_path, cf_bucket)
        # Infra deploy
        infra_template = os.path.join(helpers.BASE_DIR, 'notifier', 'dm', 'notifierInfra.py')
        endpoint_url = 'https://' + appengine_version + '-pubsub-dot-' + project + '.appspot.com/_ah/push-handlers/receive_message'
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            infra_dm_name,
            '--template', infra_template,
            '--properties',
            ",".join([
                'topic_name:' + appengine_version + '-test',
                'subscriber_name:' + appengine_version + '-noti-subscription',
                'endpoint_url:' + endpoint_url,
                'function_name:' + function_name,
                'cf_bucket:' + cf_bucket,
                'region:' + scape_to_os(args.region),
                'skip_pubsub:' + str(args.notifier_skip_pubsub)
            ]),
            '--project', project]
        run_command(cmd)

    # Build and run tests of every project
    cmd = [
        'mvn', '-f',
        os.path.join(notifier_path, 'notifier', 'app', 'pom.xml'),
        'clean', 'install', '-DskipTests=true'
    ]
    run_command(cmd)

    # Pubsub deploy
    print('notifier - deploy pubsub service')
    gcloud_path = get_sdk_path()
    cmd = [
        'mvn', '-f', os.path.join(notifier_path, 'notifier', 'app', 'dispatcher', 'pom.xml'),
        'appengine:deploy',
        'appengine:deployQueue',
        'appengine:deployCron',
        '-DskipTests=true',
        '-Dapp.deploy.project=' + project,
        '-Dapp.deploy.promote=False',
        '-Dapp.deploy.stopPreviousVersion=False',
        '-Dapp.deploy.version=' + appengine_version + '-pubsub',
        '-Dnotification.namespace=' + appengine_version,
        '-Dhash.mechanism=' + args.notifier_hash_mecanism,
        '-DcloudSdkPath=' + gcloud_path
    ]
    run_command(cmd)

    # Api deploy
    cmd = [
        'mvn', '-f', os.path.join(
            notifier_path,
            'notifier', 'app', 'api', 'pom.xml'
        ),
        'exec:java', '-DskipTests',
        '-DGetOpenApiDoc',
        '-Dendpoints.service.prefix=' + appengine_version + '-api',
        '-Dendpoints.project.id=' + project]
    run_command(cmd)

    print('notifier - deploy api endpoints')
    cmd = [
        'gcloud', 'endpoints', 'services', 'deploy', 'openapi.json',
        '--project', project
    ]
    run_command(cmd)
    cmd = [
        'mvn', '-f',
        os.path.join(notifier_path, 'notifier', 'app', 'api', 'pom.xml'),
        'appengine:deploy',
        '-DskipTests=true',
        '-Dapp.deploy.project=' + project,
        '-Dapp.deploy.promote=False',
        '-Dapp.deploy.stopPreviousVersion=False',
        '-Dapp.deploy.version=' + appengine_version + '-api',
        '-Dnotification.namespace=' + appengine_version,
        '-DcloudSdkPath=' + gcloud_path,
        '-Dendpoints.service.prefix=' + appengine_version + '-api',
        '-Dendpoints.project.id=' + project
    ]
    run_command(cmd)


def bucket_name():
    """Gets a generated bucket name"""
    name = os.path.expanduser('~/.google_code_lab_notification_cloud_function_bucket_name')
    if not os.path.isfile(name):
        with open(name, 'w') as filez:
            value = 'cl-noti-cf-bucket-{}-{}'.format(int(time.time()), base64.b64encode(os.urandom(9), altchars=b'ww').decode()).lower()
            filez.write(value)
    return open(name).read()


def generate_config_json(base_path, version):
    """Generates config.json based on sample and replace it with custom values"""
    config = open(os.path.join(base_path, 'notifier', 'function', 'default', 'config.json.sample')).read()
    config = config.replace('YOUR_CLIENT_KEY', get_or_create_client_key(tool='notifier', key_name='default'))
    config = config.replace('YOUR_APPLICATION_VERSION', version)
    with open(os.path.join(base_path, 'notifier', 'function', 'default', 'config.json'), 'w') as filez:
        filez.write(config)


def upload_cf(name, base_path, bucket):
    """Generates a CF zip and upload it to bucket"""
    zip_path = os.path.join(tempfile.gettempdir(), name + '.zip')
    zip_file = zipfile.ZipFile(zip_path, mode='w', compression=zipfile.ZIP_DEFLATED)
    for entry in os.scandir(os.path.join(base_path, 'notifier', 'function', 'default')):
        zip_file.write(entry.path, entry.name)
    zip_file.close()
    cmd = [
        'gsutil', 'cp', zip_path, 'gs://' + bucket
    ]
    run_command(cmd)


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
            '--ack-deadline', '10',
            '--push-endpoint', endpoint
        ]
        run_command(cmd)
    else:
        logger.warn('{} subscription already exists, skipping creation'.format(name))
