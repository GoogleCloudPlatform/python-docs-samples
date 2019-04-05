"""
Common gcp methods regarding regions
This module should be extracted to a gcp_utils folder on file regions.py
"""
from base import run_command_readonly


def get_region_by_zone(zone):
    """Get the region based on specified zone"""
    cmd = [
        'gcloud', 'compute', 'zones', 'describe', zone,
        '--format=value(region)'
    ]
    region_url = str(run_command_readonly(cmd).decode('utf-8')).split('/')
    return region_url[len(region_url) - 1].replace('\n', '')
