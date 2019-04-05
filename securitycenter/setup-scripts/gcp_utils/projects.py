
import json
import re

import helpers
from base import run_command, run_command_readonly, LOGGER


def has_access_to_project(project_id):
    result_ = run_command_readonly([
        'gcloud', 'projects', 'list',
        '--filter', 'project_id:{}'.format(project_id),
        '--format', 'json'
    ])
    return result_.decode("utf-8").strip() != '[]'


def enable_service_on_project(dns_project_id, service_url):
    LOGGER.info(
        "Enabling {} on project {}".format(service_url, dns_project_id)
    )
    run_command([
        'gcloud', 'services', 'enable', service_url,
        '--project', dns_project_id
    ])


def check_project_exists(project_name, project_number, project_list):
    if not helpers.DRY_RUN:
        for item in project_list:
            if (item["projectId"] == project_name
                    or item["projectNumber"] == project_number):
                return True
    return True


def return_get_projects_command(organization_id, folder_id,
                                format_='--format=\'value(projectId)\''):

    filtered_parents = [x for x in [organization_id, folder_id] if x != '']
    return [
        'gcloud', 'projects', 'list',
        '--filter=\'parent.id=({})\''.format(",".join(filtered_parents)),
        format_
    ]


def find_folder_id(project_suffix, organization_id):
    filter_ = ""
    if project_suffix:
        filter_ = "--filter=\'displayName:{}\'".format(project_suffix)
    folder_id = run_command([
        'gcloud', 'alpha', 'resource-manager', 'folders', 'list',
        '--organization', organization_id,
        filter_,
        "--format=\'value(ID)\'"
    ])
    if helpers.DRY_RUN:
        folder_id = "734300135241"
    else:
        folder_id = folder_id.decode("utf-8").strip()
    return folder_id


def get_json_list_projects(project_prefix, project_suffix, organization_id):
    result = run_command(
        return_get_projects_command(organization_id,
                                    find_folder_id(project_suffix,
                                                   organization_id),
                                    "--format='json()'"))

    if not helpers.DRY_RUN:
        json_result = json.loads(result.decode("utf-8"))
        project_pattern = re.compile(
            r"\A{}.*{}\Z".format(project_prefix, project_suffix))

        for item in json_result:
            if not project_pattern.match(item["projectId"]):
                json_result.pop(item)

        return json_result