"""Common methods used on click python scripts"""

import inspect
import json
import os
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime

import click

import helpers
from base import LOGGER


@contextmanager
def instruction_separator(step, action="Creating"):
    """Add a message at the start and end of the log messages of the step"""
    click.echo()
    click.secho('{:-^60}'.format(("{0} {1}".format(action, step)), bold=True))
    try:
        yield
        click.secho('{:-^60}'
                    .format(("{0} finished successfully".format(step))),
                    fg='green')
    except Exception:  # pylint: disable=W0703
        LOGGER.exception("error")
        click.secho('{:-^60}'
                    .format(("Problem {0} {1}".format(action, step))),
                    err=True, fg='red')


def parse_args(input_file):
    """Parse json input and return as object"""
    try:
        response_input = parse_input_json(input_file)
        click.echo("Input file read from [{0}]".format(input_file))
        return response_input
    except FileNotFoundError as not_found:
        click.echo("File [{0}] not found.".format(not_found.filename))
    except json.decoder.JSONDecodeError as err:
        click.echo("Error parsing file [{0}].\n{1}"
                   .format(input_file, err))


def parse_input_json(input_file):
    """ Parse input json """
    with open(input_file, 'r', encoding='utf-8') as infile:
        return json.loads(
            infile.read(),
            object_hook=lambda d: namedtuple('QB', d.keys())(*d.values())
        )


def configure_helpers(simulation, base_dir_reference=None):
    """
    setup helper variables
    :param simulation: whether or not to run the scripts in simulation mode
    :param base_dir_reference: can change base_dir reference, e.g. use '..' to set your base dir to the upper level
    :return:
    """
    helpers.START_TIME = datetime.utcnow().strftime('%Y%m%d%H%M')
    helpers.DRY_RUN = simulation
    set_base_dir(base_dir_reference)


def set_base_dir(reference=None):
    """
    Set base dir path used for scripts execution
    :param reference: can change base_dir reference. P.e. use '..' to set your base dir to the upper level
    :return:
    """
    helpers.BASE_DIR = os.path.join(os.path.dirname(
        os.path.abspath(inspect.stack()[0][1])))
    if reference:
        helpers.BASE_DIR = os.path.join(helpers.BASE_DIR, reference)
