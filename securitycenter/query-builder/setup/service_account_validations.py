"""
Common gcp methods regarding projects
This module should be extracted to a gcp_utils folder on file service_accounts.py
"""
import base


def service_account_exists(service_account_email, project):
    cmd = [
        'gcloud', 'iam', 'service-accounts', 'list',
        '--filter="email={}"'.format(service_account_email),
        '--project', project,
        '--format', 'json'
    ]
    result = base.run_command_readonly(cmd).decode('utf8').strip()
    return result != '[]'
