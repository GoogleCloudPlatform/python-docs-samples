import os


def get_namespace():
    return os.getenv('CREATOR_NAMESPACE', 'scccreator')


def get_current_organization(full_path=False):
    if full_path:
        return "organizations/" + str(os.getenv('organization_id'))
    else:
        return str(os.getenv('organization_id'))


def get_organization_id():
    return str(os.getenv('organization_id'))


def get_organization_display_name():
    return os.getenv('organization_display_name')


def get_sa_file_name():
    return os.getenv('CSCC_SA_CLIENT_FILE', 'accounts/cscc_api_client.json')


def get_pubsub_token():
    return os.getenv('PUBSUB_VERIFICATION_TOKEN')


def get_project_id():
    return os.getenv('project_id')
