""" compute utilities methods """

from contextlib import contextmanager

from .base import LOGGER, log_exception, run_command


@contextmanager
def gce_machine(dns_project_id, compute_zone, ssl_external_ip):
    try:
        create_new_machine(dns_project_id, compute_zone, ssl_external_ip)
        yield
    finally:
        delete_machine(dns_project_id, compute_zone)


def create_new_machine(dns_project_id, compute_zone, ssl_external_ip):
    with log_exception():
        LOGGER.info("Creating new machine")
        cmd = [
            'gcloud', 'compute', 'instances', 'create', 'ssl-certificate-gen',
            '--image-family', 'cos-stable',
            '--image-project', 'cos-cloud',
            '--zone', compute_zone,
            '--tags', 'http-server,https-server',
            '--address', ssl_external_ip,
            "--machine-type", "n1-standard-1",
            "--project", dns_project_id,
            '-q'
        ]
        run_command(cmd)


def delete_machine(dns_project_id, compute_zone):
    LOGGER.info("Deleting machine")
    cmd = [
        "gcloud", "compute", "instances", "delete",
        "ssl-certificate-gen",
        "--zone", compute_zone,
        "--project", dns_project_id,
        "-q"
    ]
    run_command(cmd)
