import shlex
import subprocess

from base import green_print, log_exception, normalize_cli_command, is_windows

from contextlib import contextmanager

from validator_handler import validate_out_of_scope_service_account


def use_service_account(key_file):
    """activate service account even in DRY_RUN."""
    parameters = [
        'gcloud', 'auth', 'activate-service-account',
        '--key-file=' + key_file
    ]
    cmd = " ".join(normalize_cli_command(parameters))
    if is_windows():
        args_ = cmd
    else:
        args_ = shlex.split(cmd)
    print(cmd)
    subprocess.check_output(args_)


def validate_service_account_to_use(key_file):
    validate_out_of_scope_service_account(
        key_file,
        'deployer service account: {}'.format(key_file))
