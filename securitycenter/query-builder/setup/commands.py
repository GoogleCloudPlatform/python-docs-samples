""" utilities commands on gcloud """

import json
import os
import subprocess

import jinja2

import base
import helpers


def cluster_exists(cluster_name, project):
    command_ = [
        'gcloud', 'container', 'clusters', 'list',
        '--filter', 'NAME=' + cluster_name,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def static_ip_exists(static_ip, project):
    command_ = [
        'gcloud', 'compute', 'addresses', 'list',
        '--filter', 'NAME=' + static_ip,
        '--project', project,
        '--format', 'json'
    ]
    return get_command_result(command_)


def bucket_exists(bucket_name):
    cmd = [
        'gsutil', 'ls',
        'gs://' + bucket_name
    ]
    try:
        base.run_command(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def get_command_result(command_):
    result_ = base.run_command_readonly(command_)
    return result_.decode("utf-8").strip() != '[]'


def get_project_number(project_id):
    command_ = [
        "gcloud", "projects", "describe", project_id,
        "--format", "value(projectNumber)"
    ]
    return base.run_command_readonly(command_).decode("utf-8").strip()


def create_file_from_template(template_file_name, context, output_file_name):
    path = os.path.join(helpers.BASE_DIR)
    template_loader = jinja2.FileSystemLoader(searchpath=path)
    template_env = jinja2.Environment(loader=template_loader)    
    template = template_env.get_template(template_file_name)
    output_text = template.render(context)

    with open(output_file_name, 'w') as outfile:
        outfile.write(output_text)


def get_json_content(json_file):
    with open(json_file) as f:
        return json.load(f)
