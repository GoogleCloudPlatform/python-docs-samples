import os
from datetime import datetime

import helpers
from base import run_command, scape_to_os
from commands import (
    bucket_status,
    gae_exists,
    gae_service_exist,
    bucket_notification_exists,
    deployment_exists,
    choose_translation_mapper,
    update_mapper_file_org_id)
from update_cloud_function import zip_and_store_cf


def main_connector(args):
    # validate need to choose translation mapper
    if not args.quiet:
        mapper_file = choose_translation_mapper()
        update_mapper_file_org_id(args.organization_id, mapper_file)

    connector_project_id = args.connector_project
    print('connector - partner bucket creation.')
    partner_bucket_name = args.connector_bucket
    partner_bucket_status = bucket_status(partner_bucket_name)
    if "NotFound" == partner_bucket_status:
        bucket_template = os.path.join(
            helpers.BASE_DIR, 'connector', 'dm', 'bucket.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            '-'.join(['bucket-for-partner',
                      datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
            '--template', bucket_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'bucketname:' + partner_bucket_name,
            ]),
            '--project', connector_project_id]
        run_command(cmd)
    print('connector - cloud function bucket creation.')
    cf_bucket_name = args.cf_bucket
    cf_bucket_status = bucket_status(cf_bucket_name)
    if "NotFound" == cf_bucket_status:
        bucket_template = os.path.join(
            helpers.BASE_DIR, 'connector', 'dm', 'bucket.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            '-'.join(['bucket-for-cf',
                      datetime.utcnow().strftime('%Y%m%d%H%M%S')]),
            '--template', bucket_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'bucketname:' + cf_bucket_name,
            ]),
            '--project', connector_project_id]
        run_command(cmd)
    print('connector - connector application creation.')
    infra_dm_name = 'infra-for-partner'
    if not deployment_exists(connector_project_id, infra_dm_name):
        zip_and_store_cf('forwardfilelink',
                         'forwardfilelink.zip', 'gs://' + cf_bucket_name)
        zip_and_store_cf('flushbuffer', 'flushbuffer.zip',
                         'gs://' + cf_bucket_name)
        zip_and_store_cf('configuration', 'configuration.zip',
                         'gs://' + cf_bucket_name)
        zip_and_store_cf('translation', 'translation.zip',
                         'gs://' + cf_bucket_name, translation_sa=args.connector_sa_file)
        zip_and_store_cf('cleanup', 'cleanup.zip',
                         'gs://' + cf_bucket_name)

        infra_template = os.path.join(
            helpers.BASE_DIR, 'connector', 'dm', 'writeFindingsConnectorInfra.py')
        cmd = [
            'gcloud', 'deployment-manager', 'deployments', 'create',
            infra_dm_name,
            '--template', infra_template,
            '--properties',
            ",".join([
                'region:' + scape_to_os(args.region),
                'cfbucket:' + cf_bucket_name,
            ]),
            '--project', connector_project_id]
        run_command(cmd)
    if not gae_exists(connector_project_id):
        print('Enable Google App Engine.')
        cmd = [
            'gcloud', 'app', 'create',
            '--region', args.gae_region,
            '--project', connector_project_id]
        run_command(cmd)
    if not gae_service_exist(connector_project_id, 'default'):
        print('Deploy blank GAE app to activate Datastore.')
        cmd = [
            'gcloud', 'app', 'deploy',
            os.path.join(helpers.BASE_DIR, 'connector', 'gae_app', 'app.yaml'),
            '--quiet',
            '--project', connector_project_id]
        run_command(cmd)
    print('connector - connector application turn on bucket notifications.')
    if not bucket_notification_exists(partner_bucket_name):
        cmd = [
            'gsutil', 'notification',
            'create',
            '-e', 'OBJECT_FINALIZE',
            '-t', 'projects/' + connector_project_id + '/topics/forwardfilelink',
            '-f', 'json',
            'gs://' + partner_bucket_name]
        run_command(cmd)
