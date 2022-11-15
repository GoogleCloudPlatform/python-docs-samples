#!/usr/bin/env python

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform operations
on Product set in Cloud Vision Product Search.

For more information, see the tutorial page at
https://cloud.google.com/vision/product-search/docs/
"""

import argparse

# [START vision_product_search_delete_product_set]
# [START vision_product_search_list_product_sets]
# [START vision_product_search_get_product_set]
# [START vision_product_search_create_product_set]
from google.cloud import vision

# [END vision_product_search_delete_product_set]
# [END vision_product_search_list_product_sets]
# [END vision_product_search_get_product_set]
# [END vision_product_search_create_product_set]


# [START vision_product_search_create_product_set]
def create_product_set(
        project_id, location, product_set_id, product_set_display_name):
    """Create a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_set_display_name: Display name of the product set.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product set with the product set specification in the region.
    product_set = vision.ProductSet(
            display_name=product_set_display_name)

    # The response is the product set with `name` populated.
    response = client.create_product_set(
        parent=location_path,
        product_set=product_set,
        product_set_id=product_set_id)

    # Display the product set information.
    print('Product set name: {}'.format(response.name))
# [END vision_product_search_create_product_set]


# [START vision_product_search_list_product_sets]
def list_product_sets(project_id, location):
    """List all product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # List all the product sets available in the region.
    product_sets = client.list_product_sets(parent=location_path)

    # Display the product set information.
    for product_set in product_sets:
        print('Product set name: {}'.format(product_set.name))
        print('Product set id: {}'.format(product_set.name.split('/')[-1]))
        print('Product set display name: {}'.format(product_set.display_name))
        print('Product set index time: ')
        print(product_set.index_time)
# [END vision_product_search_list_product_sets]


# [START vision_product_search_get_product_set]
def get_product_set(project_id, location, product_set_id):
    """Get info about the product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Get complete detail of the product set.
    product_set = client.get_product_set(name=product_set_path)

    # Display the product set information.
    print('Product set name: {}'.format(product_set.name))
    print('Product set id: {}'.format(product_set.name.split('/')[-1]))
    print('Product set display name: {}'.format(product_set.display_name))
    print('Product set index time: ')
    print(product_set.index_time)
# [END vision_product_search_get_product_set]


# [START vision_product_search_delete_product_set]
def delete_product_set(project_id, location, product_set_id):
    """Delete a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Delete the product set.
    client.delete_product_set(name=product_set_path)
    print('Product set deleted.')
# [END vision_product_search_delete_product_set]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    parser.add_argument(
        '--project_id',
        help='Project id.  Required',
        required=True)
    parser.add_argument(
        '--location',
        help='Compute region name',
        default='us-west1')

    create_product_set_parser = subparsers.add_parser(
        'create_product_set', help=create_product_set.__doc__)
    create_product_set_parser.add_argument('product_set_id')
    create_product_set_parser.add_argument('product_set_display_name')

    list_product_sets_parser = subparsers.add_parser(
        'list_product_sets', help=list_product_sets.__doc__)

    get_product_set_parser = subparsers.add_parser(
        'get_product_set', help=get_product_set.__doc__)
    get_product_set_parser.add_argument('product_set_id')

    delete_product_set_parser = subparsers.add_parser(
        'delete_product_set', help=delete_product_set.__doc__)
    delete_product_set_parser.add_argument('product_set_id')

    args = parser.parse_args()

    if args.command == 'create_product_set':
        create_product_set(
            args.project_id, args.location, args.product_set_id,
            args.product_set_display_name)
    elif args.command == 'list_product_sets':
        list_product_sets(args.project_id, args.location)
    elif args.command == 'get_product_set':
        get_product_set(args.project_id, args.location, args.product_set_id)
    elif args.command == 'delete_product_set':
        delete_product_set(
            args.project_id, args.location, args.product_set_id)
