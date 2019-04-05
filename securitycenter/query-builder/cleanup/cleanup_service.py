import datetime
import os
from time import sleep

import client.scc_client_beta as scc
from settings import configure_logger


LOGGER = configure_logger('cleanup_service')
TIME_SPENT = os.getenv('TIME_SPENT', 900)
SCC_SEARCH_TIMEOUT_SECONDS = os.getenv('SCC_SEARCH_TIMEOUT_SECONDS', None)
ORGANIZATION_ID = os.getenv('organization_id', None)

QUERY_UUID_LIST = []

# Queries per Second allowed in the API calls
WAIT_TIME = 1 / float(os.getenv('QPS', '1000'))


def add_to_be_processed(query_uuid):
    if QUERY_UUID_LIST.count(query_uuid) < 1:
        QUERY_UUID_LIST.append(query_uuid)


def pull_messages(message):
    query_uuid = message.data.decode('utf-8')
    LOGGER.info("received query id: %s", query_uuid)
    add_to_be_processed(query_uuid)
    message.ack()


def build_temp_marks_keys(uuid):
    return 'sccquerydraft{}'.format(uuid).replace("-",""), 'sccquerydrafttime{}'.format(uuid).replace("-","")


def clean_by_uuid(uuid):
    LOGGER.info("clean temp mark for query uuid %s.", uuid)
    client = scc.Client(organization_id=ORGANIZATION_ID)

    main_key, time_key = build_temp_marks_keys(uuid)

    query_args = 'securityMarks.marks.{}= "true"'.format(main_key)

    marks_to_delete = [main_key, time_key]

    remove_temp_asset_mark(client, query_args, marks_to_delete)
    remove_temp_finding_mark(client, query_args, marks_to_delete)


def remove_temp_asset_mark(client, query_args, marks_to_delete):
    LOGGER.info("clean temp mark for ASSET query_args %s.", query_args)
    results = client.list_assets(filter_expression=query_args)

    for item in results:
        if "marks" in item.securityMarks:
            LOGGER.info(item.securityMarks)
            mark_dictionary = {}
            LOGGER.info(
                "clean temp mark for %s with id %s for marks %s.",
                "ASSET",
                item.name,
                marks_to_delete
            )

            for mark in marks_to_delete:
                if mark in item.securityMarks["marks"]:
                    mark_dictionary.update({ mark: item.securityMarks["marks"][mark]})
            client.remove_asset_security_mark(asset_name=item.name,
                                            mark=mark_dictionary)


def remove_temp_finding_mark(client, query_args, marks_to_delete):
    results = client.list_findings(filter_expression=query_args)
    for item in results:
        if "marks" in item.securityMarks:
            mark_dictionary = {}
            LOGGER.info(
                "clean temp mark for %s with id %s for marks %s.",
                "FINDING",
                item.name,
                marks_to_delete
            )
            finding_id = __get_finding_id(item.name)
            source_id = __get_finding_source_id(item.name)
            for mark in marks_to_delete:
                if mark in item.securityMarks["marks"]:
                    mark_dictionary.update({ mark: item.securityMarks["marks"][mark]})

            client.remove_finding_security_mark(finding_id=finding_id,
                                                source_id=source_id,
                                                security_mark=mark_dictionary)

        # awaits some time to achieve the QPS requirements in case of removing findings marks
        sleep(WAIT_TIME)

def clean_marks_by_uuid():
    #  get mark by uuid
    #  remove mark returned
    LOGGER.info("clean_marks_by_uuid wake up.")
    while QUERY_UUID_LIST:
        query_uuid = QUERY_UUID_LIST.pop()
        try:
            clean_by_uuid(query_uuid)
        except Exception as ex:
            LOGGER.error("Could not clean marks for query: %s", query_uuid)
            LOGGER.error(ex)


def clean_temp_marks():
    LOGGER.info('cleaning temporary marks')
    client = scc.Client(organization_id=ORGANIZATION_ID)

    assets = client.list_assets()
    findings = client.list_findings()

    __clean_draft_asset_marks(assets, client)
    __clean_draft_finding_marks(findings, client)


def __clean_draft_asset_marks(resources, client):
    LOGGER.info('cleaning %s', "ASSET")
    for resource in resources:
        if "marks" in resource.securityMarks:
            mark_list = {}
            for mark in resource.securityMarks["marks"]:
                if 'sccquerydrafttime' in mark and __has_time_passed(resource.securityMarks["marks"][mark]):
                    LOGGER.debug('mark [%s] will be removed', mark)
                    mark_list = {
                        mark.replace('time', ''): resource.securityMarks["marks"][mark.replace('time', '')],
                        mark: resource.securityMarks["marks"][mark]
                    }
            if mark_list:
                client.remove_asset_security_mark(asset_name=resource.name,
                                                mark=mark_list)


def __clean_draft_finding_marks(resources, client):
    LOGGER.info('cleaning %s', "FINDING")
    for resource in resources:
        if "marks" in resource.securityMarks:
            mark_list = {}
            for mark in resource.securityMarks["marks"]:
                if 'sccquerydrafttime' in mark and __has_time_passed(resource.securityMarks["marks"][mark]):
                    LOGGER.debug('mark [%s] will be removed', mark)
                    mark_list = {
                        mark.replace('time', ''): resource.securityMarks["marks"][mark.replace('time', '')],
                        mark: resource.securityMarks["marks"][mark]
                    }
                if mark_list:
                    finding_id = __get_finding_id(resource.name)
                    source_id = __get_finding_source_id(resource.name)
                    client.remove_finding_security_mark(finding_id=finding_id,
                                                        source_id=source_id,
                                                        security_mark=mark_list)



def __has_time_passed(last_time):
    return (datetime.datetime.utcnow().timestamp() - float(last_time)) > TIME_SPENT


def __get_finding_id(finding_name):
    return finding_name.split('/')[-1]


def __get_finding_source_id(finding_name):
    return finding_name.split('/')[3]
