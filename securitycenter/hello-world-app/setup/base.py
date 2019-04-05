import subprocess
import platform

import sys
import os

import helpers
import shlex


def run_command(parameters):
    '''Run a command'''
    parameters = normalize_cli_command(parameters)
    cmd = " ".join(parameters)
    print(cmd)
    if not helpers.DRY_RUN:
        return subprocess.check_output(shlex.split(cmd, posix=(not is_windows())))


def run_command_readonly(parameters):
    '''Run a readonly command'''
    parameters = normalize_cli_command(parameters)
    cmd = " ".join(parameters)
    if ('list' in parameters) or ('ls' in parameters) or ('describe' in parameters):
        print(cmd)
        try:
            subprocess_check_output = subprocess.check_output(
                shlex.split(
                    cmd,
                    posix=(not is_windows())),
                stderr=subprocess.STDOUT)
            return subprocess_check_output
        except subprocess.CalledProcessError as call_error:
            return call_error.output
    print('Invalid usage of run_command_readonly: ' + cmd)
    sys.exit(99)


def is_windows():
    '''Verify if the platform is windows'''
    return platform.system().upper() == "WINDOWS"


def get_sdk_path():
    if is_windows():
        return os.popen('where gcloud.cmd 2>/dev/null').read().replace("\\\\bin\\\\gcloud.cmd", "")
    else:
        return os.popen('which gcloud 2>/dev/null').read().replace("/bin/gcloud", "")


def scape_to_os(value):
    '''Escape value using OS quotes'''
    if is_windows():
        return '\'' + value + '\''
    else:
        return '\\\'' + value + '\\\''


def get_gcloud_command():
    """Choose correct executable to run google cloud platform CLI."""
    return 'gcloud.cmd' if is_windows() else 'gcloud'


def get_gsutil_command():
    """Choose correct executable to run google cloud gsutil platform CLI."""
    return 'gsutil.cmd' if is_windows() else 'gsutil'


def normalize_cli_command(parameters):
    '''Normalize CLI command to work on posix / windows'''
    if len(parameters) > 0 and parameters[0] == 'gcloud':
        parameters[0] = get_gcloud_command()
    if len(parameters) > 0 and parameters[0] == 'gsutil':
        parameters[0] = get_gsutil_command()
    return parameters
