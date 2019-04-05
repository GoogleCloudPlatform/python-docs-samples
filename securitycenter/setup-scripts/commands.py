import base64
import codecs
import json
import os
from shutil import copy2

import jinja2

import base
import helpers
import logger
import yaml


def get_project_number(project_id):
    project_number = base.run_command([
        'gcloud', 'projects', 'describe', project_id,
        '--format', 'value(projectNumber)'
    ])
    if helpers.DRY_RUN:
        return "123456789"
    else:
        return project_number.decode("utf-8").strip()


def get_organization_display_name(org_id):
    display_name = base.run_command_readonly([
        'gcloud', 'organizations', 'describe', org_id,
        '--format', 'value(displayName)'
    ])
    return display_name.decode("utf-8").strip()


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


def subscription_exists(project_name, subscription_name):
    subscription = 'projects/{}/subscriptions/{}'.format(project_name, subscription_name)
    result_ = base.run_command_readonly([
        'gcloud', 'pubsub', 'subscriptions', 'describe', subscription
    ])
    return result_.decode("utf-8").strip().__contains__(subscription)


def topic_exists(project_name, topic_name):
    topic = 'projects/{}/topics/{}'.format(project_name, topic_name)
    result_ = base.run_command_readonly([
        'gcloud', 'pubsub', 'topics', 'describe', topic
    ])
    return result_.decode("utf-8").strip().__contains__(topic)


def gae_exists(project_name):
    if helpers.DRY_RUN:
        return False
    result_ = base.run_command_readonly([
        'gcloud', 'app', 'describe',
        '--project', project_name,
        '--format', 'json'
    ])
    clean_result = result_.decode("utf-8").strip()
    return 'does not contain an App Engine application' not in clean_result


def gae_service_exist(project_name, service_name):
    if helpers.DRY_RUN:
        return False
    result_ = base.run_command_readonly([
        'gcloud', 'app', 'services', 'describe', service_name,
        '--project', project_name,
        '--format', 'value(id)'
    ])
    clean_result = result_.decode("utf-8").strip()
    return service_name == clean_result


def bucket_notification_exists(bucket_name):
    result_ = base.run_command_readonly([
        'gsutil', 'notification', 'list',
        'gs://' + bucket_name
    ])
    clean_result = result_.decode("utf-8").strip()
    return clean_result != ""


def deployment_exists(project_name, deployment_name):
    result_ = base.run_command_readonly([
        'gcloud', 'deployment-manager', 'deployments', 'list',
        '--filter', 'NAME=' + deployment_name,
        '--format', 'json',
        '--project', project_name
    ])
    return result_.decode("utf-8").strip() != '[]'


def use_service_account(key_file):
    """activate service account"""
    use_service_account_disclaimer()
    base.run_command([
        'gcloud', 'auth', 'activate-service-account',
        '--key-file='+key_file])


def get_mapper_samples():
    """Choose the mapper used on translation cloud function."""
    samples_path = os.path.join(
        helpers.BASE_DIR, 'connector', 'dm', 'mapper_samples')
    samples = enumerate(os.scandir(samples_path), start=1)
    options = {}
    print('Enter the path of mapper to use on translation or choose one below.')
    for index, item in samples:
        print('[{}] {}'.format(index, item.path))
        options[index] = item.path

    mapper = options[1]
    while True:
        ans = input(
            'Please enter an index OR full path OR blank to choose the first one listed: ')
        if not ans:
            break
        if ans.isdigit():
            index = float(ans)
            if index in options.keys():
                mapper = options[index]
                break
            else:
                continue
        if os.path.isfile(ans):
            mapper = ans
            break

    return mapper


def get_properties_from_mapper(properties):
    mapper = get_mapper_samples()
    response = {}
    
    with codecs.open(mapper, "r", encoding="UTF-8") as openedfile:
        content = openedfile.read()
        stream = yaml.load(content)
        for prop in properties:
            response[prop] = stream[prop]

    return response


def choose_translation_mapper():
    mapper = get_mapper_samples()
    dstMapper = os.path.join(
        helpers.BASE_DIR,
        'connector',
        'dm',
        'function',
        'translation',
        'mapper.yaml'
    )
    print('Copying file "{}" to "{}"'.format(mapper, dstMapper))
    copy2(mapper, dstMapper)
    return dstMapper


def copy_files(from_path, to_path):
    print('Copying file "{}" to "{}"'.format(from_path, to_path))
    copy2(from_path, to_path)


def create_file_from_template(template_file_name, context, output_file_name):
    path = os.path.join(helpers.BASE_DIR, 'setup', 'templates')
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template_file_name)
    output_text = template.render(context)

    with open(output_file_name, 'w') as outfile:
        outfile.write(output_text)


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


def build_org_level_role_full_name(organization_id, role):
    return 'organizations/{}/roles/{}'.format(organization_id, role)


def iam_org_level_role_exist(organization_id, role):
    role_id_full_name = build_org_level_role_full_name(organization_id, role)
    current_role_name = base.run_command_readonly(
        ['gcloud', 'iam', 'roles', 'list',
         '--organization', organization_id,
         '--filter', role,
         '--format', "value(name)"]
    )
    return current_role_name.decode("utf-8").strip() == role_id_full_name


def update_mapper_file_org_id(organization_id, selected_mapper_file):
    with codecs.open(selected_mapper_file, "r", encoding="UTF-8") as openedfile:
        content = openedfile.read()
        stream = yaml.load(content)
        current_org_id = stream['org_name']
        org_id = 'organizations/{}'.format(organization_id)
        print('Changing organization id from "{}" to "{}"'.format(
            current_org_id, org_id))
        stream['org_name'] = org_id
        with codecs.open(selected_mapper_file, 'w', encoding="UTF-8") as output:
            yaml.dump(stream, output, default_flow_style=False)


def get_or_create_client_key(tool=None, key_name=None):
    """Get a client key to be used for validation."""
    key_file = os.path.expanduser(
        '~/.google_code_lab_{}_cloud_function_secret_client_key_{}'.format(tool, key_name))
    if not os.path.isfile(key_file):
        with open(key_file, 'wb') as f:
            f.write(base64.b64encode(os.urandom(42), altchars=b'ww'))
    return open(key_file).read().strip('\n')


def get_firewall_rules(project):
    firewall_rules = base.run_command_readonly([
        'gcloud', 'compute', 'firewall-rules', 'list',
        '--format=\'value(NAME)\'',
        '--project', project
    ])
    return firewall_rules.decode('utf-8').splitlines() if firewall_rules else []


def network_exists(network_name, project):
    result_ = base.run_command_readonly([
        'gcloud', 'compute', 'networks', 'list',
        '--filter ', 'name=' + network_name,
        '--project', project,
        '--format', 'json'
    ])
    return result_.decode("utf-8").strip() != '[]'


def save_json_file(path_file, data):
    output = open(path_file, "w")
    output.write(json.dumps(data, indent=4, sort_keys=True))
    output.close()


def link_billing(billing_account_id, project_id):
    print('Enabling billing for project {}.'.format(project_id))
    cmd = [
        'gcloud', 'beta', 'billing', 'projects', 'link', project_id,
        '--billing-account', billing_account_id
    ]
    base.run_command(cmd)


def project_has_billing(project_id):
    result = base.run_command_readonly(
        ['gcloud', 'beta', 'billing', 'projects', 'describe',
         project_id,
         '--format', 'value(billingEnabled)'])
    return 'TRUE' == result.decode("utf-8").strip().upper()
