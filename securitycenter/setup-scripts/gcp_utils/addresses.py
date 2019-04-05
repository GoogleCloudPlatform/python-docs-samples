""" network addresses utilities methods """
from contextlib import contextmanager

from .base import LOGGER, run_command, run_command_readonly, log_exception

@contextmanager
def external_ip(dns_project_id, compute_region, name):
    try:
        create_external_address(dns_project_id, compute_region, name)
        yield
    finally:
        delete_addresses(dns_project_id, compute_region, name)


def delete_addresses(dns_project_id, compute_region, name):
    LOGGER.info("Deleting Adresses")
    cmd = [
        "gcloud", "compute", "addresses", "delete",
        name,
        "--region", compute_region,
        "--project", dns_project_id,
        "-q"
    ]
    run_command(cmd)


def create_external_address(dns_project_id, compute_region, name):
    with log_exception():
        LOGGER.info("Creating external region %s, project %s",
                    compute_region, dns_project_id)
        cmd = [
            'gcloud', 'compute', 'addresses',
            'create', name,
            '--region', compute_region,
            '--project', dns_project_id
        ]
        run_command(cmd)


def get_external_ip(dns_project_id, name):
    cmd = [
        'gcloud', 'compute', 'addresses', 'list',
        '--filter="name:{}"'.format(name),
        "--format='value(address)'",
        '--project', dns_project_id
    ]
    return run_command_readonly(cmd)\
           .decode("utf-8")\
           .replace("\r", "")\
           .replace("\n", "")
