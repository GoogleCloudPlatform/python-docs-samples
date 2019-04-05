from .db import database

from peewee import (
    AutoField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    UUIDField,
    BooleanField,
    TextField
)


class BaseModel(Model):
    class Meta:
        database = database


class Query(BaseModel):
    uuid = UUIDField(primary_key=True)
    name = CharField()
    description = CharField()
    owner = CharField()
    topic = CharField(null=True)
    timestamp = DateTimeField(null=True)
    schedule = CharField(null=True)
    next_run = DateTimeField(null=True)
    send_notification = BooleanField(default=False)
    last_execution_date = DateTimeField(null=True)
    last_execution_result = IntegerField(null=True)
    last_execution_status = CharField(null=True)

    class Meta:
        table_name = 'query'


class Step(BaseModel):
    _id = AutoField(primary_key=True)
    order = IntegerField()
    scc_resource_type = CharField()
    filter = TextField(null=True)
    read_time_type = CharField(null=True)
    read_time_value = CharField(null=True)
    read_time_zone = CharField(null=True)
    compare_duration = CharField(null=True)
    in_value = TextField(null=True)
    out_value = TextField(null=True)
    threshold_operator = CharField(null=True)
    threshold_value = CharField(null=True)
    last_execution_result = IntegerField(null=True)
    last_execution_status = CharField(null=True)
    query = ForeignKeyField(Query, related_name='steps')

    class Meta:
        table_name = 'step'
