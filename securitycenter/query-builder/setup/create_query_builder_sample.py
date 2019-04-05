#!/usr/bin/env python3
"""
Script that creates a sample file
to be used as input on run_setup of query_builder
"""
import json

import click

from parameters import QUERY_BUILDER_INPUT


@click.command()
@click.option('--output-file', help='File name', required=True)
def create_query_builder_sample(output_file):
    """ create query builder sample """
    with open(output_file, 'w') as outfile:
        json.dump(QUERY_BUILDER_INPUT, outfile, ensure_ascii=False, indent=4)
    click.echo("Output-file written [%s]" % output_file)


if __name__ == '__main__':
    create_query_builder_sample()  # pylint: disable=no-value-for-parameter
