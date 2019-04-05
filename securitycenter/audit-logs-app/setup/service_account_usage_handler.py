import shlex
import subprocess

from base import green_print, log_exception, normalize_cli_command, is_windows

from contextlib import contextmanager


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


@contextmanager
def service_account_wall():
    """" context manager to print simulate mode message """
    use_service_account_disclaimer()
    try:
        with log_exception():
            yield
    finally:
        use_service_account_disclaimer()


def use_service_account_disclaimer():
    green_print("*************************************************")
    green_print("* This script runs using the service account    *")
    green_print("* provided in the key file. It executes         *")
    green_print("* gcloud auth activate-service-account \        *")
    green_print("* --key-file=<your-key-file>                    *")
    green_print("* so that all gcloud commands that are executed *")
    green_print("* are executed with this service account.       *")
    green_print("*                                               *")
    green_print("* After execution please run:                   *")
    green_print("* gcloud auth list                              *")
    green_print("* to list the current accounts and run:         *")
    green_print("* gcloud config set account `YOUR-ACCOUNT`      *")
    green_print("* to set your account back as the active one.   *")
    green_print("*************************************************")
