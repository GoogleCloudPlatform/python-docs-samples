import datetime
import pytest
import os

import cleanup_service as sut

CLIENT_SEARCH_ASSETS = 'cleanup_service.scc.Client.list_assets'
CLIENT_SEARCH_FINDINGS = 'cleanup_service.scc.Client.list_findings'
CLIENT_REMOVE_ASSETS = 'cleanup_service.scc.Client.remove_asset_security_mark'
CLIENT_REMOVE_FINDING = 'cleanup_service.scc.Client.remove_finding_security_mark'
CLIENT_BUILD_SERVICE = 'cleanup_service.scc.Client._build_service'

CLIENT_GET_CREDENTIALS = os.environ.get(
    'SCC_SA_CLIENT_FILE',
    'accounts/cscc_api_client.json'
    )
EMPTY_RESULT = []


ACCOUNT_SET = pytest.mark.skipif(
    not os.path.isfile(CLIENT_GET_CREDENTIALS),
    reason='SCC account not specified'
)

@ACCOUNT_SET
def test_build_temp_maks():
    # given
    uuid = '804910119c5d4ad8b4bd143085b9d1b5'
    # when
    main_mark, time_mark = sut.build_temp_marks_keys(uuid)
    # then
    assert main_mark == 'sccquerydraft804910119c5d4ad8b4bd143085b9d1b5'
    assert time_mark == 'sccquerydrafttime804910119c5d4ad8b4bd143085b9d1b5'


@ACCOUNT_SET
def test_process_uuid_no_mark_found(mocker):
    with mocker.patch(CLIENT_BUILD_SERVICE),\
            mocker.patch(CLIENT_SEARCH_ASSETS, return_value=EMPTY_RESULT),\
            mocker.patch(CLIENT_SEARCH_FINDINGS, return_value=EMPTY_RESULT),\
            mocker.patch(CLIENT_REMOVE_ASSETS) as mock_remove_asset,\
            mocker.patch(CLIENT_REMOVE_FINDING) as mock_remove_finding:
        # when
        sut.clean_marks_by_uuid()
        # then
        mock_remove_asset.assert_not_called()
        mock_remove_finding.assert_not_called()


@ACCOUNT_SET
def test_process_uuid_mark_found_in_asset(mocker):
    # given
    uuid = '804910119c5d4ad8b4bd143085b9d1b5'
    asset_name = 'organizations/1055058813388/assets/6848586495725745982'
    main_mark, time_mark = sut.build_temp_marks_keys(uuid)
    scc_marks = {main_mark: "true", time_mark: "true"}
    mock_assets_results = [MockAsset(asset_name,
                                     scc_marks,
                                     securityMarks={"marks": scc_marks})]

    sut.add_to_be_processed(uuid)

    with mocker.patch(CLIENT_BUILD_SERVICE),\
            mocker.patch(CLIENT_SEARCH_ASSETS, return_value=mock_assets_results),\
            mocker.patch(CLIENT_SEARCH_FINDINGS, return_value=EMPTY_RESULT),\
            mocker.mock_module.patch(CLIENT_REMOVE_ASSETS) as mock_remove_asset,\
            mocker.mock_module.patch(CLIENT_REMOVE_FINDING) as mock_remove_finding:
        # when
        sut.clean_marks_by_uuid()
        # then
        mock_remove_asset.assert_any_call(
            asset_name=asset_name,
            mark=scc_marks
        )
     
        mock_remove_finding.assert_not_called()


@ACCOUNT_SET
def test_process_uuid_mark_found_in_finding(mocker):
    # given
    uuid = '804910119c5d4ad8b4bd143085b9d1b5'
    finding_id = 'u5gh9794guthg47940001'
    source_id = '10711839371761827624'
    finding_name = "organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001"
    main_mark, time_mark = sut.build_temp_marks_keys(uuid)
    scc_marks = {main_mark: "true", time_mark: "true"}

    mock_findings_results = [MockFinding(finding_name,
                                         scc_marks,
                                         securityMarks={"marks": scc_marks})]

    sut.add_to_be_processed(uuid)

    with mocker.patch(CLIENT_BUILD_SERVICE),\
            mocker.patch(CLIENT_SEARCH_ASSETS, return_value=EMPTY_RESULT),\
            mocker.patch(CLIENT_SEARCH_FINDINGS, return_value=mock_findings_results),\
            mocker.mock_module.patch(CLIENT_REMOVE_ASSETS) as mock_remove_asset,\
            mocker.mock_module.patch(CLIENT_REMOVE_FINDING) as mock_remove_finding:
        # when
        sut.clean_marks_by_uuid()
        # then
        mock_remove_finding.assert_any_call(
            source_id=source_id,
            finding_id=finding_id,
            security_mark=scc_marks
        )
        mock_remove_asset.assert_not_called()


