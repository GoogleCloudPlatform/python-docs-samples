import argparse

# [START storage_signed_url_dependencies]
import collections
import datetime
import hashlib
import json
import sys

# pip install six
from six.moves.urllib.parse import quote

# pip install google-auth
from google.oauth2 import service_account
# [END storage_signed_url_dependencies]

def create_signed_url(service_account_file, bucket_name, object_name,
    expiration, http_method='GET', query_parameters=None, headers=None):

    if expiration > 604800:
        print('Expiration time can\'t be longer than a week')
        sys.exit(1)

    # [START storage_signed_url_canonical_uri]
    escaped_object_name = quote(object_name, safe='')
    canonical_uri = "/{}/{}".format(bucket_name, escaped_object_name)
    # [END storage_signed_url_canonical_uri]

    # [START storage_signed_url_canonical_datetime]
    datetime_now = datetime.datetime.utcnow()
    request_timestamp = datetime_now.strftime("%Y%m%dT%H%M%SZ")
    datestamp = datetime_now.strftime("%Y%m%d")
    # [END storage_signed_url_canonical_datetime]

    # [START storage_signed_url_credentials]
    google_credentials = service_account.Credentials.from_service_account_file(service_account_file)
    client_email = google_credentials.service_account_email
    credential_scope = "{}/auto/gcs/goog4_request".format(datestamp)
    credential = "{}/{}".format(client_email, credential_scope)
    # [END storage_signed_url_credentials]

    if headers is None:
        headers = dict()
    # [START storage_signed_url_canonical_headers]
    headers['host'] = "storage.googleapis.com"

    canonical_headers = ""
    ordered_headers = collections.OrderedDict(sorted(headers.items()))
    for k,v in ordered_headers.items():
        lower_k = str(k).lower()
        strip_v = str(v).lower()
        canonical_headers += "{}:{}\n".format(lower_k, strip_v)
    # [END storage_signed_url_canonical_headers]

    # [START storage_signed_url_signed_headers]
    signed_headers = ""
    for k,_ in ordered_headers.items():
        lower_k = str(k).lower()
        signed_headers += "{};".format(lower_k)
    signed_headers = signed_headers[:-1] # remove trailing ';'
    # [END storage_signed_url_signed_headers]

    if query_parameters is None:
        query_parameters = dict()
    # [START storage_signed_url_canonical_query_parameters]
    query_parameters["X-Goog-Algorithm"] = "GOOG4-RSA-SHA256"
    query_parameters["X-Goog-Credential"] = credential
    query_parameters["X-Goog-Date"] = request_timestamp
    query_parameters["X-Goog-Expires"] = expiration
    query_parameters["X-Goog-SignedHeaders"] = signed_headers

    canonical_query_string = ""
    ordered_query_parameters = collections.OrderedDict(sorted(query_parameters.items()))
    for k,v in ordered_query_parameters.items():
        encoded_k = quote(str(k), safe='')
        encoded_v = quote(str(v), safe='')
        canonical_query_string += "{}={}&".format(encoded_k, encoded_v)
    canonical_query_string = canonical_query_string[:-1] # remove trailing ';'
    # [END storage_signed_url_canonical_query_parameters]

    # [START storage_signed_url_canonical_request]
    canonical_request = "\n".join([http_method,
        canonical_uri,
        canonical_query_string,
        canonical_headers,
        signed_headers,
        "UNSIGNED-PAYLOAD"])
    # [END storage_signed_url_canonical_request]

    # [START storage_signed_url_hash]
    canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()
    # [END storage_signed_url_hash]

    # [START storage_signed_url_string_to_sign]
    string_to_sign = "\n".join(["GOOG4-RSA-SHA256",
                      request_timestamp,
                      credential_scope,
                      canonical_request_hash])
    # [END storage_signed_url_string_to_sign]

    # [START storage_signed_url_signer]
    signature = google_credentials.signer.sign(string_to_sign).hex()
    # [END storage_signed_url_signer]

    # [START storage_signed_url_construction]
    signed_url = "https://storage.googleapis.com{}?{}&x-goog-signature={}".format(
        canonical_uri, canonical_query_string, signature)
    # [END storage_signed_url_construction]
    return signed_url

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description=__doc__,
    #     formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('service_account_file', help='Path to your Google service account.')
    # parser.add_argument('request_method', help='A request method, e.g GET, POST.')
    # parser.add_argument('bucket_name', help='Your Cloud Storage bucket name.')
    # parser.add_argument('object_name', help='Your Cloud Storage object name.')
    # parser.add_argument('expiration', help='Expiration Time.')

    # args = parser.parse_args()
    # signed_url = create_signed_url(
    #     service_account_file=args.service_account_file, request_method='GET',
    #     bucket_name=args.bucket_name, object_name=args.object_name,
    #     expiration=args.expiration)

    signed_url = create_signed_url(
        service_account_file="spec-test-ruby-samples-3fb0d39a74ab.json",
        bucket_name="jessefrank2", object_name="test_lifecycle.json",
        expiration=3600)
    print(signed_url)
