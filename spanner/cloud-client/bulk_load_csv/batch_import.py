# Copyright 2019 Google Inc. All Rights Reserved.
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
#
# This application demonstrates how to do batch operations from a csv file
# using Cloud Spanner.
# For more information, see the README.rst.


import csv
import time
import threading
import argparse
from google.cloud import spanner


def is_bool_null(file):
    # This function convertes the boolean values
    # in the dataset from strings to boolean data types.
    # It also converts the string Null to a None data
    # type indicating an empty cell.
    data = list(csv.reader(file))
    # Reads each line in the csv file.
    for line in range(len(data)):
        for cell in range(len(data[line])):
            # Changes the string to boolean.
            if data[line][cell] == 'true':
                data[line][cell] = eval('True')
            # Changes blank string to python readable None type.
            if data[line][cell] == '':
                data[line][cell] = None
    return (data)


def divide_chunks(lst, n):
    # This function divides the csv file into chunks so that the mutation will
    # commit every 500 rows.
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def insert_data(database, filepath, table_name, column_names):
    # This function iterates over the list of files
    # belonging to the dataset and,
    # writes each line into cloud spanner using the batch mutation function.
    with open(filepath, newline='') as file:
        data = is_bool_null(file)
        data = tuple(data)
        l_group = list(divide_chunks(data, 500))
    # Inserts each chunk of data into database
    for current_inserts in (l_group):
        if current_inserts is not None:
            with database.batch() as batch:
                batch.insert(
                    table=table_name,
                    columns=column_names,
                    values=current_inserts)


def main(instance_id, database_id):
    # Inserts sample data into the given database.
    # The database and table must already exist and can be created
    # using`create_database`.
    start = time.time()
    # File paths
    comments_file = 'hnewscomments.txt'
    stories_file = 'hnewsstories.txt'
    # Instantiates a spanner client
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)
    # Sets the Column names.
    s_columnnames = (
        'id',
        'by',
        'author',
        'dead',
        'deleted',
        'descendants',
        'score',
        'text',
        'time',
        'time_ts',
        'title',
        'url',
    )
    c_columnnames = (
        'id',
        'by',
        'author',
        'dead',
        'deleted',
        'parent',
        'ranking',
        'text',
        'time',
        'time_ts',
    )
    # Creates threads
    t1 = threading.Thread(
        target=insert_data,
        args=(database, stories_file, 'stories', s_columnnames))
    t2 = threading.Thread(
        target=insert_data,
        args=(database, comments_file, 'comments', c_columnnames))
    # Starting threads
    t1.start()
    t2.start()
    # Wait until all threads finish
    t1.join()
    t2.join()

    print('Finished Inserting Data.')
    end = time.time()
    print('Time: ', end - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('instance_id', help='Your Cloud Spanner instance ID.')
    parser.add_argument('database_id', help='Your Cloud Spanner database ID.')

    args = parser.parse_args()

    main(args.instance_id, args.database_id)
