import json
import os
import uuid
from datetime import datetime as dt

from query_builder.domain_model.dtos import Query as QueryDTO, Step as StepDTO, \
    Threshold as Threshold, ReadTime
from query_builder.domain_model.models import Query as QueryModel, \
    Step as StepModel

STEPS_MODEL = []
REF_TIME = ReadTime(
    _type='TIMESTAMP',
    value="1w",
    zone=None
)


THRESHOLD_STEP_1 = Threshold(operator='ge', value='15')
THRESHOLD_STEP_2 = Threshold(operator='le', value='15')

STEPS_MODEL_1 = StepModel(uuid.uuid4(), order=1, scc_resource_type="ASSET",
                          out_value="attribute.parent_id",
                          threshold_operator=THRESHOLD_STEP_1.operator, threshold_value=THRESHOLD_STEP_1.value,
                          read_time_type=REF_TIME._type,
                          read_time_value=REF_TIME.value,
                          read_time_zone=REF_TIME.zone, in_value=None,
                          filter="attribute.asset_type = \"Firewall\" AND property.allowed : \"0-65535\"",
                          last_execution_status="fail",last_execution_result=5)                          
STEPS_MODEL.append(STEPS_MODEL_1)
STEPS_MODEL_2 = StepModel(uuid.uuid4(), order=2, scc_resource_type="ASSET",
                          in_value="attribute.parent_id",
                          compare_duration="1w",
                          threshold_operator=THRESHOLD_STEP_2.operator, threshold_value=THRESHOLD_STEP_2.value,
                          read_time=None, out_value=None,
                          filter="attribute.asset_type = \"Instance\"",
                          last_execution_status=None,last_execution_result=None)
STEPS_MODEL.append(STEPS_MODEL_2)
QUERY_MODEL = QueryModel(uuid="087d49d1-5296-4270-997c-9074d9079a5a", name='number_1',
                         description='some description for first query',
                         owner='dandrade@ciandt.com', topic='topic', steps=STEPS_MODEL,
                         sendNotification=True,
                         last_execution_result=None, last_execution_status=None, last_execution_date=None)

STEPS_DTO = []

STEPS_DTO_1 = StepDTO(order=STEPS_MODEL_1.order, kind=STEPS_MODEL_1.scc_resource_type,
                      out_join=STEPS_MODEL_1.out_value,
                      threshold=THRESHOLD_STEP_1,
                      last_execution_status=STEPS_MODEL_1.last_execution_status,
                      last_execution_result=STEPS_MODEL_1.last_execution_result,
                      read_time=REF_TIME, in_join=STEPS_MODEL_1.in_value,
                      filter_=STEPS_MODEL_1.filter, uuid=QUERY_MODEL.uuid)
STEPS_DTO.append(STEPS_DTO_1)
STEPS_DTO_2 = StepDTO(order=STEPS_MODEL_2.order, kind=STEPS_MODEL_2.scc_resource_type,
                      out_join=STEPS_MODEL_2.out_value,
                      threshold=THRESHOLD_STEP_2,
                      last_execution_status=STEPS_MODEL_2.last_execution_status,
                      last_execution_result=STEPS_MODEL_2.last_execution_result,
                      read_time=REF_TIME, in_join=STEPS_MODEL_2.in_value,
                      filter_=STEPS_MODEL_2.filter, uuid=QUERY_MODEL.uuid)
STEPS_DTO.append(STEPS_DTO_2)
QUERY_DTO = QueryDTO(uuid=QUERY_MODEL.uuid, name=QUERY_MODEL.name,
                     description=QUERY_MODEL.description,
                     owner=QUERY_MODEL.owner, topic=QUERY_MODEL.topic,
                     send_notification=QUERY_MODEL.sendNotification, 
                     last_execution_date=QUERY_MODEL.last_execution_date,
                     last_execution_result=QUERY_MODEL.last_execution_result,
                     last_execution_status=QUERY_MODEL.last_execution_status)

QUERY_DTO_WITH_LAST_EXECUTION = QueryDTO(uuid=QUERY_MODEL.uuid,
                                         name=QUERY_MODEL.name,
                                         description=QUERY_MODEL.description,
                                         owner=QUERY_MODEL.owner,
                                         topic=QUERY_MODEL.topic,
                                         send_notification=QUERY_MODEL.sendNotification,
                                         last_execution_date=dt(2019, 1, 14, 10,
                                                                34, 55),
                                         last_execution_result=8,
                                         last_execution_status='SUCCESS')


def load_json_file(path):
    json_file = open(path, 'r')
    json_object = json.loads(json_file.read())
    json_file.close()
    return json_object


PATH = os.path.dirname(os.path.abspath(__file__))
QUERY_JSON_WITH_STEPS = load_json_file(PATH + "/query_json_with_steps.json")
QUERY_JSON_STEP = load_json_file(PATH + "/step.json")
QUERY_JSON_WITHOUT_STEPS = load_json_file(PATH + "/query_without_steps.json")
QUERY_JSON_WITH_STEPS_WITH_LAST_EXECUTION = load_json_file(
    PATH + "/query_json_with_steps_with_last_execution.json")
QUERY_JSON_WITH_STEPS_WITHOUT_LAST_EXECUTION = load_json_file(
    PATH + "/query_json_with_steps_without_last_execution.json")
