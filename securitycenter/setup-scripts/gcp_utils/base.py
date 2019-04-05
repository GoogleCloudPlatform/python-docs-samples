""""Base methods"""

import logging
import platform
import shlex
import subprocess
import sys
from contextlib import contextmanager

import helpers

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# create a file handler
HANDLER = logging.FileHandler('base.log')

# create a logging format
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)

# add the handlers to the LOGGER
LOGGER.addHandler(HANDLER)

if helpers.DEBUG:
    LOGGER.setLevel(logging.DEBUG)
    HANDLER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)
    HANDLER.setLevel(logging.INFO)

@contextmanager
def log_exception():
    """ Quietly yield logging exception """
    try:
        yield
    except Exception as err:  # pylint: disable=W0703
        LOGGER.error(err)


def run_command(parameters):
    """Run a command"""
    parameters = normalize_cli_command(parameters)
    cmd = " ".join(parameters)
    LOGGER.info(cmd)
    if not helpers.DRY_RUN:
        if is_windows():
            args_ = cmd
        else:
            args_ = shlex.split(cmd)
        ret = subprocess.check_output(args_)
        LOGGER.debug(ret.decode("utf-8"))
        return ret


def run_command_readonly(parameters):
    """
    Run a readonly command.
    The command will be executed even in simulation mode
    :param parameters: an array that represents the command to be executed
    :return:
    """
    parameters = normalize_cli_command(parameters)
    cmd = " ".join(parameters)
    if 'list' in parameters or 'get-iam-policy' in parameters or \
            'get-server-config' in parameters or \
            'describe' in parameters:
        LOGGER.info(cmd)
        if is_windows():
            args_ = cmd
        else:
            args_ = shlex.split(cmd)
        ret = subprocess.check_output(args_)
        LOGGER.debug(ret.decode("utf-8"))
        return ret
    LOGGER.error('Invalid usage of run_command_readonly %s', cmd)
    sys.exit(99)


def is_windows():
    """Verify if the platform is windows"""
    return platform.system().upper() == "WINDOWS"


def scape_to_os(value):
    """Escape value using OS quotes"""
    if is_windows():
        return '\'' + value + '\''

    return '\\\'' + value + '\\\''


def get_gcloud_command():
    """Choose correct executable to run google cloud platform CLI."""
    return 'gcloud.cmd' if is_windows() else 'gcloud'


def get_gsutil_command():
    """Choose correct executable to run google cloud gsutil platform CLI."""
    return 'gsutil.cmd' if is_windows() else 'gsutil'


def get_kubectl_command():
    return 'kubectl.cmd' if is_windows() else 'kubectl'


def normalize_cli_command(parameters):
    """Normalize CLI command to work on posix / windows"""
    if parameters:
        options = {
            'gcloud':  get_gcloud_command,
            'gsutil': get_gsutil_command,
            'kubectl': get_kubectl_command
        }

        parameters[0] = options.get(parameters[0], lambda: parameters[0])()
    return parameters
