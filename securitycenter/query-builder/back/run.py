import os

from flask_cors import CORS

from query_builder.application.app import (
    create_app,
    create_database
)
from query_builder.domain_model.services.configuration_service import is_production_environment

MODE = os.getenv('APP_ENV', 'development')

create_database()
APP = create_app(mode=MODE)
CORS(APP)

if __name__ == '__main__':
    APP.run(**APP.config.get_namespace('RUN_'))
