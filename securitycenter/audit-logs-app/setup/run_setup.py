#!/usr/bin/env python3
#pylint: disable=missing-docstring, C0301, no-value-for-parameter

import json
import os
import re
import sys
from datetime import datetime

import click

import helpers
import logger
from base import run_command, run_command_readonly, scape_to_os
from click_script_commons import (
    instruction_separator,
    configure_helpers,
    set_base_dir
)
from commands import (bucket_status, copy_service_account, deployment_exists,
                      project_exists, simulation_mode_disclaimer, sink_exists,
                      subscription_exists, topic_exists)
from grant_roles_to_member import grant_roles_on_project
from service_account_usage_handler import service_account_wall
from simulation_mode import simulation_wall
from update_cloud_function import zip_and_store_cf

SINK_SA_REGEX = re.compile(r'(serviceAccount:o\w+-\w+@gcp-sa-logging\.iam\.gserviceaccount\.com)')


@click.command()
@click.option('--organization_id', help='organization id', required=True)
@click.option('--project', help='Project', required=True)
@click.option('--cf_bucket', help='Cloud function bucket, this bucket is regional')
@click.option('--df_bucket', help='Dataflow function bucket, this bucket is regional')
@click.option('--bucket_region', help='Cloud function location', required=True)
@click.option('--df_window', help='Dataflow time window, set in minutes')
@click.option('--scc_api_key', help='API Key to access SCC API from your SCC enabled project', required=True)
@click.option('--scc_sa_file', type=click.Path(exists=True), help='Service account for Security Command Center access.', required=True)
@click.option('--org_browser_sa_file', type=click.Path(exists=True), help='Service account for browser access at org level.', required=True)
@click.option('--audit_logs_source_id', help='Source ID to create the findings for audit logs', required=True)
@click.option('--binary_authorization_source_id', help='Source ID to create the findings for binary authorization', required=True)
@click.option('--simulation/--no-simulation', default=True, help='Simulate the execution. Do not execute any command.')
@click.option('--use_dm', is_flag=True, default=False, help='Run setup with deployment manager instead of the default commands.')
def __run_steps(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation, use_dm, binary_authorization_source_id):
    if use_dm:
        __run_steps_dm(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation, binary_authorization_source_id)
    else:
        __run_commands(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation, binary_authorization_source_id)


def __create_topic(project, name):
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


def __create_subscription(project, name, topic):
    if not subscription_exists(project, name):
        logger.info('Creating {} subscription'.format(name))
        cmd = [
            'gcloud', 'pubsub', 'subscriptions', 'create',
            name,
            '--project', project,
            '--topic', 'projects/{}/topics/{}'.format(project, topic),
            '--ack-deadline', '300'
        ]
        run_command(cmd)
    else:
        logger.warn('{} subscription already exists, skipping creation'.format(name))


def __create_bucket(name, region, project):
    status = bucket_status(name)
    if status == 'NotFound':
        logger.info('Bucket not found, creating...')
        cmd = [
            'gsutil', 'mb',
            '-p', project,
            '-c', 'REGIONAL',
            '-l', region,
            'gs://{}/'.format(name)
        ]
        run_command(cmd)
    else:
        logger.warn('Bucket already exists, skipping creation')


def __create_sink(name, _filter, destination_topic_name, project, organization_id):
    if not sink_exists(organization_id, name):
        logger.info('Creating sink {}...'.format(name))
        cmd = [
            'gcloud', 'logging', 'sinks', 'create', name,
            'pubsub.googleapis.com/projects/{}/topics/{}'.format(project, destination_topic_name),
            '--include-children',
            '--log-filter \'{}\''.format(_filter),
            '--organization', organization_id
        ]
        run_command(cmd)
    else:
        logger.warn('{} sink already exists, skipping creation'.format(name))


