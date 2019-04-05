""""Input validation methods"""

import logging
import os.path
from contextlib import contextmanager

import click

import helpers
from commands import get_json_content
from project_validations import (
    gcp_project_exists
)
from service_account_validations import service_account_exists
from zone_validations import gcp_zone_list, get_managed_zones_by_project

LOGGER = logging.getLogger(__name__)

CLOUD_SQL_USERNAME_MAX_LENGTH = 16

@contextmanager
def validation_separator(step):
    """
    Add a message at the start and end of the log messages of the step
    :param step: the step description
    :return:
    """
    click.echo()
    click.secho('{:-^60}'.format(("Validating {}".format(step))), bold=True)
    try:
        yield
        click.secho('{:-^60}'.format(("{} validated successfully".format(step))),
                    fg='green')
    except Exception as e:  # pylint: disable=W0703
        LOGGER.error(e)
        click.secho('{:-^60}'.format(("Problem validating {}".format(step))),
                    err=True, fg='red')
        if not helpers.DRY_RUN:
            raise


def validate_zone(zone, step_element_message, project_id):
    """Validate if given zone belongs to GCP zone list"""
    with validation_separator(step_element_message):
        gcp_zones = gcp_zone_list(project_id)
        if zone not in gcp_zones:
            raise ValueError(
                "The zone {} does not belong to GCP zones list".format(zone)
            )


def validate_project(project_id, step_element_message):
    """Validate if given project id exists on GCP and user has access"""
    with validation_separator(step_element_message):
        if not gcp_project_exists(project_id):
            raise ValueError(
                "The project {} does exist or the user does not have access to it".format(project_id)
            )


def validate_in_scope_service_account(project, service_account_file,
                                      step_element_message):
    """
    Validate if the given service account exists at given project and if the
    provided file is valid
    :param service_account_file: service account file path got from parameters
    :param step_element_message: describe elements that are being validated
    {sa_name}@{project}.iam.gserviceaccount.com
    :param project: project id
    :return:
    """
    with validation_separator(step_element_message):
        file_content = get_json_content(service_account_file)
        service_account_email = file_content['client_email']
        if not service_account_exists(service_account_email, project):
            raise ValueError(
                "The Service account {} does exist for the project {}".format(
                    service_account_email,
                    project
                )
            )


def validate_out_of_scope_service_account(service_account_file,
                                          step_element_message):
    """
    Validate if the service account JSON file is valid
    :param service_account_file: service account file path
    :param step_element_message: describe elements that are being validated
    :return:
    """
    with validation_separator(step_element_message):
        get_json_content(service_account_file)


def validate_file_exists(file_path, step_element_message):
    """Validate the given path is valid"""
    with validation_separator(step_element_message):
        if not os.path.isfile(file_path):
            raise ValueError(
                "The given file does not exists, please check the path: {}".format(file_path)
            )


def validate_dns_zone(dns_project, dns_zone, step_element_message):
    """Check if the given zone belongs to the dns project"""
    with validation_separator(step_element_message):
        zones = get_managed_zones_by_project(dns_project)
        if dns_zone not in zones:
            raise ValueError(
                "The managed zone {} does not exists in zone list for the project {}".format(
                    dns_zone,
                    dns_project
                )
            )


def validate_cloud_sql(cloud_sql, step_element_message):
    """Check if Cloud SQL properties are valid"""
    with validation_separator(step_element_message):
        db_username = cloud_sql.user_name
        if len(db_username) > CLOUD_SQL_USERNAME_MAX_LENGTH:
            raise ValueError("Cloud SQL username {} characters exceeds maximum allowed: {}"
                             .format(db_username, CLOUD_SQL_USERNAME_MAX_LENGTH))