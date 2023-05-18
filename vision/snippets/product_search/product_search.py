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

"""This tutorial demonstrates how users query the product set with their
own images and find the products similer to the image using the Cloud
Vision Product Search API.

For more information, see the tutorial page at
https://cloud.google.com/vision/product-search/docs/
"""

import argparse

# [START vision_product_search_get_similar_products]
# [START vision_product_search_get_similar_products_gcs]
from google.cloud import vision

# [END vision_product_search_get_similar_products]
# [END vision_product_search_get_similar_products_gcs]


# [START vision_product_search_get_similar_products]
def get_similar_products_file(
        project_id,
        location,
        product_set_id,
        product_category,
        file_path,
        filter,
        max_results
):
    """Search similar products to image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_category: Category of the product.
        file_path: Local file path of the image to be searched.
        filter: Condition to be applied on the labels.
                Example for filter: (color = red OR color = blue) AND style = kids
                It will search on all products with the following labels:
                color:red AND style:kids
                color:blue AND style:kids
        max_results: The maximum number of results (matches) to return. If omitted, all results are returned.
    """
    # product_search_client is needed only for its helper methods.
    product_search_client = vision.ProductSearchClient()
    image_annotator_client = vision.ImageAnnotatorClient()

    # Read the image as a stream of bytes.
    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    # Create annotate image request along with product search feature.
    image = vision.Image(content=content)

    # product search specific parameters
    product_set_path = product_search_client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)
    product_search_params = vision.ProductSearchParams(
        product_set=product_set_path,
        product_categories=[product_category],
        filter=filter)
    image_context = vision.ImageContext(
        product_search_params=product_search_params)

    # Search products similar to the image.
    response = image_annotator_client.product_search(
        image,
        image_context=image_context,
        max_results=max_results
    )

    index_time = response.product_search_results.index_time
    print('Product set index time: ')
    print(index_time)

    results = response.product_search_results.results

    print('Search results:')
    for result in results:
        product = result.product

        print(f'Score(Confidence): {result.score}')
        print(f'Image name: {result.image}')

        print(f'Product name: {product.name}')
        print('Product display name: {}'.format(
            product.display_name))
        print(f'Product description: {product.description}\n')
        print(f'Product labels: {product.product_labels}\n')
# [END vision_product_search_get_similar_products]


# [START vision_product_search_get_similar_products_gcs]
def get_similar_products_uri(
        project_id, location, product_set_id, product_category,
        image_uri, filter):
    """Search similar products to image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_category: Category of the product.
        image_uri: Cloud Storage location of image to be searched.
        filter: Condition to be applied on the labels.
        Example for filter: (color = red OR color = blue) AND style = kids
        It will search on all products with the following labels:
        color:red AND style:kids
        color:blue AND style:kids
    """
    # product_search_client is needed only for its helper methods.
    product_search_client = vision.ProductSearchClient()
    image_annotator_client = vision.ImageAnnotatorClient()

    # Create annotate image request along with product search feature.
    image_source = vision.ImageSource(image_uri=image_uri)
    image = vision.Image(source=image_source)

    # product search specific parameters
    product_set_path = product_search_client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)
    product_search_params = vision.ProductSearchParams(
        product_set=product_set_path,
        product_categories=[product_category],
        filter=filter)
    image_context = vision.ImageContext(
        product_search_params=product_search_params)

    # Search products similar to the image.
    response = image_annotator_client.product_search(
        image, image_context=image_context)

    index_time = response.product_search_results.index_time
    print('Product set index time: ')
    print(index_time)

    results = response.product_search_results.results

    print('Search results:')
    for result in results:
        product = result.product

        print(f'Score(Confidence): {result.score}')
        print(f'Image name: {result.image}')

        print(f'Product name: {product.name}')
        print('Product display name: {}'.format(
            product.display_name))
        print(f'Product description: {product.description}\n')
        print(f'Product labels: {product.product_labels}\n')
# [END vision_product_search_get_similar_products_gcs]


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
    parser.add_argument('--product_set_id')
    parser.add_argument('--product_category')
    parser.add_argument('--filter', default='')
    parser.add_argument('--max_results', default='')

    get_similar_products_file_parser = subparsers.add_parser(
        'get_similar_products_file', help=get_similar_products_file.__doc__)
    get_similar_products_file_parser.add_argument('--file_path')

    get_similar_products_uri_parser = subparsers.add_parser(
        'get_similar_products_uri', help=get_similar_products_uri.__doc__)
    get_similar_products_uri_parser.add_argument('--image_uri')

    args = parser.parse_args()

    if args.command == 'get_similar_products_file':
        get_similar_products_file(
            args.project_id, args.location, args.product_set_id,
            args.product_category, args.file_path, args.filter, args.max_results)
    elif args.command == 'get_similar_products_uri':
        get_similar_products_uri(
            args.project_id, args.location, args.product_set_id,
            args.product_category, args.image_uri, args.filter, args.max_results)