def __grant_roles_sink_writter(sink_name, project, organization_id):
    logger.info('Grantting sink permission to publish on pubsub...')
    outputs = run_command_readonly([
        'gcloud', 'logging', 'sinks', 'describe',
        sink_name,
        '--organization', organization_id,
        '--format', 'value(writerIdentity)'
    ])
    account = outputs.decode('utf-8').strip()
    if account:
        sink_publisher_role = os.path.join(helpers.BASE_DIR, 'roles', 'sink_publisher.txt')
        grant_roles_on_project(sink_publisher_role, project, account)


def __run_commands(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation, binary_authorization_source_id):
    # print simulation mode
    configure_helpers(simulation, '..')

    simulation_mode_disclaimer()

    # check project
    logger.step('Checking project existence...')
    __validate_project(project)

    # service account copying
    logger.step('Copying service account to function...')
    dst_scc_sa_path = os.path.join(helpers.BASE_DIR, 'function', 'finding-scc-writer', 'accounts')
    copy_service_account(scc_sa_file, dst_scc_sa_path, 'cscc_api_client.json')

    dst_browser_sa_path = os.path.join(helpers.BASE_DIR, 'function', 'log-single-converter', 'accounts')
    copy_service_account(org_browser_sa_file, dst_browser_sa_path, 'google_api_client.json')

    logger.step('Copying service account to dataflow...')
    dst_browser_sa_path = os.path.join(helpers.BASE_DIR, 'dataflow', 'aggregator', 'src', 'main', 'resources')
    copy_service_account(org_browser_sa_file, dst_browser_sa_path, 'google_api_client.json')

    # create dataflow bucket
    logger.step('Creating dataflow bucket...')
    df_bucket_name = df_bucket or 'bucket-df-' + project
    __create_bucket(df_bucket_name, bucket_region, project)

    # pub/sub
    logger.step('Creating Pub/Sub topics and subscriptions...')
    log_sink_single_name = 'log_sink_single'
    __create_topic(project, log_sink_single_name)

    __create_topic(project, 'topic_single_findings')
    __create_subscription(project, 'subscription_single_findings', 'topic_single_findings')

    log_sink_aggregated_name = 'log_sink_aggregated'
    __create_topic(project, log_sink_aggregated_name)
    __create_subscription(project, 'subscription_aggregated_logs', log_sink_aggregated_name)

    __create_topic(project, 'topic_aggregated_findings')
    __create_subscription(project, 'subscription_aggregated_findings', 'topic_aggregated_findings')

    findings_to_save_name = 'findings_to_save'
    __create_topic(project, findings_to_save_name)

    # functions
    logger.step('Creating functions bucket...')
    cf_bucket_name = cf_bucket or 'bucket-cf-' + project
    __create_bucket(cf_bucket_name, bucket_region, project)

    logger.step('Uploading functions to bucket...')
    converter_function_name = 'log-single-converter'
    zip_and_store_cf(converter_function_name, '{}.zip'.format(converter_function_name), 'gs://' + cf_bucket_name)
    writer_function_name = 'finding-scc-writer'
    zip_and_store_cf(writer_function_name, '{}.zip'.format(writer_function_name), 'gs://' + cf_bucket_name)

    logger.step('Deploying function...')
    cmd = [
        'gcloud', 'functions', 'deploy', converter_function_name,
        '--project', project,
        '--source', 'gs://{}/{}.zip'.format(cf_bucket_name, converter_function_name),
        '--region', bucket_region,
        '--trigger-topic', log_sink_single_name,
        '--entry-point', 'convert',
        '--runtime', 'nodejs6',
        '--timeout', '180',
        '--memory', '256MB'
    ]
    run_command(cmd)
    cmd = [
        'gcloud', 'functions', 'deploy', writer_function_name,
        '--project', project,
        '--source', 'gs://{}/{}.zip'.format(cf_bucket_name, writer_function_name),
        '--region', bucket_region,
        '--trigger-topic', findings_to_save_name,
        '--entry-point', 'sendFinding',
        '--runtime', 'nodejs6',
        '--timeout', '180',
        '--memory', '256MB',
        '--set-env-vars', 'ORGANIZATION_ID={},API_KEY={},SOURCE_ID={},BIN_AUTH_SOURCE_ID={}'.format(organization_id, scc_api_key, audit_logs_source_id, binary_authorization_source_id)
    ]
    run_command(cmd)

    # sinks
    # reset base_dir to attend sink roles base dir
    set_base_dir()

    logger.step('Creating single sinks...')
    network_types_filters = ["gce_subnetwork", "gce_firewall_rule",
                             "gce_forwarding_rule", "gce_network", "gce_route",
                             "gce_reserved_address", "gce_target_http_proxy",
                             "gce_target_https_proxy", "gce_target_ssl_proxy",
                             "gce_router", "vpn_gateway", "dns_managed_zone",
                             "network_security_policy"]
    gce_types_filters = ["gce_instance", "gce_disk", "gce_node_group",
                         "gce_node_template", "gce_target_pool",
                         "gce_autoscaler", "gce_backend_service",
                         "gce_backend_bucket", "gce_client_ssl_policy",
                         "gce_commitment", "gce_license", "gce_health_check",
                         "gce_url_map", "gce_project", "gce_snapshot",
                         "gce_ssl_certificate", "gce_image",
                         "gce_instance_group", "gce_instance_group_manager",
                         "gce_instance_template", "gce_operation"]
    single_sinks = {
        'sink_network_single': 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type=({})'.format(' OR '.join(network_types_filters)),
        'sink_gce_single': 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type=({})'.format(' OR '.join(gce_types_filters)),
        'sink_gcs_single': 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type="gcs_bucket"',
        'sink_binauthz_single': 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND resource.type="k8s_cluster" AND protoPayload.methodName="io.k8s.core.v1.pods.create" AND (protoPayload.response.code=403 OR protoPayload.request.metadata.annotations."alpha.image-policy.k8s.io/break-glass"="true" OR labels."imagepolicywebhook.image-policy.k8s.io/break-glass"="true")'
    }
    for sink, _filter in single_sinks.items():
        __create_sink(sink, _filter, log_sink_single_name, project, organization_id)
        __grant_roles_sink_writter(sink, project, organization_id)

    logger.step('Creating aggregated sinks...')
    aggregated_sinks = {
        'sink_iam_aggregated': 'protoPayload.@type="type.googleapis.com/google.cloud.audit.AuditLog" AND logName:"activity" AND protoPayload.methodName=SetIamPolicy'
    }
    for sink, _filter in aggregated_sinks.items():
        __create_sink(sink, _filter, log_sink_aggregated_name, project, organization_id)
        __grant_roles_sink_writter(sink, project, organization_id)

    # deploy gae
    logger.step('Deploying GAE application...')
    # set base_dir to attend gae throttler base dir
    set_base_dir('..')
    __gae_throttler_setup(project)

    # create dataflow and its job
    logger.step('Creating Dataflow...')
    logger.info('Creating dataflow template...')
    df_bucket_path = 'gs://{}'.format(df_bucket_name)
    df_window = df_window or 60
    __dataflow_template_creation(project, df_bucket_path, df_window)

    logger.info('Creating dataflow job...')
    __dataflow_job_from_template(project, 'aggregator', df_bucket_path)


