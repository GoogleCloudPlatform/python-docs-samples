import os


def is_production_environment():
    return os.getenv('APP_ENV', '') == 'production'


def get_organization_id():
    return str(os.getenv('organization_id'))


def get_organization_display_name():
    return os.getenv('organization_display_name')


def get_organization_uri():
    return "organizations/{}".format(get_organization_id())


def get_default_notification_topic():
    return os.getenv('NOTIFICATION_TOPIC')


def get_project_id():
    return os.getenv('project_id')
