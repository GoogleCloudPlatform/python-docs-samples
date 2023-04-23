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

"""This application demonstrates how to perform basic operations on reference
images in Cloud Vision Product Search.

For more information, see the tutorial page at
https://cloud.google.com/vision/product-search/docs/
"""

import argparse

# [START vision_product_search_create_reference_image]
# [START vision_product_search_delete_reference_image]
# [START vision_product_search_list_reference_images]
# [START vision_product_search_get_reference_image]
from google.cloud import vision

# [END vision_product_search_create_reference_image]
# [END vision_product_search_delete_reference_image]
# [END vision_product_search_list_reference_images]
# [END vision_product_search_get_reference_image]


# [START vision_product_search_create_reference_image]
def create_reference_image(
        project_id, location, product_id, reference_image_id, gcs_uri):
    """Create a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
        gcs_uri: Google Cloud Storage path of the input image.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Create a reference image.
    reference_image = vision.ReferenceImage(uri=gcs_uri)

    # The response is the reference image with `name` populated.
    image = client.create_reference_image(
        parent=product_path,
        reference_image=reference_image,
        reference_image_id=reference_image_id)

    # Display the reference image information.
    print(f'Reference image name: {image.name}')
    print(f'Reference image uri: {image.uri}')
# [END vision_product_search_create_reference_image]


# [START vision_product_search_list_reference_images]
def list_reference_images(
        project_id, location, product_id):
    """List all images in a product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # List all the reference images available in the product.
    reference_images = client.list_reference_images(parent=product_path)

    # Display the reference image information.
    for image in reference_images:
        print(f'Reference image name: {image.name}')
        print('Reference image id: {}'.format(image.name.split('/')[-1]))
        print(f'Reference image uri: {image.uri}')
        print('Reference image bounding polygons: {}'.format(
            image.bounding_polys))
# [END vision_product_search_list_reference_images]


# [START vision_product_search_get_reference_image]
def get_reference_image(
        project_id, location, product_id, reference_image_id):
    """Get info about a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the reference image.
    reference_image_path = client.reference_image_path(
        project=project_id, location=location, product=product_id,
        reference_image=reference_image_id)

    # Get complete detail of the reference image.
    image = client.get_reference_image(name=reference_image_path)

    # Display the reference image information.
    print(f'Reference image name: {image.name}')
    print('Reference image id: {}'.format(image.name.split('/')[-1]))
    print(f'Reference image uri: {image.uri}')
    print(f'Reference image bounding polygons: {image.bounding_polys}')
# [END vision_product_search_get_reference_image]


# [START vision_product_search_delete_reference_image]
def delete_reference_image(
        project_id, location, product_id, reference_image_id):
    """Delete a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the reference image.
    reference_image_path = client.reference_image_path(
        project=project_id, location=location, product=product_id,
        reference_image=reference_image_id)

    # Delete the reference image.
    client.delete_reference_image(name=reference_image_path)
    print('Reference image deleted from product.')
# [END vision_product_search_delete_reference_image]


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

    create_reference_image_parser = subparsers.add_parser(
        'create_reference_image', help=create_reference_image.__doc__)
    create_reference_image_parser.add_argument('product_id')
    create_reference_image_parser.add_argument('reference_image_id')
    create_reference_image_parser.add_argument('gcs_uri')

    list_reference_images_parser = subparsers.add_parser(
        'list_reference_images',
        help=list_reference_images.__doc__)
    list_reference_images_parser.add_argument('product_id')

    get_reference_image_parser = subparsers.add_parser(
        'get_reference_image', help=get_reference_image.__doc__)
    get_reference_image_parser.add_argument('product_id')
    get_reference_image_parser.add_argument('reference_image_id')

    delete_reference_image_parser = subparsers.add_parser(
        'delete_reference_image', help=delete_reference_image.__doc__)
    delete_reference_image_parser.add_argument('product_id')
    delete_reference_image_parser.add_argument('reference_image_id')

    args = parser.parse_args()

    if args.command == 'create_reference_image':
        create_reference_image(
            args.project_id, args.location, args.product_id,
            args.reference_image_id, args.gcs_uri)
    elif args.command == 'list_reference_images':
        list_reference_images(
            args.project_id, args.location, args.product_id)
    elif args.command == 'get_reference_image':
        get_reference_image(
            args.project_id, args.location, args.product_id,
            args.reference_image_id)
    elif args.command == 'delete_reference_image':
        delete_reference_image(
            args.project_id, args.location, args.product_id,
            args.reference_image_id)
