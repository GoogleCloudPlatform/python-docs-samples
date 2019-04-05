"""
Common gcp methods regarding projects
This module should be extracted to a gcp_utils folder on file projects.py
"""

from base import run_command_readonly


def gcp_project_exists(project_id):
    """Validate if given project id exists on GCP and user has access"""
    cmd = [
        'gcloud', 'projects', 'list',
        '--filter', 'PROJECT_ID=' + project_id,
        '--format', 'json'
    ]
    result = run_command_readonly(cmd).decode('utf8').strip()

    return result != '[]'


