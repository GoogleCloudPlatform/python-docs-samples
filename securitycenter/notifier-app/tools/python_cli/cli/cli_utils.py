"""CLI utility functions."""
import codecs


def read_file(userfile, encoding="UTF-8"):
    """Read a file respecting the encoding.

    Params:
    filepath
    encoding defaults to UTF-8
    """
    with codecs.open(userfile, "r", encoding=encoding) as openedfile:
        return openedfile.read()


def setup_api_instance(client, api_endpoints_url, token):
    """Set up an Api client instance with the required configuration info."""
    client.configuration.host = api_endpoints_url
    client.configuration.access_token = token
    return client.DefaultApi()
