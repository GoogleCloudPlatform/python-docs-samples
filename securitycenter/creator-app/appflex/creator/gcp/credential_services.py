from google.oauth2 import service_account as sa

from creator.config_service import get_sa_file_name

GCP_ALL_SCOPES = 'https://www.googleapis.com/auth/cloud-platform'


def get_credential_from_file():
    credentials = sa.Credentials.from_service_account_file(get_sa_file_name())
    return credentials.with_scopes([GCP_ALL_SCOPES])