def __run_steps_dm(organization_id, project, cf_bucket, df_bucket, bucket_region, df_window, scc_api_key, scc_sa_file, org_browser_sa_file, audit_logs_source_id, simulation, binary_authorization_source_id):
    with service_account_wall():
        with simulation_wall(simulation):
            configure_helpers(simulation, '..')

            __validate_project(project)

            dst_scc_sa_path = os.path.join(helpers.BASE_DIR, 'function', 'finding-scc-writer', 'accounts')
            copy_service_account(scc_sa_file, dst_scc_sa_path, 'cscc_api_client.json')

            # Copy browser sa to cloud function
            dst_browser_sa_path = os.path.join(
                helpers.BASE_DIR,
                'function',
                'log-single-converter',
                'accounts')
            copy_service_account(org_browser_sa_file, dst_browser_sa_path, 'google_api_client.json')
            # Copy browser sa to dataflow
            dst_browser_sa_path = os.path.join(
                helpers.BASE_DIR,
                'dataflow',
                'aggregator',
                'src',
                'main',
                'resources')
            copy_service_account(org_browser_sa_file, dst_browser_sa_path, 'google_api_client.json')

            df_bucket_name = df_bucket or 'bucket-df-' + project
            __create_dataflow_bucket(df_bucket_name, bucket_region, project)

            cf_bucket_name = cf_bucket or 'bucket-cf-' + project
            __cloud_function_bucket(cf_bucket_name, project, bucket_region)

            infra_dm_name = '-'.join(['infra', project])
            __application_creation(cf_bucket_name, infra_dm_name, organization_id, project, bucket_region, scc_api_key, audit_logs_source_id, binary_authorization_source_id)

            __grant_roles(infra_dm_name, project)

            __gae_throttler_setup(project)

            df_bucket_path = 'gs://{}'.format(df_bucket_name)

            df_window = df_window or 60

            __dataflow_template_creation(project, df_bucket_path, df_window)

            __dataflow_job_from_template(project, 'aggregator', df_bucket_path)


