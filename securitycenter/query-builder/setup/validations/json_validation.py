"""validation for input json"""

import jsonschema
import simplejson as json


def validate(input_json):
    with open('validations/schema.json', 'r') as f:
        schema_data = f.read()
    schema = json.loads(schema_data)
    jsonschema.validate(input_json, schema)
