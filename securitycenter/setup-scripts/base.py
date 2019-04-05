""""Base methods"""

import logging
import platform
import shlex
import subprocess

import sys
import os

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
    if 'list' in parameters \
            or 'get-iam-policy' in parameters \
            or 'ls' in parameters \
            or 'describe' in parameters \
            or 'get-server-config' in parameters:
        LOGGER.info(cmd)
        if is_windows():
            args_ = cmd
        else:
            args_ = shlex.split(cmd)
        try:
            ret = subprocess.check_output(args_, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as call_error:
            return call_error.output
        LOGGER.debug(ret.decode("utf-8"))
        return ret
    LOGGER.error('Invalid usage of run_command_readonly %s', cmd)
    sys.exit(99)


def is_windows():
    """Verify if the platform is windows"""
    return platform.system().upper() == "WINDOWS"


def get_sdk_path():
    if is_windows():
        return os.popen('where gcloud.cmd 2>/dev/null').read().replace("\\\\bin\\\\gcloud.cmd", "")
    else:
        return os.popen('which gcloud 2>/dev/null').read().replace("/bin/gcloud", "")


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
    """Choose correct executable to run kubectl."""
    return 'kubectl.cmd' if is_windows() else 'kubectl'


def get_maven_command():
    """Choose correct executable to run maven."""
    return 'mvn.cmd' if is_windows() else 'mvn'


def normalize_cli_command(parameters):
    """Normalize CLI command to work on posix / windows"""
    if parameters:
        options = {
            'gcloud':  get_gcloud_command,
            'gsutil': get_gsutil_command,
            'kubectl': get_kubectl_command,
            'mvn': get_maven_command
        }

        parameters[0] = options.get(parameters[0], lambda: parameters[0])()
    return parameters


def green_print(value):
    """ green print """
    print("\033[1;32;40m{}\033[0;0m".format(value))
