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

"""This application demonstrates how to perform basic operations on Product
in Cloud Vision Product Search.

For more information, see the tutorial page at
https://cloud.google.com/vision/product-search/docs/
"""

import argparse

# [START vision_product_search_create_product]
# [START vision_product_search_delete_product]
# [START vision_product_search_list_products]
# [START vision_product_search_get_product]
# [START vision_product_search_update_product_labels]
# [START vision_product_search_purge_orphan_products]
from google.cloud import vision
from google.protobuf import field_mask_pb2 as field_mask

# [END vision_product_search_create_product]
# [END vision_product_search_delete_product]
# [END vision_product_search_list_products]
# [END vision_product_search_get_product]
# [END vision_product_search_update_product_labels]
# [END vision_product_search_purge_orphan_products]


# [START vision_product_search_create_product]
def create_product(
        project_id, location, product_id, product_display_name,
        product_category):
    """Create one product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_display_name: Display name of the product.
        product_category: Category of the product.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product with the product specification in the region.
    # Set product display name and product category.
    product = vision.Product(
        display_name=product_display_name,
        product_category=product_category)

    # The response is the product with the `name` field populated.
    response = client.create_product(
        parent=location_path,
        product=product,
        product_id=product_id)

    # Display the product information.
    print(f'Product name: {response.name}')
# [END vision_product_search_create_product]


# [START vision_product_search_list_products]
def list_products(project_id, location):
    """List all products.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # List all the products available in the region.
    products = client.list_products(parent=location_path)

    # Display the product information.
    for product in products:
        print(f'Product name: {product.name}')
        print('Product id: {}'.format(product.name.split('/')[-1]))
        print(f'Product display name: {product.display_name}')
        print(f'Product description: {product.description}')
        print(f'Product category: {product.product_category}')
        print(f'Product labels: {product.product_labels}\n')
# [END vision_product_search_list_products]


# [START vision_product_search_get_product]
def get_product(project_id, location, product_id):
    """Get information about a product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Get complete detail of the product.
    product = client.get_product(name=product_path)

    # Display the product information.
    print(f'Product name: {product.name}')
    print('Product id: {}'.format(product.name.split('/')[-1]))
    print(f'Product display name: {product.display_name}')
    print(f'Product description: {product.description}')
    print(f'Product category: {product.product_category}')
    print(f'Product labels: {product.product_labels}')
# [END vision_product_search_get_product]


# [START vision_product_search_update_product_labels]
def update_product_labels(
        project_id, location, product_id, key, value):
    """Update the product labels.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        key: The key of the label.
        value: The value of the label.
    """
    client = vision.ProductSearchClient()

    # Get the name of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Set product name, product label and product display name.
    # Multiple labels are also supported.
    key_value = vision.Product.KeyValue(key=key, value=value)
    product = vision.Product(
        name=product_path,
        product_labels=[key_value])

    # Updating only the product_labels field here.
    update_mask = field_mask.FieldMask(paths=['product_labels'])

    # This overwrites the product_labels.
    updated_product = client.update_product(
        product=product, update_mask=update_mask)

    # Display the updated product information.
    print(f'Product name: {updated_product.name}')
    print(f'Updated product labels: {product.product_labels}')
# [END vision_product_search_update_product_labels]


# [START vision_product_search_delete_product]
def delete_product(project_id, location, product_id):
    """Delete the product and all its reference images.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Delete a product.
    client.delete_product(name=product_path)
    print('Product deleted.')
# [END vision_product_search_delete_product]


# [START vision_product_search_purge_orphan_products]
def purge_orphan_products(project_id, location, force):
    """Delete all products not in any product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient()

    parent = f"projects/{project_id}/locations/{location}"

    # The purge operation is async.
    operation = client.purge_products(request={
        "parent": parent,
        "delete_orphan_products": True,
        # The operation is irreversible and removes multiple products.
        # The user is required to pass in force=True to actually perform the
        # purge.
        # If force is not set to True, the service raises an exception.
        "force": force
    })

    operation.result(timeout=500)

    print('Orphan products deleted.')
# [END vision_product_search_purge_orphan_products]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '--project_id',
        help='Project id.  Required',
        required=True)
    parser.add_argument(
        '--location',
        help='Compute region name',
        default='us-west1')

    subparsers = parser.add_subparsers(dest='command')

    create_product_parser = subparsers.add_parser(
        'create_product', help=create_product.__doc__)
    create_product_parser.add_argument('product_id')
    create_product_parser.add_argument('product_display_name')
    create_product_parser.add_argument('product_category')

    list_products_parser = subparsers.add_parser(
        'list_products', help=list_products.__doc__)

    get_product_parser = subparsers.add_parser(
        'get_product', help=get_product.__doc__)
    get_product_parser.add_argument('product_id')

    update_product_labels_parser = subparsers.add_parser(
        'update_product_labels', help=update_product_labels.__doc__)
    update_product_labels_parser.add_argument('product_id')
    update_product_labels_parser.add_argument('key')
    update_product_labels_parser.add_argument('value')

    delete_product_parser = subparsers.add_parser(
        'delete_product', help=delete_product.__doc__)
    delete_product_parser.add_argument('product_id')

    purge_orphan_products_parser = subparsers.add_parser(
        'purge_orphan_products', help=purge_orphan_products.__doc__)
    purge_orphan_products_parser.add_argument('--force', action='store_true')

    args = parser.parse_args()

    if args.command == 'create_product':
        create_product(
            args.project_id, args.location, args.product_id,
            args.product_display_name, args.product_category)
    elif args.command == 'list_products':
        list_products(args.project_id, args.location)
    elif args.command == 'get_product':
        get_product(args.project_id, args.location, args.product_id)
    elif args.command == 'update_product_labels':
        update_product_labels(
            args.project_id, args.location, args.product_id,
            args.key, args.value)
    elif args.command == 'delete_product':
        delete_product(args.project_id, args.location, args.product_id)
    elif args.command == 'purge_orphan_products':
        purge_orphan_products(args.project_id, args.location, args.force)
