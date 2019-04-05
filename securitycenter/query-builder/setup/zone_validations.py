"""
Common gcp methods regarding zones
This module should be extracted to a gcp_utils folder on file zones.py
"""

from base import run_command_readonly


def gcp_zone_list(project_id):
    """Validate if given project id exists on GCP and user has access"""
    cmd = [
        'gcloud', 'compute', 'zones', 'list',
        '--format="value(NAME)"',
        '--project', project_id
    ]
    result = run_command_readonly(cmd).decode('utf8').strip()

    return result


def get_managed_zones_by_project(project_id):
    """Get managed zones for the given project id"""
    cmd = [
        'gcloud', 'dns', 'managed-zones', 'list',
        '--project', project_id,
        '--format=value(name)'
    ]
    result = run_command_readonly(cmd).decode('utf8').strip()

    return result