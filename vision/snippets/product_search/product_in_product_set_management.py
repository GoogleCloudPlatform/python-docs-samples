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

"""This application demonstrates how to perform create operations
on Product set in Cloud Vision Product Search.

For more information, see the tutorial page at
https://cloud.google.com/vision/product-search/docs/
"""

import argparse

# [START vision_product_search_add_product_to_product_set]
# [START vision_product_search_remove_product_from_product_set]
# [START vision_product_search_purge_products_in_product_set]
from google.cloud import vision

# [END vision_product_search_add_product_to_product_set]
# [END vision_product_search_remove_product_from_product_set]
# [END vision_product_search_purge_products_in_product_set]


# [START vision_product_search_add_product_to_product_set]
def add_product_to_product_set(
        project_id, location, product_id, product_set_id):
    """Add a product to a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Add the product to the product set.
    client.add_product_to_product_set(
        name=product_set_path, product=product_path)
    print('Product added to product set.')
# [END vision_product_search_add_product_to_product_set]


# [START vision_product_search_list_products_in_product_set]
def list_products_in_product_set(
        project_id, location, product_set_id):
    """List all products in a product set.
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

    # List all the products available in the product set.
    products = client.list_products_in_product_set(name=product_set_path)

    # Display the product information.
    for product in products:
        print(f'Product name: {product.name}')
        print('Product id: {}'.format(product.name.split('/')[-1]))
        print(f'Product display name: {product.display_name}')
        print(f'Product description: {product.description}')
        print(f'Product category: {product.product_category}')
        print(f'Product labels: {product.product_labels}')
# [END vision_product_search_list_products_in_product_set]


# [START vision_product_search_remove_product_from_product_set]
def remove_product_from_product_set(
        project_id, location, product_id, product_set_id):
    """Remove a product from a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Remove the product from the product set.
    client.remove_product_from_product_set(
        name=product_set_path, product=product_path)
    print('Product removed from product set.')
# [END vision_product_search_remove_product_from_product_set]


# [START vision_product_search_purge_products_in_product_set]
def purge_products_in_product_set(
        project_id, location, product_set_id, force):
    """Delete all products in a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        force: Perform the purge only when force is set to True.
    """
    client = vision.ProductSearchClient()

    parent = f"projects/{project_id}/locations/{location}"

    product_set_purge_config = vision.ProductSetPurgeConfig(
        product_set_id=product_set_id)

    # The purge operation is async.
    operation = client.purge_products(request={
        "parent": parent,
        "product_set_purge_config": product_set_purge_config,
        # The operation is irreversible and removes multiple products.
        # The user is required to pass in force=True to actually perform the
        # purge.
        # If force is not set to True, the service raises an exception.
        "force": force
    })

    operation.result(timeout=500)

    print('Deleted products in product set.')
# [END vision_product_search_purge_products_in_product_set]


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

    add_product_to_product_set_parser = subparsers.add_parser(
        'add_product_to_product_set', help=add_product_to_product_set.__doc__)
    add_product_to_product_set_parser.add_argument('product_id')
    add_product_to_product_set_parser.add_argument('product_set_id')

    list_products_in_product_set_parser = subparsers.add_parser(
        'list_products_in_product_set',
        help=list_products_in_product_set.__doc__)
    list_products_in_product_set_parser.add_argument('product_set_id')

    remove_product_from_product_set_parser = subparsers.add_parser(
        'remove_product_from_product_set',
        help=remove_product_from_product_set.__doc__)
    remove_product_from_product_set_parser.add_argument('product_id')
    remove_product_from_product_set_parser.add_argument('product_set_id')

    purge_products_in_product_set_parser = subparsers.add_parser(
        'purge_products_in_product_set',
        help=purge_products_in_product_set.__doc__)
    purge_products_in_product_set_parser.add_argument('product_set_id')
    purge_products_in_product_set_parser.add_argument(
        '--force', action='store_true')

    args = parser.parse_args()

    if args.command == 'add_product_to_product_set':
        add_product_to_product_set(
            args.project_id, args.location, args.product_id,
            args.product_set_id)
    elif args.command == 'list_products_in_product_set':
        list_products_in_product_set(
            args.project_id, args.location, args.product_set_id)
    elif args.command == 'remove_product_from_product_set':
        remove_product_from_product_set(
            args.project_id, args.location, args.product_id,
            args.product_set_id)
    elif args.command == 'purge_products_in_product_set':
        purge_products_in_product_set(
            args.project_id, args.location, args.product_set_id, args.force)
