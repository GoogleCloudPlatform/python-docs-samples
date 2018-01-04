# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sample app that uses the Data Loss Prevent API to inspect a file on Google
Cloud Storage."""


from __future__ import print_function

import argparse


# [START inspect_gcs_file]
def inspect_gcs_file(bucket, filename, info_types=None, min_likelihood=None,
                 max_findings=None):
    """Uses the Data Loss Prevention API to analyze a string for protected data.
    Args:
        bucket: The name of the GCS bucket containing the file, as a string.
        filename: The name of the file in the bucket, including the path, as a
            string; e.g. 'images/myfile.png'.
        info_types: A list of strings representing info types to look for.
            A full list of info type categories can be fetched from the API with
            the .list_root_categories(language_code) client method, and a list
            of types in a category with .list_info_types(category,
            language_code). Examples include 'US_MALE_NAME', 'US_FEMALE_NAME',
            'EMAIL_ADDRESS', 'CANADA_SOCIAL_INSURANCE_NUMBER', 'JAPAN_PASSPORT'.
            If info_types is omitted, the API will use a limited default set.
        min_likelihood: A string representing the minimum likelihood threshold
            that constitutes a match. One of: 'LIKELIHOOD_UNSPECIFIED',
            'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'.
        max_findings: The maximum number of findings to report; 0 = no maximum.
    Returns:
        None; the response from the API is printed to the terminal.
    """

    # Import the client library
    import google.cloud.dlp

    # Instantiate a client.
    dlp = google.cloud.dlp.DlpServiceClient()

    # Prepare info_type by converting the list of strings into a list of
    # dictionaries (protos are also accepted).
    if info_types is not None:
        info_types = [{'name': info_type} for info_type in info_types]

    # Construct the configuration dictionary. Keys which are None may
    # optionally be omitted entirely.
    inspect_config = {
        'info_types': info_types,
        'min_likelihood': min_likelihood,
        'max_findings': max_findings,
    }

    # Construct a cloud_storage_options dictionary with the file's URL.
    url = 'gs://{}/{}'.format(bucket, filename)
    storage_config = {'cloud_storage_options':
                         {'file_set':
                             {'url': url}
                         }
                     }

    operation = dlp.create_inspect_operation(inspect_config, storage_config,
                                             None)

    # Get the operation result name, which can be used to look up the full
    # results. This call blocks until the operation is complete; to avoid
    # blocking, use operation.add_done_callback(fn) instead.
    operation_result = operation.result()

    response = dlp.list_inspect_findings(operation_result.name)

    # TODO DO NOT SUBMIT: haven't successfully gotten results object so not sure this is correct
    if response.result.findings:
        for finding in response.result.findings:
            try:
                print('Quote: {}'.format(finding.quote))
            except AttributeError:
                pass
            print('Info type: {}'.format(finding.info_type.name))
            print('Likelihood: {}'.format(finding.likelihood))
    else:
        print('No findings.')
# [END inspect_gcs_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__)
    parser.add_argument('bucket',
        help='The name of the GCS bucket containing the file.')
    parser.add_argument('filename',
        help='The name of the file in the bucket, including the path, e.g. '
        '"images/myfile.png".')
    parser.add_argument('--info_types', action='append',
        help='Strings representing info types to look for. A full list of info '
             'categories and types is available from the API. Examples '
             'include "US_MALE_NAME", "US_FEMALE_NAME", "EMAIL_ADDRESS", '
             '"CANADA_SOCIAL_INSURANCE_NUMBER", "JAPAN_PASSPORT". If omitted, '
             'the API will use a limited default set. Specify this flag '
             'multiple times to specify multiple info types.')
    parser.add_argument('--min_likelihood',
        choices=['LIKELIHOOD_UNSPECIFIED', 'VERY_UNLIKELY', 'UNLIKELY',
                 'POSSIBLE', 'LIKELY', 'VERY_LIKELY'],
        help='A string representing the minimum likelihood threshold that '
             'constitutes a match.')
    parser.add_argument('--max_findings', type=int,
        help='The maximum number of findings to report; 0 = no maximum.')
    parser.add_argument('--include_quote', type=bool,
        help='A boolean for whether to display a quote of the detected '
             'information in the results.')

    args = parser.parse_args()

    inspect_gcs_file(
        args.bucket, args.filename, info_types=args.info_types,
        min_likelihood=args.min_likelihood, include_quote=args.include_quote)