def __create_dataflow_bucket(df_bucket_name, location, project):
    with instruction_separator('Dataflow bucket.'):
        cf_bucket_status = bucket_status(df_bucket_name)
        if "NotFound" == cf_bucket_status:
            bucket_template = os.path.join(
                helpers.BASE_DIR, 'dm', 'bucket.py')
            cmd = [
                'gcloud', 'deployment-manager', 'deployments', 'create',
                '-'.join(['bucket', project,
                          datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
                '--template', bucket_template,
                '--properties',
                ",".join([
                    'location:' + scape_to_os(location),
                    'bucketname:' + df_bucket_name,
                    'storageClass:' + "REGIONAL",
                ]),
                '--project', project
            ]
            run_command(cmd)


def __gae_throttler_setup(project):
    throttler_path = os.path.join(helpers.BASE_DIR, 'throttler', 'app.yaml')
    run_command(['gcloud', 'app', 'deploy', throttler_path, '-q', '--project', project])

    cron_path = os.path.join(helpers.BASE_DIR, 'throttler', 'cron.yaml')
    run_command(['gcloud', 'app', 'deploy', cron_path, '-q', '--project', project])


def __dataflow_template_creation(project, dataflow_bucket, window_size):
    output_topic = 'topic_aggregated_findings'
    subscription = 'subscription_aggregated_logs'
    dataflow_subscription_path = 'projects/{}/subscriptions/{}'.format(project, subscription)
    dataflow_output_topic_path = 'projects/{}/topics/{}'.format(project, output_topic)
    main_class = 'com.google.log.audit.FullLogAggregatorWithErrorTreatment'
    args = ['--runner=DataflowRunner',
            '--project={}'.format(project),
            '--templateLocation={}/templates/DataflowJobTemplate'.format(dataflow_bucket),
            '--gcpTempLocation={}/temp'.format(dataflow_bucket),
            '--windowSize={}'.format(window_size),
            '--pubsubSubscription={}'.format(dataflow_subscription_path),
            '--outputTopic={}'.format(dataflow_output_topic_path),
            '--output={}/invalidLogs'.format(dataflow_bucket)]

    dataflow_path = os.path.join(helpers.BASE_DIR, 'dataflow', 'aggregator', 'pom.xml')
    run_command(['mvn', '-f', dataflow_path, 'compile', 'exec:java',
                 '-Dexec.mainClass={}'.format(main_class),
                 '-Dexec.args=\"{}\"'.format(' '.join(args)),
                 '-Pdataflow-runner'])


def __dataflow_job_from_template(project, job_name, dataflow_bucket):
    job = __get_active_job_by_name(project, job_name)

    if job:
        old_job_name = job_name
        job_name = '{}_1'.format(job_name)
        print('Job {} already exists in this project {}.'
              .format(old_job_name, project))
        __cancel_job(project, job[0]['id'])
        print('Changing job name to {}'.format(job_name))

    print('Creating job named {}'.format(job_name))
    template_path = '{}/templates/DataflowJobTemplate'.format(dataflow_bucket)
    run_command(['gcloud', 'dataflow', 'jobs', 'run', job_name,
                 '--gcs-location', template_path,
                 '--project', project])


def __cancel_job(project, job_id):
    print('Canceling job with id {}'.format(job_id))
    run_command(['gcloud', 'dataflow', 'jobs', 'cancel', job_id,
                 '--project', project])


def __get_active_job_by_name(project, job_name):
    active_jobs = run_command(['gcloud', 'dataflow', 'jobs', 'list',
                               '--status=active', '--project', project,
                               '--format=json',
                               '--filter=name={}'.format(job_name)])

    if active_jobs:
        active_jobs = json.loads(active_jobs.decode("utf-8").strip())

    return active_jobs


def __grant_roles(infra_dm_name, project):
    with instruction_separator('Role to sa created by sink to publish.', action='Granting'):
        outputs = run_command_readonly([
            'gcloud', 'deployment-manager', 'manifests', 'describe',
            '--deployment', infra_dm_name,
            '--project', project,
            '--format', 'value(layout)'
        ])
        accounts = SINK_SA_REGEX.findall(outputs.decode("utf-8").strip())
        if accounts:
            sink_publisher_role = os.path.join(
                helpers.BASE_DIR, 'setup', 'roles', 'sink_publisher.txt')
            for account in accounts:
                grant_roles_on_project(
                    sink_publisher_role,
                    project,
                    account
                )


def __application_creation(cf_bucket_name, infra_dm_name, organization_id, project, location, scc_api_key, audit_logs_source_id, binary_authorization_source_id):
    with instruction_separator('Aplication.'):
        if not deployment_exists(project, infra_dm_name):
            # store converter function in bucket
            zip_and_store_cf('log-single-converter', 'log-single-converter.zip', 'gs://' + cf_bucket_name)

            # store sender function in bucket
            zip_and_store_cf('finding-scc-writer', 'finding-scc-writer.zip', 'gs://' + cf_bucket_name)

            infra_template = os.path.join(helpers.BASE_DIR, 'dm', 'infra.py')
            cmd = [
                'gcloud', 'deployment-manager', 'deployments', 'create',
                infra_dm_name,
                '--template', infra_template,
                '--properties',
                ",".join([
                    'region:' + scape_to_os(location),
                    'cfbucket:' + cf_bucket_name,
                    'organization_id:' + scape_to_os(organization_id),
                    'scc_api_key:' + scape_to_os(scc_api_key),
                    'audit_logs_source_id:' + scape_to_os(audit_logs_source_id),
                    'binary_authorization_source_id:' + scape_to_os(binary_authorization_source_id)
                ]),
                '--project', project
            ]
            run_command(cmd)


def __cloud_function_bucket(cf_bucket_name, project, location):
    with instruction_separator('Cloud function bucket.'):
        cf_bucket_status = bucket_status(cf_bucket_name)
        if "NotFound" == cf_bucket_status:
            bucket_template = os.path.join(
                helpers.BASE_DIR, 'dm', 'bucket.py')
            cmd = [
                'gcloud', 'deployment-manager', 'deployments', 'create',
                '-'.join(['bucket', project,
                          datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
                '--template', bucket_template,
                '--properties',
                ",".join([
                    'location:' + scape_to_os(location),
                    'bucketname:' + cf_bucket_name,
                    'storageClass:' + "REGIONAL"
                ]),
                '--project', project
            ]
            run_command(cmd)


def __validate_project(project):
    if not project_exists(project):
        click.echo(('Project {} not found. Please check if id is correct or if '
                    'you have been granted access to it.'.format(project)))
        sys.exit(2)


if __name__ == '__main__':
    __run_steps()