@ACCOUNT_SET
def test_process_all_marks_found_in_finding_and_assets_way_in_the_past(mocker):
    # given
    uuid = '804910119c5d4ad8b4bd143085b9d1b5'
    finding_id = 'u5gh9794guthg47940001'
    source_id = '10711839371761827624'
    asset_name = 'organizations/1055058813388/assets/6848586495725745982'
    finding_name = "organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001"
    main_mark, time_mark = sut.build_temp_marks_keys(uuid)

    # Thursday, November 29, 1973 9:33:09 PM
    really_old_timestamp = '123456789'
    scc_marks = {
        main_mark: 'true',
        time_mark: really_old_timestamp
    }
    mock_assets_results = [MockAsset(resourceName=asset_name,
                                     marks=scc_marks,
                                     securityMarks={"marks": scc_marks})]
    mock_findings_results = [MockFinding(resourceName=finding_name,
                                         marks=scc_marks,
                                         securityMarks={"marks": scc_marks})]
    #scc_marks = [main_mark, time_mark]
    with mocker.patch(CLIENT_BUILD_SERVICE),\
            mocker.patch(CLIENT_SEARCH_ASSETS, return_value=mock_assets_results),\
            mocker.patch(CLIENT_SEARCH_FINDINGS, return_value=mock_findings_results),\
            mocker.mock_module.patch(CLIENT_REMOVE_ASSETS) as mock_remove_asset,\
            mocker.mock_module.patch(CLIENT_REMOVE_FINDING) as mock_remove_finding:
        # when
        sut.clean_temp_marks()
        # then
        mock_remove_finding.assert_any_call(
            source_id=source_id,
            finding_id=finding_id,
            security_mark=scc_marks
        )
        mock_remove_asset.assert_any_call(
            asset_name=asset_name,
            mark=scc_marks
        )


@ACCOUNT_SET
def test_process_all_marks_found_in_finding_and_assets_still_fresh(mocker):
    # given
    uuid = '804910119c5d4ad8b4bd143085b9d1b5'
    asset_name = 'organizations/1055058813388/assets/6848586495725745982'
    finding_name = "organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001"
    main_mark, time_mark = sut.build_temp_marks_keys(uuid)
    # Current date UTC
    utc_now_timestamp = str(datetime.datetime.utcnow().timestamp())
    scc_marks = {
        main_mark: 'true',
        time_mark: utc_now_timestamp
    }

    mock_assets_results = [MockAsset(asset_name,
                                     scc_marks,
                                     securityMarks={"marks": scc_marks})]
    mock_findings_results = [MockFinding(finding_name,
                                         scc_marks,
                                         securityMarks={"marks": scc_marks})]

    with mocker.patch(CLIENT_BUILD_SERVICE),\
            mocker.patch(CLIENT_SEARCH_ASSETS, return_value=mock_assets_results),\
            mocker.patch(CLIENT_SEARCH_FINDINGS, return_value=mock_findings_results),\
            mocker.mock_module.patch(CLIENT_REMOVE_ASSETS) as mock_remove_asset,\
            mocker.mock_module.patch(CLIENT_REMOVE_FINDING) as mock_remove_finding:
        # when
        sut.clean_temp_marks()
        # then
        mock_remove_finding.assert_not_called()
        mock_remove_asset.assert_not_called()


class MockAsset:
    def __init__(self, resourceName, marks, securityMarks=None):
        self.name = resourceName
        self.marks = marks
        self.securityMarks = securityMarks


class MockFinding:
    def __init__(self, resourceName, marks, securityMarks=None):
        self.name = resourceName
        self.marks = marks
        self.securityMarks = securityMarks
