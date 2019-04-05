import base
import helpers
import os
from shutil import copy2
import logger


def copy_files(from_path, to_path):
    print('Copying file "{}" to "{}"'.format(from_path, to_path))
    copy2(from_path, to_path)


def copy_service_account(sa_file, dst_sa_path, dst_sa_file_name):
    print('Coping service account.')
    if not os.path.exists(dst_sa_path):
        os.makedirs(dst_sa_path)
    dst_sa_file = os.path.join(
        dst_sa_path,
        dst_sa_file_name
    )
    copy_files(sa_file, dst_sa_file)


def get_project_number(project_id):
    project_number = base.run_command([
        'gcloud', 'projects', 'describe', project_id,
        '--format', 'value(projectNumber)'
    ])
    if helpers.DRY_RUN:
        return "123456789"
    else:
        return project_number.decode("utf-8").strip()


def get_service_account_email(sa_name, project_id):
    account_email = base.run_command([
        'gcloud', 'iam', 'service-accounts', 'list',
        '--project', project_id,
        '--filter', sa_name,
        '--format', 'value(email)'
    ])
    if helpers.DRY_RUN:
        return "creator@project_id.iam.gserviceaccount.com"
    else:
        return account_email.decode("utf-8").strip()


def get_cloud_services_default_service_account(project_id):
    project_number = get_project_number(project_id)
    return project_number + '@cloudservices.gserviceaccount.com'


def get_compute_engine_default_service_account(project_id):
    project_number = get_project_number(project_id)
    return project_number + '-compute@developer.gserviceaccount.com'


def upload_to_bucket(local_path, bucket_path):
    base.run_command([
        'gsutil', 'cp', local_path, bucket_path
    ])


def project_exists(project_id):
    result_ = base.run_command_readonly([
        'gcloud', 'projects', 'list',
        '--filter', 'PROJECT_ID=' + project_id,
        '--format', 'json'
    ])
    return result_.decode("utf-8").strip() != '[]'


def has_file(file_):
    return os.path.isfile(file_)


def bucket_status(bucket_name):
    result_ = base.run_command_readonly([
        'gsutil', 'ls', '-L', '-b',
        'gs://' + bucket_name
    ])
    clean_result = result_.decode("utf-8").strip()
    if "BucketNotFoundException" in clean_result:
        return "NotFound"
    if "AccessDeniedException" in clean_result:
        return "AccessDenied"
    return "Found"


def deployment_exists(project_name, deployment_name):
    result_ = base.run_command_readonly([
        'gcloud', 'deployment-manager', 'deployments', 'list',
        '--filter', 'NAME=' + deployment_name,
        '--format', 'json',
        '--project', project_name
    ])
    return result_.decode("utf-8").strip() != '[]'


def use_service_account(key_file):
    '''activate service account'''
    use_service_account_disclaimer()
    base.run_command([
        'gcloud', 'auth', 'activate-service-account',
        '--key-file=' + key_file
    ])


def subscription_exists(project_name, subscription_name):
    subscription = 'projects/{}/subscriptions/{}'.format(project_name, subscription_name)
    result_ = base.run_command_readonly([
        'gcloud', 'pubsub', 'subscriptions', 'describe', subscription
    ])
    return result_.decode("utf-8").strip().__contains__(subscription)


def sink_exists(organization, sink_name):
    result_ = base.run_command_readonly([
        'gcloud', 'logging', 'sinks', 'describe', sink_name,
        '--organization', organization
    ])
    return not result_.decode("utf-8").strip().__contains__('NOT_FOUND: Sink {} does not exist'.format(sink_name))


def topic_exists(project_name, topic_name):
    topic = 'projects/{}/topics/{}'.format(project_name, topic_name)
    result_ = base.run_command_readonly([
        'gcloud', 'pubsub', 'topics', 'describe', topic
    ])
    return result_.decode("utf-8").strip().__contains__(topic)


def print_disclaimer(title, disclaimer):
    logger.print_in_color(logger.SOLARIZED, '\n === {:=<75}'.format(title.upper() + ' '))
    logger.print_in_color(logger.SOLARIZED, '  ' + disclaimer.replace('\n', '\n  '))
    logger.print_in_color(logger.SOLARIZED, ' {:-<79}\n'.format(''))


def simulation_mode_disclaimer():
    if helpers.DRY_RUN:
        disclaimer_text = 'Running in simulation mode. The gcloud commands will be printed but NOT'
        disclaimer_text += '\nexecuted. Check the README for more information.'
        print_disclaimer('simulation', disclaimer_text)


def use_service_account_disclaimer():
    disclaimer_text = 'This script runs using the service account provided in the key file.'
    disclaimer_text += '\nCheck the README for more information.'
    print_disclaimer('service account', disclaimer_text)
