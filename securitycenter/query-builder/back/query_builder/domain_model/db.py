import os
from peewee import MySQLDatabase, SqliteDatabase
import query_builder.application.default_settings as default_settings

LOGGER = default_settings.configure_logger('db')


def select_database(db_name):
    if db_name == "Sqlite":
        LOGGER.info("Connecting on Sqlite")
        return SqliteDatabase('test.db')
    else:
        LOGGER.info("Connecting on MySQL")
        return MySQLDatabase(
            'query_builder',
            user=os.getenv('db_user'),
            password=os.getenv('db_password'),
            host=os.getenv('db_host', '172.17.0.2'),
            port=int(os.getenv('db_port', '3306'))
        )


database = select_database(os.getenv('db_type', 'Sqlite'))
