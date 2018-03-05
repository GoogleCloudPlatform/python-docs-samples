"""This application demonstrates how to perform operations on data (content)
when using the Google Cloud CDN (Content Delivery Network).

For more information, see the README.md under /cdn and the documentation
at https://cloud.google.com/cdn/docs.
"""

import argparse
import base64
<<<<<<< HEAD
import datetime
import hashlib
import hmac
import urlparse

def sign_url(url, key_name, key, expiration_time):
    """Gets the Signed URL string for the specified URL and configuration.

    Args:
        url: The URL to sign.
        key_name: Signed URL key name to use for the 'KeyName=' query parameter.
        key: The 16-byte unencoded secret key value to use for signing.
        expiration_time: expiration time expressed as a UTC datetime object.

    Returns:
        Returns the Signed URL appended with the query parameters based on the
        specified configuration.  Roughly of the form:
        {url}{separator}Expires={expiration}&KeyName={key_name}&Signature={signature}

    """
    stripped_url = url.strip()
    parsed_url = urlparse.urlsplit(stripped_url)
    query_params = urlparse.parse_qs(parsed_url.query, keep_blank_values=True)
    epoch = datetime.datetime.utcfromtimestamp(0)
    expiration_timestamp = (expiration_time - epoch).total_seconds()

    url_to_sign = '{url}{separator}Expires={expires}&KeyName={key_name}'.format(
            url=stripped_url,
            separator='&' if query_params else '?',
            expires=expiration_timestamp,
            key_name=key_name)

    signature = base64.urlsafe_b64encode(
            hmac.new(key, url_to_sign, hashlib.sha1).digest())

    return '{url}&Signature={signature}'.format(
            url=url_to_sign, signature=signature)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('sign-url', help=sign_url.__doc__)

    sign_url_parser = subparsers.add_parser('sign-url', help=sign_url.__doc__)
    sign_url_parser.add_argument('url',
            help="The URL to sign.")
    sign_url_parser.add_argument('key_name',
            help="Signed URL key name to use for the 'KeyName=' query parameter.")
    sign_url_parser.add_argument('key',
            help="The 16-byte unencoded secret key value to use for signing.")
    sign_url_parser.add_argument('expiration_timestamp',
            help="Expiration time expessed as seconds since the epoch.")

    args = parser.parse_args()

    args.url = "http://35.186.234.33/index.html"
    args.key_name = "my-key"
    args.key = base64.urlsafe_b64decode("nZtRohdNF9m3cKM24IcK4w==")

    if args.command == 'sign-url':
        expiration_time = datetime.datetime.fromtimestamp(float(args.expiration_timestamp))
        print sign_url(args.url, args.key_name, args.key, expiration_time)

