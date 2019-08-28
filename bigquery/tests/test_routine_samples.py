# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import bigquery
from google.cloud import bigquery_v2


def test_create_routine(capsys, client, random_routine_id):
    from .. import create_routine

    create_routine.create_routine(client, random_routine_id)
    out, err = capsys.readouterr()
    assert "Created routine {}".format(random_routine_id) in out


def test_create_routine_ddl(capsys, client, random_routine_id):
    from .. import create_routine_ddl

    create_routine_ddl.create_routine_ddl(client, random_routine_id)
    routine = client.get_routine(random_routine_id)
    out, err = capsys.readouterr()

    assert "Created routine {}".format(random_routine_id) in out
    return routine
    assert routine.type_ == "SCALAR_FUNCTION"
    assert routine.language == "SQL"
    expected_arguments = [
        bigquery.RoutineArgument(
            name="arr",
            data_type=bigquery_v2.types.StandardSqlDataType(
                type_kind=bigquery_v2.enums.StandardSqlDataType.TypeKind.ARRAY,
                array_element_type=bigquery_v2.types.StandardSqlDataType(
                    type_kind=bigquery_v2.enums.StandardSqlDataType.TypeKind.STRUCT,
                    struct_type=bigquery_v2.types.StandardSqlStructType(
                        fields=[
                            bigquery_v2.types.StandardSqlField(
                                name="name",
                                type=bigquery_v2.types.StandardSqlDataType(
                                    type_kind=bigquery_v2.enums.StandardSqlDataType.TypeKind.STRING
                                ),
                            ),
                            bigquery_v2.types.StandardSqlField(
                                name="val",
                                type=bigquery_v2.types.StandardSqlDataType(
                                    type_kind=bigquery_v2.enums.StandardSqlDataType.TypeKind.INT64
                                ),
                            ),
                        ]
                    ),
                ),
            ),
        )
    ]
    assert routine.arguments == expected_arguments


def test_list_routines(capsys, client, dataset_id, routine_id):
    from .. import list_routines

    list_routines.list_routines(client, dataset_id)
    out, err = capsys.readouterr()
    assert "Routines contained in dataset {}:".format(dataset_id) in out
    assert routine_id in out


def test_delete_routine(capsys, client, routine_id):
    from .. import delete_routine

    delete_routine.delete_routine(client, routine_id)
    out, err = capsys.readouterr()
    assert "Deleted routine {}.".format(routine_id) in out


def test_update_routine(client, routine_id):
    from .. import update_routine

    routine = update_routine.update_routine(client, routine_id)
    assert routine.body == "x * 4"
