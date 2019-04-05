""""SQL setup methods"""

import logging
import os
from contextlib import contextmanager
from datetime import datetime

import helpers
from base import (
    run_command,
    log_exception,
    run_command_readonly
)
from commands import get_command_result

LOGGER = logging.getLogger(__name__)


def get_connection_name(project, instance_name):
    """Get the sql connection name"""
    cmd = [
        'gcloud', 'sql', 'instances', 'describe', instance_name,
        '--project=' + project,
        "--format='value(connectionName)'"
    ]

    if not helpers.DRY_RUN:
        connection_name = str(run_command(cmd).
                              decode('utf-8')).replace('\n', '')
    else:
        connection_name = 'connection_name'

    return connection_name


@contextmanager
def gcs_acl_role(user_mail, role, path):
    """Temporary bucket ACL context"""
    LOGGER.debug('Adding ACL role to %s...', user_mail)
    cmd = [
        'gsutil', 'acl', 'ch', '-u', user_mail + role, path
    ]
    run_command(cmd)

    with log_exception():
        yield

    LOGGER.debug('Removing acl given for %s...', user_mail)
    cmd = [
        'gsutil', 'acl', 'ch', '-d', user_mail, path
    ]
    run_command(cmd)


def execute_storage_flow(project,
                         sql_input,
                         region,
                         sql_instance_service_account,
                         base_path,
                         use_dm):
    """Execute storage and clean storage flow, to generate db structure"""
    create_sql_bucket(project, region, use_dm)

    bucket_path = 'gs://' + project + '_db_load'

    with gcs_acl_role(sql_instance_service_account, ':W', bucket_path):
        file_path = '../k8s/db/dump-query_builder-201812281118.sql'
        dump_path = os.path.join(base_path, file_path)

        LOGGER.debug('Upload file to DB bucket...')
        cmd = [
            'gsutil', 'cp', dump_path, 'gs://' + project + '_db_load/'
        ]
        run_command(cmd)

        file_bucket_path = \
            'gs://{}_db_load/dump-query_builder-201812281118.sql'\
            .format(project)

        with gcs_acl_role(sql_instance_service_account, ':R',
                          file_bucket_path):
            LOGGER.debug('Load db structure...')
            cmd = [
                'gcloud', 'sql', 'import', 'sql', sql_input.instance_name,
                file_bucket_path,
                '--database=' + sql_input.database_name,
                '--quiet',
                '--project', project
            ]
            run_command(cmd)


def get_instance_service_account(project, sql_instance_name):
    """Get generated sql instance service account"""
    LOGGER.debug('Getting instance service account email address')
    cmd = [
        'gcloud', 'sql', 'instances', 'describe', sql_instance_name,
        '--project', project,
        "--format='value(serviceAccountEmailAddress)'"
    ]

    if not helpers.DRY_RUN:
        instance_service_account = str(run_command(cmd).
                                       decode('utf-8')).replace('\n', '')
    else:
        instance_service_account = 'instance_service_account'

    return instance_service_account


def create_sql_bucket(project, region, use_dm=False):
    """Create bucket to keep database strucuture"""
    bucket_name = project + '_db_load'
    bucket_log_name = project + '_db_load_log'
    cmd = [
        'gsutil', 'ls', '-p', project
    ]
    if not helpers.DRY_RUN:
        existing_buckets = str(run_command(cmd).decode('utf8')).split('\n')
    else:
        existing_buckets = []
    matching = [s for s in existing_buckets
                if bucket_name in s or
                bucket_log_name in s]

    if len(matching) == 2:
        LOGGER.debug('Buckets already exist in project, skipping creation...')
        return

    deployment_name = '-'.join([
        'dm',
        'bucket',
        project,
        datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ])

    if use_dm:
        bucket_template = os.path.join(helpers.BASE_DIR, 'dm', 'bucket.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            deployment_name,
            '--template', bucket_template,
            '--properties',
            ",".join([
                'project:' + project,
                'region:' + region,
                'bucket_name:' + bucket_name
            ]),
            '--project', project
        ]
    else:
        cmd = [
            'gsutil', 'mb',
            '-p', project,
            '-c', 'REGIONAL',
            '-l', region,
            'gs://{}/'.format(bucket_name)
        ]

    LOGGER.debug('creating DB bucket...')
    run_command(cmd)


def execute_dm_sql_structure(project, sql_input, region, use_dm=False):
    """Execute the configuration of sql on deployment manager"""
    deployment_name = '-'.join([
        'dm',
        'sql',
        project,
        datetime.utcnow().strftime('%Y%m%d%H%M%S')
    ])

    if use_dm:
        sql_template = os.path.join(helpers.BASE_DIR, 'dm', 'sql.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            deployment_name,
            '--template', sql_template,
            '--properties',
            ",".join([
                'instance_name:' + sql_input.instance_name,
                'region:' + region,
                'tier:' + sql_input.tier,
                'database_name:' + sql_input.database_name,
                'charset:' + sql_input.charset,
                'user_name:' + sql_input.user_name,
                'user_password:' + sql_input.user_password,
                'user_resource_name:' + sql_input.user_resource_name
            ]),
            '--project', project
        ]
        run_command(cmd)
    else:
        cmd = [
            'gcloud', 'sql', 'instances', 'create',
            sql_input.instance_name,
            '--region {}'.format(region),
            '--tier {}'.format(sql_input.tier),
            '--project', project
        ]
        run_command(cmd)

        cmd = [
            'gcloud', 'sql', 'databases', 'create',
            sql_input.database_name,
            '--instance {}'.format(sql_input.instance_name),
            '--charset {}'.format(sql_input.charset),
            '--project', project
        ]
        run_command(cmd)

        cmd = [
            'gcloud', 'sql', 'users', 'create',
            sql_input.user_name,
            '--instance {}'.format(sql_input.instance_name),
            '--password {}'.format(sql_input.user_password),
            '--project', project
        ]
        run_command(cmd)


def stop_instance(instance_name, project):
    """Stop the given SQL instance"""
    cmd = [
        'gcloud', 'sql', 'instances', 'patch', instance_name,
        '--activation-policy', 'NEVER',
        '--project', project
    ]
    LOGGER.debug('Stopping instance')
    run_command(cmd)


def cloud_sql_instance_exists(cloud_sql_instance_name, project):
    command_ = [
        'gcloud', 'sql', 'instances', 'list',
        '--filter', 'NAME=' + cloud_sql_instance_name,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def start_cloud_sql_instance(instance_name, project):
    """Start the given SQL instance"""
    cmd = [
        'gcloud', 'sql', 'instances', 'patch', instance_name,
        '--activation-policy', 'ALWAYS',
        '--project', project
    ]
    LOGGER.debug('Starting instance')
    run_command(cmd)


def cloud_sql_instance_running(instance_name, project):
    """Verify if the given SQL instance has started"""
    command_ = [
        'gcloud', 'sql', 'instances', 'describe', instance_name,
        '--format', 'value(settings.activationPolicy)',
        '--project', project
    ]
    result_ = run_command_readonly(command_).decode("utf-8").strip()
    return result_ == 'ALWAYS'

