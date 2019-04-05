"""Peewee test class"""
import argparse
import pytest
from query_builder.application import app as _app
from peewee import Model, AutoField, CharField, SqliteDatabase

USER = "proxyuser"
PASSWORD = "kubernetes-test"
HOST = "localhost"
PORT = 3306
DATABASENAME = "query_builder"

DATABASE = SqliteDatabase(':memory:')


class BaseModel(Model):
    """Base Model for Peewee test"""
    class Meta:
        """Define database instance for BaseModel"""
        database = DATABASE


class ModelTest(BaseModel):
    """Test Model for Peewee test"""
    id = AutoField()  # Auto-incrementing primary key.
    query = CharField()

    class Meta:
        """Define table name for ModelTest"""
        table_name = 'test'


class ModelTest2(BaseModel):
    """Test Model for Peewee test"""
    id = AutoField()  # Auto-incrementing primary key.
    name = CharField()

    class Meta:
        """Define database instance for BaseModel2"""
        table_name = 'test_two'


@pytest.fixture
def create_app():
    """Create app in development configuration"""
    return _app.create_app('development')


@pytest.fixture
def close_connections():
    """Close connection with database before running all tests"""
    if not DATABASE.is_closed():
        DATABASE.close()


def test_peewee_connect():
    """Test connection database"""
    result = DATABASE.connect()
    assert result


@pytest.mark.skip("Skiping tables creation")
def test_peewee_create_table():
    """Test table creation using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    DATABASE.create_tables([ModelTest, ModelTest2])
    result = len(DATABASE.get_tables())
    assert result == 2


def test_peewee_insert_row():
    """Test insertion in table using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    if not ModelTest.table_exists():
        ModelTest.create_table()

    result = ModelTest(query="TEST QUERY INSERT").save()
    
    assert result == 1


def test_peewee_select_row():
    """Test selection at table using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    if not ModelTest.table_exists():
        ModelTest.create_table()

    #GIVEN
    ModelTest(query="TEST QUERY TO SELECT").save()

    #WHEN
    result = ModelTest.select().where(ModelTest.query == "TEST QUERY TO SELECT").count()

    #THEN
    assert result == 1


def test_peewee_select_not_found():
    """Test selection not founf at table using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    if not ModelTest.table_exists():
        ModelTest.create_table()

    result = ModelTest.select().where(ModelTest.query == "TEST QUERY").count()

    ModelTest.drop_table()
    assert result == 0


def test_peewee_update_row():
    """Test updating row using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    if not ModelTest.table_exists():
        ModelTest.create_table()

    #GIVEN
    ModelTest(query="TEST QUERY TO INSERT").save()

    #WHEN
    ModelTest.update(query="TEST QUERY UPDATED")\
    .where(ModelTest.query == "TEST QUERY TO INSERT").execute()

    #THEN
    result = ModelTest.select().where(ModelTest.query == "TEST QUERY UPDATED").count()

    ModelTest.drop_table()
    assert result == 1


def test_peewee_insert_many():
    """Test many inserts using Peewee"""
    if DATABASE.is_closed():

        DATABASE.connect()

    if not ModelTest2.table_exists():
        ModelTest2.create_table()

    fields = [ModelTest2.id, ModelTest2.name]
    data_source = [
        (None, 'test_1'),
        (None, 'test_2'),
        (None, 'test_3'),
        (None, 'test_4')
    ]
    models_inserted = ModelTest2.insert_many(
        data_source,
        fields=fields
    ).execute()

    ModelTest2.drop_table()
    assert models_inserted == 4


def test_peewee_delete_records():
    """Test delete rows using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    if not ModelTest.table_exists():
        ModelTest.create_table()

    #GIVEN
    ModelTest(query="TEST QUERY TO DELETE", id=2).save()

    #WHEN
    ModelTest.delete().where(ModelTest.id == 2).execute()

    #THEN
    exists = ModelTest.select().where(ModelTest.query == "TEST QUERY TO DELETE").count()

    ModelTest.drop_table()
    assert exists == 0


def test_peewee_drop_table():
    """Test drop table using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    #GIVEN
    DATABASE.create_tables([ModelTest, ModelTest2])

    #WHEN
    DATABASE.drop_tables([ModelTest, ModelTest2])

    #THEN
    result = len(DATABASE.get_tables())
    assert result == 0


def test_close_db():
    """Test closing connection using Peewee"""
    if DATABASE.is_closed():
        DATABASE.connect()

    assert DATABASE.close()
