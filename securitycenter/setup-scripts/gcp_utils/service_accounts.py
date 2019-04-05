import base
import re
import json


def use_service_account(key_file):
    """activate service account"""
    base.run_command([
        'gcloud', 'auth', 'activate-service-account',
        '--key-file=' + key_file
    ])


def get_policies_organization(organization_id):
    result = base.run_command_readonly([
        'gcloud', 'organizations', 'get-iam-policy', organization_id,
        '--format', 'json'
    ])
    return json.loads(result.decode("utf-8"))


def get_policies_project(project_id):
    result = base.run_command_readonly([
        'gcloud', 'projects', 'get-iam-policy', project_id,
        '--format', 'json'
    ])
    return json.loads(result.decode("utf-8"))


def remove_from_police(member, policies):
    for policy in policies["bindings"]:
        if member in policy["members"]:
            policy["members"].remove(member)
    return policies


def add_member_to_police(member, role, policies):
    if check_if_role_exists(role, policies):
        for policy in policies["bindings"]:
            if policy["role"] == role:
                policy["members"].append(member)
    else:
        policies = add_role_to_police(member, role, policies)
    return policies


def check_if_role_exists(role, policies):
    for policy in policies["bindings"]:
        if policy["role"] == role:
            return True
    return False


def add_role_to_police(member, role, policies):
    pattern = {'members': [], 'role': ''}
    pattern["members"].append(member)
    pattern["role"] = role
    policies["bindings"].append(pattern)
    return policies


def set_police_on_organization(organization_id, file):
    base.run_command([
        'gcloud', 'organizations',
        'set-iam-policy', organization_id, file
    ])


def set_police_on_project(project_id, file):
    base.run_command([
        'gcloud', 'projects',
        'set-iam-policy', project_id, file
    ])


def get_project_name(service_account):
    regex = "@([^.]+)"
    return re.search(regex, service_account).group(1)


def get_project_number(service_account):
    regex = "([0-9]*)([^@]+)"
    return re.search(regex, service_account).group(1)