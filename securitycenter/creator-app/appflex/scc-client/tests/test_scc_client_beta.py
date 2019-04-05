import os

import pytest

import client.scc_client_beta as beta

# @pytest.hookimpl(tryfirst=True)
# def pytest_collection_modifyitems(item):
#     print('before')
#     os.environ['SCC_CLIENT_DEVELOPER_KEY'] = '123456'

ACCOUNT_SET = pytest.mark.skipif(
    not os.path.isfile(os.environ.get(
        'SCC_SA_CLIENT_FILE',
        'accounts/cscc_api_client.json'
    )),
    reason='SCC account not specified'
)


@ACCOUNT_SET
def test_return_empty_if_there_is_no_assets(mocker):
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute') \
            as mock:
        # when
        result = scc_client.list_assets()

        # then
        mock.assert_called()
        assert result == []


@ACCOUNT_SET
def test_list_assets(mocker):
    # given
    organization_id = '1055058813388'
    scc_client = beta.Client(organization_id, default_max_pages=3)
    asset_id = '16098821301900709014'
    name = 'organizations/{}/assets/{}'.format(organization_id, asset_id)
    security_center_properties = {
        "resourceName": "//compute.googleapis.com/projects/akoclsecteamcom-dns-control/zones/us-central1-b/instances/deploy-machine",
        "resourceType": "google.compute.Instance",
        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/345653786583",
        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/345653786583",
        "resourceOwners": [
            "user:amandak@clsecteam.com"
        ]
    }
    resource_properties = {
        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
        "labelFingerprint": "42wmspb8rsm=",
        "creationTimestamp": "2018-03-13t13:52:31.557-07:00",
        "serviceAccount": "[{\"email\":\"345653786583-compute@developer.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/cloud-platform\"]}]",
        "name": "deploy-machine",
        "machineType": "https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/zones/us-central1-b/machinetypes/n1-standard-1",
        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"deploy-machine\",\"guestOsFeature\":[{\"type\":\"VIRTIO_SCSI_MULTIQUEUE\"}],\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/debian-cloud/global/licenses/debian-9-stretch\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/zones/us-central1-b/disks/deploy-machine\",\"type\":\"PERSISTENT\"}]",
        "tags": "{\"fingerprint\":\"42WmSpB8rSM=\"}",
        "canIpForward": False,
        "networkInterface": "[{\"accessConfig\":[{\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"s6A9Sc4l+Mc=\",\"ipAddress\":\"10.128.0.2\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/regions/us-central1/subnetworks/default\"}]",
        "zone": "https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/zones/us-central1-b",
        "cpuPlatform": "unknown cpu platform",
        "deletionProtection": False,
        "selfLink": "https://www.googleapis.com/compute/v1/projects/akoclsecteamcom-dns-control/zones/us-central1-b/instances/deploy-machine",
        "startRestricted": False,
        "status": "terminated",
        "id": "2701343270994543841"
    }
    security_marks = {
        "name": name+"/securityMarks"
    }
    create_time = '2018-10-23T17:17:03.783Z'
    update_time = '2018-10-23T17:17:03.783Z'
    state = 'UNUSED'
    filter_expression = 'securityCenterProperties.resourceType : "INSTANCE" \
        AND resourceProperties.name: "deploy-machine" AND \
        securityCenterProperties.resourceName: "akoclsecteamcom-dns-control"'
    json = mock_list_assets(name, security_center_properties,
                            resource_properties, security_marks,
                            create_time, update_time, state)

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_response(json, size=1)) \
            as mock:
        # when
        assets = scc_client.list_assets(filter_expression=filter_expression)

        # then
        mock.assert_called()
        assert assets[0].name == name
        assert assets[0].securityCenterProperties == security_center_properties
        assert assets[0].resourceProperties == resource_properties
        assert assets[0].securityMarks == security_marks
        assert assets[0].createTime == create_time
        assert assets[0].updateTime == update_time
        assert assets[0].state == state


@ACCOUNT_SET
def test_state_added_for_assets_network_created_eight_hours_from_execution_time(mocker):
    # given
    organization_id = '1055058813388'
    asset_type = '"google.compute.Network"'
    execution_time = '2018-03-17T14:00:00.0Z'
    # 8 hours in seconds
    duration = '28800s'
    scc_client = beta.Client(organization_id, default_max_pages=3)

    json = mock_asset_network_state_active_and_added()
    json_size = 4

    query = 'filter=securityCenterProperties.resourceType = {}&readTime={}&' \
            'compare_duration={}'.format(asset_type, execution_time, duration)

    # when
    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_response(json, json_size)) \
            as mock:

        assets = scc_client.list_assets(query)

        # then
        assert len(assets) == json_size

        added_assets = [asset for asset in assets if asset.state == 'ADDED']
        mock.assert_called()

        assert len(added_assets) == 2
        assert added_assets[0].state == 'ADDED'
        assert added_assets[1].state == 'ADDED'


@ACCOUNT_SET
def test_list_findings(mocker):
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)
    name = "organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001"
    parent = "organizations/1055058813388/sources/10711839371761827624"
    resourceName = "organizations/1055058813388/assets/16712790543092542367"
    state = "ACTIVE"
    category = "PROJECT_ACCESS"
    externalUri = "https://console.cloud.google.com"
    sourceProperties = {
        "scc_environment": "hackathon"
    }
    securityMarks = {
        "name": "organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001/securityMarks"
    }
    eventTime = "2018-10-30T12:27:43Z"
    createTime = "2018-10-30T12:27:43Z"
    json = mock_list_findings(name, parent, resourceName, state, category,
                              externalUri, sourceProperties, securityMarks,
                              eventTime, createTime)

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_response(json, size=1)) \
            as mock:
        # when
        findings = scc_client.list_findings()

        # then
        mock.assert_called()
        assert findings[0].name == name
        assert findings[0].parent == parent
        assert findings[0].resourceName == resourceName
        assert findings[0].state == state
        assert findings[0].category == category
        assert findings[0].externalUri == externalUri
        assert findings[0].sourceProperties == sourceProperties
        assert findings[0].securityMarks == securityMarks
        assert findings[0].eventTime == eventTime
        assert findings[0].createTime == createTime


@ACCOUNT_SET
def test_list_findings_from_instances_with_specific_ports_allowed_on_firewall(mocker):
    # given element values
    from_port = 0
    to_port = 65535
    asset_firewall_resource_type = 'Firewall'
    asset_instance_resource_type = 'google.compute.Instance'
    finding_category = 'CONTAINER_RUNTIME_ANOMALY'

    organization_id = '1055058813388'

    # given queries
    asset_firewall_query = 'filter=securityCenterProperties.resourceType : "{}"  AND ' \
                           'resourceProperties.allowed : "{}-{}"'.format(asset_firewall_resource_type, from_port, to_port)
    asset_instances_query = 'filter=securityCenterProperties.resourceType = "{}" AND ' \
                            'securityCenterProperties.resourceParent = "//cloudresourcemanager.googleapis.com/projects/138150943629" OR ' \
                            'securityCenterProperties.resourceParent = "//cloudresourcemanager.googleapis.com/projects/246054159221" OR ' \
                            'securityCenterProperties.resourceParent = "//cloudresourcemanager.googleapis.com/projects/808630039469"'.format(asset_instance_resource_type)
    finding_query = 'category = "{}" AND ' \
                    'resourceName = "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-b/instances/aef-default-20180222t230228-s7wk" OR ' \
                    'resourceName = "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-c/instances/aef-default-1-qgk7" OR ' \
                    'resourceName = "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-f/instances/aef-default-20180222t230228-1rb9"'.format(finding_category)

    scc_client = beta.Client(organization_id, default_max_pages=3)
    json = mock_finding_category()
    json_size = 1

    # when 3 step query (ASSET - ASSET - FINDING)
    with mocker.mock_module.patch(
            'googleapiclient.http.HttpRequest.execute',
            return_value=mock_asset_firewall_allowed_ports()) as mock:
        scc_client.list_assets(asset_firewall_query)

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_asset_instances()) as mock:
        scc_client.list_assets(asset_instances_query)

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_response(json, json_size)) \
                as mock:
        findings = scc_client.list_findings('-', finding_query)

    # then
    mock.assert_called()
    assert json_size == len(findings)
    assert findings


@ACCOUNT_SET
def test_list_findings_from_projects_of_different_sources(mocker):
    # given
    dome9_source_id = 'organizations/688851828130/sources/9300364871731100004'
    redlock_source_id = 'organizations/688851828130/sources/250821172470083347'
    organization_id = '1055058813388'

    # given query
    query = 'parent = {} OR parent = {} AND ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/8604840416" OR ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/760319584329" OR ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/581282749270" OR ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/387457489797" OR ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/635775969782" OR ' \
            'resourceName = "//cloudresourcemanager.googleapis.com/projects/685140108503"'\
        .format(dome9_source_id, redlock_source_id)

    scc_client = beta.Client(organization_id, default_max_pages=3)

    json = mock_finding_sources()
    json_size = 4

    # when
    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_response(json, json_size)) \
            as mock:
        findings = scc_client.list_findings()

        # then
        mock.assert_called()
        assert json_size == len(findings)
        assert findings


@ACCOUNT_SET
def test_create_finding(mocker):
    # given
    organization_id = '1055058813388'
    scc_client = beta.Client(organization_id, default_max_pages=3)
    source_id = '10711839371761827624'
    finding_id = 'a0a0a0a0a0b8'
    category = 'test_category'
    name = "organizations/{}/sources/{}/findings/{}".format(organization_id,
                                                            source_id,
                                                            finding_id)
    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute',
                                  return_value=mock_create_finding()) as mock:
        # when
        result = scc_client.create_finding(source_id, finding_id, category)

        # then
        mock.assert_called()
        finding = beta.Finding(result)

        assert finding.name == name
        assert finding.category == category
        assert finding.state == 'ACTIVE'
        assert finding.eventTime == "2018-11-05T18:15:51.012971Z"


@ACCOUNT_SET
@pytest.mark.xfail(raises=TypeError)
def test_required_asset_id_when_update_asset_security_mark():
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)
    asset_id = ''
    security_marks_map = {
        'scc_beta_client_test': 'test'
    }

    # when
    scc_client.update_asset_security_mark(security_marks_map, asset_id=asset_id)

    # then
    # expect TypeError: Parameter "name" value does not match the
    # pattern "^organizations/[^/]+/assets/[^/]+/securityMarks$"


@ACCOUNT_SET
def test_update_asset_security_mark(mocker):
    # given
    organization_id = '1055058813388'
    scc_client = beta.Client(organization_id, default_max_pages=3)
    asset_id = '11712741160732498783'
    security_marks_map = {
        'scc_beta_client_test': 'test'
    }
    name = "organizations/{}/assets/{}/securityMarks".format(organization_id,
                                                             asset_id)
    with mocker.mock_module.patch(
            'googleapiclient.http.HttpRequest.execute',
            return_value=mock_update_asset_security_mark()) as mock:
        # when
        result = scc_client.update_asset_security_mark(security_marks_map,
                                                       asset_id=asset_id)
        # then
        mock.assert_called()
        assert result.get('name') == name
        assert result.get('marks') == security_marks_map


@ACCOUNT_SET
def test_remove_asset_security_mark():
    # https: // securitycenter.googleapis.com / v1beta1 / organizations / 1055058813388 / sources / 10711839371761827624 / findings / u5gh9794guthg47940001 / securityMarks?updateMask = marks.betaapi
    # https: // securitycenter.googleapis.com / v1beta1 / organizations / 1055058813388 / assets / 16098821301900709014 / securityMarks?updateMask = marks.testX
    organization_id = '1055058813388'
    scc_client = beta.Client(organization_id, default_max_pages=3)
    asset_id = '16098821301900709014'
    mark = 'testX'

    # when
    result = scc_client.remove_asset_security_mark(asset_id, mark)

    print(result)


@ACCOUNT_SET
@pytest.mark.xfail(raises=TypeError)
def test_required_finding_id_when_update_finding_security_mark():
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)
    finding_id = ''
    source_id = '9264282320680000000'
    security_marks_map = {
        'scc_beta_client_test': 'test'
    }

    # when
    scc_client.update_finding_security_mark(security_marks_map,
                                            source_id=source_id,
                                            finding_id=finding_id)

    # then
    # assert TypeError: Parameter "name" value does not match the pattern
    # "^organizations/[^/]+/sources/[^/]+/findings/[^/]+/securityMarks$"


@ACCOUNT_SET
@pytest.mark.xfail(raises=TypeError)
def test_required_source_id_when_update_finding_security_mark():
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)
    finding_id = 'u5gh9794guthg47940001'
    source_id = ''
    security_marks_map = {
        'scc_beta_client_test': 'test'
    }

    # when
    scc_client.update_finding_security_mark(security_marks_map,
                                            source_id=source_id,
                                            finding_id=finding_id)

    # then assert TypeError: Parameter "name" value does not match the pattern
    # "^organizations/[^/]+/sources/[^/]+/findings/[^/]+/securityMarks$"


@ACCOUNT_SET
def test_update_finding_security_mark(mocker):
    # given
    organization_id = '1055058813388'
    scc_client = beta.Client(organization_id, default_max_pages=3)
    finding_id = 'u5gh9794guthg47940001'
    source_id = '10711839371761827624'
    security_marks_map = {
        'scc_beta_client_test': 'test_mark'
    }
    name = 'organizations/{}/sources/{}/findings/{}/securityMarks'.format(
        organization_id,
        source_id,
        finding_id)
    with mocker.mock_module.patch(
            'googleapiclient.http.HttpRequest.execute',
            return_value=mock_update_finding_security_mark()) as mock:
        # when
        result = scc_client.update_finding_security_mark(security_marks_map,
                                                         source_id=source_id,
                                                         finding_id=finding_id)
        # then
        mock.assert_called()
        assert result.get('name') == name
        assert result.get('marks') == security_marks_map


@ACCOUNT_SET
def test_remove_finding_security_mark(mocker):
    # given
    scc_client = beta.Client('1055058813388', default_max_pages=3)
    finding_id = 'u5gh9794guthg47940001'
    source_id = '10711839371761827624'
    security_marks_map = {
        'scc_beta_client_test': 'test_mark'
    }

    with mocker.mock_module.patch('googleapiclient.http.HttpRequest.execute') \
            as mock:
        # when
        result = scc_client.remove_finding_security_mark(security_marks_map,
                                                         source_id=source_id,
                                                         finding_id=finding_id)
        # then
        mock.assert_called()
        assert result


class HttpResponseMock(object):

    def __init__(self, mock_payload=None, size=50):
        self.json = mock_payload
        self.size = size

    def get(self, desc, value=0):
        if desc == 'totalSize':
            return self.size
        elif desc == 'listAssetsResults' or desc == 'findings':
            return self.json


def mock_response(mock_payload=None, size=None):
    return HttpResponseMock(mock_payload, size)


def mock_list_assets(name, securityCenterProperties, resourceProperties,
                     securityMarks, createTime, updateTime, state):
    return [{
        "asset": {
            "name": name,
            "securityCenterProperties": securityCenterProperties,
            "resourceProperties": resourceProperties,
            "securityMarks": securityMarks,
            "createTime": createTime,
            "updateTime": updateTime
        },
        "state": state
    }]


def mock_list_findings(name, parent, resourceName, state, category,
                       externalUri, sourceProperties, securityMarks,
                       eventTime, createTime):
    return [{
        "name": name,
        "parent": parent,
        "resourceName": resourceName,
        "state": state,
        "category": category,
        "externalUri": externalUri,
        "sourceProperties": sourceProperties,
        "securityMarks": securityMarks,
        "eventTime": eventTime,
        "createTime": createTime
    }]


def mock_create_finding():
    return {
        "name": "organizations/1055058813388/sources/10711839371761827624/findings/a0a0a0a0a0b8",
        "parent": "organizations/1055058813388/sources/10711839371761827624",
        "state": "ACTIVE",
        "category": "test_category",
        "securityMarks": {
            "name": "organizations/1055058813388/sources/10711839371761827624/findings/a0a0a0a0a0b8/securityMarks"
        },
        "eventTime": "2018-11-05T18:15:51.012971Z",
        "createTime": "2018-11-05T18:15:51.012971Z"
    }


def mock_update_finding_security_mark():
    return {
        'name': 'organizations/1055058813388/sources/10711839371761827624/findings/u5gh9794guthg47940001/securityMarks',
        'marks': {
            'scc_beta_client_test': 'test_mark'
        }
    }


def mock_update_asset_security_mark():
    return {
        "marks": {
            "scc_beta_client_test": "test",
        },
        "name": "organizations/1055058813388/assets/11712741160732498783/securityMarks"
    }


def mock_asset_firewall_allowed_ports():
    return {
        "listAssetsResults": [
            {
                "asset": {
                    "name": "organizations/688851828130/assets/650853799622838538",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/asset-dev-project/global/firewalls/default-allow-internal",
                        "resourceType": "google.compute.Firewall",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceOwners": [
                            "user:dandrade@gcp-sec-demo-org.joonix.net",
                            "user:lucasbr@gcp-sec-demo-org.joonix.net",
                            "user:walves@gcp-sec-demo-org.joonix.net"
                        ]
                    },
                    "resourceProperties": {
                        "sourceRange": "[\"10.128.0.0/9\"]",
                        "creationTimestamp": "2018-02-22t05:51:30.438-08:00",
                        "name": "default-allow-internal",
                        "direction": "ingress",
                        "description": "allow internal traffic on the default network",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/firewalls/default-allow-internal",
                        "priority": 65534,
                        "allowed": "[{\"ipProtocol\":\"tcp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"udp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"icmp\"}]",
                        "disabled": "false",
                        "network": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default",
                        "id": "7392811674201453581"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/650853799622838538/securityMarks",
                        "marks": {
                            "environment": "development",
                            "scc_query_3891e95b-403d-44b3-ad62-6678abbeea12": "true"
                        }
                    },
                    "createTime": "2018-08-01T10:45:32.791Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/10855669941519462085",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/bin-auth-playground/global/firewalls/default-allow-internal",
                        "resourceType": "google.compute.Firewall",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/246054159221",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/246054159221",
                        "resourceOwners": [
                            "user:andychang@google.com"
                        ]
                    },
                    "resourceProperties": {
                        "sourceRange": "[\"10.128.0.0/9\"]",
                        "creationTimestamp": "2018-09-24t14:19:08.097-07:00",
                        "name": "default-allow-internal",
                        "description": "allow internal traffic on the default network",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/bin-auth-playground/global/firewalls/default-allow-internal",
                        "priority": 65534,
                        "allowed": "[{\"ipProtocol\":\"tcp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"udp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"icmp\"}]",
                        "disabled": "false",
                        "network": "https://www.googleapis.com/compute/v1/projects/bin-auth-playground/global/networks/default",
                        "direction": "ingress",
                        "id": "3927342531763038755"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/10855669941519462085/securityMarks"
                    },
                    "createTime": "2018-10-17T22:03:23.376Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/1480242085031720440",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/global/firewalls/default-allow-internal",
                        "resourceType": "google.compute.Firewall",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceOwners": [
                            "user:andychang@google.com"
                        ]
                    },
                    "resourceProperties": {
                        "sourceRange": "[\"10.128.0.0/9\"]",
                        "creationTimestamp": "2018-09-24t14:10:38.195-07:00",
                        "name": "default-allow-internal",
                        "description": "allow internal traffic on the default network",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/firewalls/default-allow-internal",
                        "priority": 65534,
                        "allowed": "[{\"ipProtocol\":\"tcp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"udp\",\"port\":[\"0-65535\"]},{\"ipProtocol\":\"icmp\"}]",
                        "disabled": "false",
                        "network": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/default",
                        "direction": "ingress",
                        "id": "7704448539799383073"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/1480242085031720440/securityMarks"
                    },
                    "createTime": "2018-09-26T06:14:09.800Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            }
        ]
    }


def mock_asset_instances():
    return {
        "listAssetsResults": [
            {
                "asset": {
                    "name": "organizations/688851828130/assets/8549367430367362526",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-b/instances/aef-default-1-vvnn",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceOwners": [
                            "user:dandrade@gcp-sec-demo-org.joonix.net",
                            "user:lucasbr@gcp-sec-demo-org.joonix.net",
                            "user:walves@gcp-sec-demo-org.joonix.net"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "ftozzgdzr9o=",
                        "creationTimestamp": "2018-11-08t07:01:30.233-08:00",
                        "serviceAccount": "[{\"email\":\"asset-dev-project@appspot.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/appengine.apis\",\"https://www.googleapis.com/auth/cloud-platform\",\"https://www.googleapis.com/auth/devstorage.full_control\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/userinfo.email\"]}]",
                        "name": "aef-default-1-vvnn",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/machinetypes/custom-1-1024",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"boot\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/goog-vmruntime-images/global/licenses/appengine-flex-grandfathered\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/disks/aef-default-1-vvnn\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"Sn0ni+rLoFQ=\",\"tag\":[\"aef-default-1\"]}",
                        "labels": "{\"goog-aef-service-name\":\"default\",\"goog-aef-service-version\":\"1\"}",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.239.184.234\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"y36tElXFz+g=\",\"ipAddress\":\"10.128.0.4\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b",
                        "cpuPlatform": "intel haswell",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/instances/aef-default-1-vvnn",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "1019681803025903910"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/8549367430367362526/securityMarks"
                    },
                    "createTime": "2018-11-09T14:42:52.490Z",
                    "updateTime": "2018-11-09T14:42:52.490Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/15808082664009662130",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-b/instances/aef-default-20180222t230228-s7wk",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceOwners": [
                            "user:dandrade@gcp-sec-demo-org.joonix.net",
                            "user:lucasbr@gcp-sec-demo-org.joonix.net",
                            "user:walves@gcp-sec-demo-org.joonix.net"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "p4gki06nsng=",
                        "creationTimestamp": "2018-11-08t12:57:49.589-08:00",
                        "serviceAccount": "[{\"email\":\"asset-dev-project@appspot.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/appengine.apis\",\"https://www.googleapis.com/auth/cloud-platform\",\"https://www.googleapis.com/auth/devstorage.full_control\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/userinfo.email\"]}]",
                        "name": "aef-default-20180222t230228-s7wk",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/machinetypes/custom-1-1024",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"boot\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/goog-vmruntime-images/global/licenses/appengine-flex-grandfathered\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/disks/aef-default-20180222t230228-s7wk\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"5H0YU3GxdPU=\",\"tag\":[\"aef-default-20180222t230228\"]}",
                        "labels": "{\"goog-aef-service-name\":\"default\",\"goog-aef-service-version\":\"20180222t230228\"}",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.232.191.154\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"/zhG8hrT/74=\",\"ipAddress\":\"10.128.0.5\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b",
                        "cpuPlatform": "intel haswell",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-b/instances/aef-default-20180222t230228-s7wk",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "4624056960995106213"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/15808082664009662130/securityMarks"
                    },
                    "createTime": "2018-11-09T14:42:52.490Z",
                    "updateTime": "2018-11-09T14:42:52.490Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/11090808372097575537",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-c/instances/aef-default-1-qgk7",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceOwners": [
                            "user:dandrade@gcp-sec-demo-org.joonix.net",
                            "user:lucasbr@gcp-sec-demo-org.joonix.net",
                            "user:walves@gcp-sec-demo-org.joonix.net"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "ftozzgdzr9o=",
                        "creationTimestamp": "2018-11-08t06:53:41.282-08:00",
                        "serviceAccount": "[{\"email\":\"asset-dev-project@appspot.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/appengine.apis\",\"https://www.googleapis.com/auth/cloud-platform\",\"https://www.googleapis.com/auth/devstorage.full_control\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/userinfo.email\"]}]",
                        "name": "aef-default-1-qgk7",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-c/machinetypes/custom-1-1024",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"boot\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/goog-vmruntime-images/global/licenses/appengine-flex-grandfathered\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-c/disks/aef-default-1-qgk7\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"Sn0ni+rLoFQ=\",\"tag\":[\"aef-default-1\"]}",
                        "labels": "{\"goog-aef-service-name\":\"default\",\"goog-aef-service-version\":\"1\"}",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.192.122.71\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"1p8vg+A4an0=\",\"ipAddress\":\"10.128.0.3\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-c",
                        "cpuPlatform": "intel haswell",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-c/instances/aef-default-1-qgk7",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "3666986952928391963"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/11090808372097575537/securityMarks"
                    },
                    "createTime": "2018-11-09T14:42:52.490Z",
                    "updateTime": "2018-11-09T14:42:52.490Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/16730332267438903747",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/asset-dev-project/zones/us-central1-f/instances/aef-default-20180222t230228-1rb9",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                        "resourceOwners": [
                            "user:dandrade@gcp-sec-demo-org.joonix.net",
                            "user:lucasbr@gcp-sec-demo-org.joonix.net",
                            "user:walves@gcp-sec-demo-org.joonix.net"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "p4gki06nsng=",
                        "creationTimestamp": "2018-11-08t13:03:53.673-08:00",
                        "serviceAccount": "[{\"email\":\"asset-dev-project@appspot.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/appengine.apis\",\"https://www.googleapis.com/auth/cloud-platform\",\"https://www.googleapis.com/auth/devstorage.full_control\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/userinfo.email\"]}]",
                        "name": "aef-default-20180222t230228-1rb9",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-f/machinetypes/custom-1-1024",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"boot\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/goog-vmruntime-images/global/licenses/appengine-flex-grandfathered\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-f/disks/aef-default-20180222t230228-1rb9\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"5H0YU3GxdPU=\",\"tag\":[\"aef-default-20180222t230228\"]}",
                        "labels": "{\"goog-aef-service-name\":\"default\",\"goog-aef-service-version\":\"20180222t230228\"}",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.188.10.113\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"zBWRPYmH9c4=\",\"ipAddress\":\"10.128.0.2\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-f",
                        "cpuPlatform": "intel ivy bridge",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/zones/us-central1-f/instances/aef-default-20180222t230228-1rb9",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "4329772124065045079"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/16730332267438903747/securityMarks"
                    },
                    "createTime": "2018-11-09T14:42:52.490Z",
                    "updateTime": "2018-11-09T14:42:52.490Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/4912831810690827275",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-tcjv",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceOwners": [
                            "user:andychang@google.com"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "2ixrno2sgum=",
                        "creationTimestamp": "2018-09-24t17:02:54.668-07:00",
                        "serviceAccount": "[{\"email\":\"808630039469-compute@developer.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/devstorage.read_only\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/monitoring\",\"https://www.googleapis.com/auth/service.management.readonly\",\"https://www.googleapis.com/auth/servicecontrol\",\"https://www.googleapis.com/auth/trace.append\"]}]",
                        "name": "gke-bin-auth-demo-cluste-default-pool-da672324-tcjv",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/machinetypes/n1-standard-1",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"persistent-disk-0\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/cos-cloud/global/licenses/cos\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/disks/gke-bin-auth-demo-cluste-default-pool-da672324-tcjv\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"Uu9IMkz5Xr4=\",\"tag\":[\"gke-bin-auth-demo-cluster-5dd7583a-node\"]}",
                        "labels": "{\"goog-gke-node\":\"\"}",
                        "canIpForward": "true",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"104.198.71.65\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"B7J3xWoh100=\",\"ipAddress\":\"10.128.0.4\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a",
                        "cpuPlatform": "intel sandy bridge",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-tcjv",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "2561507433730328003"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/4912831810690827275/securityMarks"
                    },
                    "createTime": "2018-10-16T22:11:19.925Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/7789062843971036188",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-870f",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceOwners": [
                            "user:andychang@google.com"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "2ixrno2sgum=",
                        "creationTimestamp": "2018-09-24t17:02:53.950-07:00",
                        "serviceAccount": "[{\"email\":\"808630039469-compute@developer.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/devstorage.read_only\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/monitoring\",\"https://www.googleapis.com/auth/service.management.readonly\",\"https://www.googleapis.com/auth/servicecontrol\",\"https://www.googleapis.com/auth/trace.append\"]}]",
                        "name": "gke-bin-auth-demo-cluste-default-pool-da672324-870f",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/machinetypes/n1-standard-1",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"persistent-disk-0\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/cos-cloud/global/licenses/cos\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/disks/gke-bin-auth-demo-cluste-default-pool-da672324-870f\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"Uu9IMkz5Xr4=\",\"tag\":[\"gke-bin-auth-demo-cluster-5dd7583a-node\"]}",
                        "labels": "{\"goog-gke-node\":\"\"}",
                        "canIpForward": "true",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.194.44.209\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"0iTRDzhebe8=\",\"ipAddress\":\"10.128.0.2\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a",
                        "cpuPlatform": "intel sandy bridge",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-870f",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "7749059858296784323"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/7789062843971036188/securityMarks"
                    },
                    "createTime": "2018-10-16T22:11:19.925Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            },
            {
                "asset": {
                    "name": "organizations/688851828130/assets/8450780238350708758",
                    "securityCenterProperties": {
                        "resourceName": "//compute.googleapis.com/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-kqq4",
                        "resourceType": "google.compute.Instance",
                        "resourceParent": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceProject": "//cloudresourcemanager.googleapis.com/projects/808630039469",
                        "resourceOwners": [
                            "user:andychang@google.com"
                        ]
                    },
                    "resourceProperties": {
                        "scheduling": "{\"automaticRestart\":true,\"onHostMaintenance\":\"MIGRATE\",\"preemptible\":false}",
                        "labelFingerprint": "2ixrno2sgum=",
                        "creationTimestamp": "2018-09-24t17:02:54.479-07:00",
                        "serviceAccount": "[{\"email\":\"808630039469-compute@developer.gserviceaccount.com\",\"scope\":[\"https://www.googleapis.com/auth/devstorage.read_only\",\"https://www.googleapis.com/auth/logging.write\",\"https://www.googleapis.com/auth/monitoring\",\"https://www.googleapis.com/auth/service.management.readonly\",\"https://www.googleapis.com/auth/servicecontrol\",\"https://www.googleapis.com/auth/trace.append\"]}]",
                        "name": "gke-bin-auth-demo-cluste-default-pool-da672324-kqq4",
                        "machineType": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/machinetypes/n1-standard-1",
                        "disk": "[{\"autoDelete\":true,\"boot\":true,\"deviceName\":\"persistent-disk-0\",\"index\":0,\"interface\":\"SCSI\",\"license\":[\"https://www.googleapis.com/compute/v1/projects/cos-cloud/global/licenses/cos\"],\"mode\":\"READ_WRITE\",\"source\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/disks/gke-bin-auth-demo-cluste-default-pool-da672324-kqq4\",\"type\":\"PERSISTENT\"}]",
                        "tags": "{\"fingerprint\":\"Uu9IMkz5Xr4=\",\"tag\":[\"gke-bin-auth-demo-cluster-5dd7583a-node\"]}",
                        "labels": "{\"goog-gke-node\":\"\"}",
                        "canIpForward": "true",
                        "networkInterface": "[{\"accessConfig\":[{\"externalIp\":\"35.193.197.237\",\"name\":\"external-nat\",\"networkTier\":\"PREMIUM\",\"type\":\"ONE_TO_ONE_NAT\"}],\"fingerprint\":\"RolpgYWVe9c=\",\"ipAddress\":\"10.128.0.3\",\"name\":\"nic0\",\"network\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/global/networks/default\",\"subnetwork\":\"https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/regions/us-central1/subnetworks/default\"}]",
                        "zone": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a",
                        "cpuPlatform": "intel sandy bridge",
                        "deletionProtection": "false",
                        "selfLink": "https://www.googleapis.com/compute/v1/projects/binary-authorization-demo/zones/us-central1-a/instances/gke-bin-auth-demo-cluste-default-pool-da672324-kqq4",
                        "startRestricted": "false",
                        "status": "running",
                        "id": "8094363787102307779"
                    },
                    "securityMarks": {
                        "name": "organizations/688851828130/assets/8450780238350708758/securityMarks"
                    },
                    "createTime": "2018-10-16T22:11:19.925Z",
                    "updateTime": "2018-10-17T22:03:23.376Z"
                },
                "state": "UNUSED"
            }
        ],
        "readTime": "2018-11-11T18:59:15.906Z",
        "totalSize": 7
    }


def mock_finding_category():
    return [
            {
                "name": "organizations/688851828130/sources/10525437515560121179/findings/ac785971e7024c609d91f47211519d3e",
                "parent": "organizations/688851828130/sources/10525437515560121179",
                "resourceName": "//compute.googleapis.com/projects/container-security-demo/zones/us-central1-a/instances/gke-cluster-sec-demo-tar-default-pool-0dfce3bb-mnrn",
                "state": "ACTIVE",
                "category": "CONTAINER_RUNTIME_ANOMALY-HIGH_RISK_IP",
                "externalUri": "http://35.197.45.209:8081/#!/login",
                "sourceProperties": {
                    "host": "liron-srv",
                    "sccCategory": "Container Runtime Anomaly - High Risk IP",
                    "sccStatus": "ACTIVE",
                    "msg": "Connection to high risk IP 54.88.32.27:80, which is explicitly blocked in the runtime rule",
                    "sccStat": "info​",
                    "container": "/nifty_poincare",
                    "url": "http://35.197.45.209:8081/#!/login",
                    "scc_status": "ACTIVE",
                    "scc_source_category_id": "CONTAINER_RUNTIME_ANOMALY-HIGH_RISK_IP",
                    "sccSeverity": "high",
                    "image": "alpine:3.7",
                    "rule": "Default - alert on suspicious runtime behavior"
                },
                "securityMarks": {
                    "name": "organizations/688851828130/sources/10525437515560121179/findings/ac785971e7024c609d91f47211519d3e/securityMarks"
                },
                "eventTime": "2018-07-20T18:31:29Z",
                "createTime": "2018-07-20T18:31:29Z"
            }
        ]


def mock_finding_sources():
    return [{
        "name": "organizations/688851828130/sources/250821172470083347/findings/e0d6193111244e3289aa9abe2dd4308e",
        "parent": "organizations/688851828130/sources/250821172470083347",
        "resourceName": "//cloudresourcemanager.googleapis.com/projects/520732501711",
        "state": "ACTIVE",
        "category": "Sensitive IAM updates",
        "externalUri": "https://app-demo.redlock.io/alerts?filters#alert.status=open&timeType=absolute&startTime=1520956413304&endTime=1520957313552&alertRule.name=RedLock-CSCC-Integration&cloud.account=RedLock-Google-CSCC-DoNotDelete&alert.id=P-51307",
        "sourceProperties": {
            "resourceConfig": "{\"severity\":\"\\\"NOTICE\\\"\",\"logName\":\"cloudaudit.googleapis.com%2Factivity\",\"payload\":{\"requestMetadata\":{\"callerSuppliedUserAgent\":\"google-cloud-sdk x_Tw5K8nnjoRAqULM9PFAC2b gcloud/192.0.0 command/gcloud.iam.service-accounts.keys.create invocation-id/ec2e60a4a68e4be0be95f3cf5a0bf086 environment/None environment-version/None interactive/True from-script/True python/2.7.12 (Linux 4.13.0-36-generic),gzip(gfe)\",\"callerIp\":\"177.185.2.139\"},\"request\":{\"@type\":\"type.googleapis.com/google.iam.admin.v1.CreateServiceAccountKeyRequest\",\"private_key_type\":2,\"name\":\"projects/-/serviceAccounts/creator@connector-project-redlock.iam.gserviceaccount.com\"},\"authorizationInfo\":[{\"resource\":\"projects/-/serviceAccounts/103761591776958066191\",\"permission\":\"iam.serviceAccountKeys.create\",\"granted\":true}],\"authenticationInfo\":{\"principalEmail\":\"manasses@gcp-sec-demo-org-rl.joonix.net\"},\"response\":{\"valid_after_time\":{\"seconds\":1520956880},\"@type\":\"type.googleapis.com/google.iam.admin.v1.ServiceAccountKey\",\"private_key_type\":2,\"name\":\"projects/connector-project-redlock/serviceAccounts/creator@connector-project-redlock.iam.gserviceaccount.com/keys/caeabf66adaf225c9b09dd5efd6a1aa46a6217ed\",\"valid_before_time\":{\"seconds\":1836316880},\"key_algorithm\":2},\"methodName\":\"google.iam.admin.v1.CreateServiceAccountKey\",\"resourceName\":\"projects/-/serviceAccounts/103761591776958066191\",\"serviceName\":\"iam.googleapis.com\",\"status\":{}},\"resource\":\"{\\\"type\\\":\\\"service_account\\\",\\\"labels\\\":{\\\"email_id\\\":\\\"creator@connector-project-redlock.iam.gserviceaccount.com\\\",\\\"unique_id\\\":\\\"103761591776958066191\\\",\\\"project_id\\\":\\\"connector-project-redlock\\\"}}\",\"operation\":\"null\",\"labels\":\"{}\",\"insertId\":\"c7r2tcc4wo\",\"timestamp\":1520956879967}",
            "cloudType": "Google Cloud Platform",
            "accountName": "RedLock-Google-CSCC-DoNotDelete",
            "severity": "medium",
            "alertRemediationCli": "BLANK",
            "policyDescription": "Detects sensitive IAM updates such as addition, and deletion of Service Account Key, IAM policies etc. Changing these configurations in the cloud environment may leave the cloud in a vulnerable state and it is important that security teams have visibility into and get alerted when these operations are performed.",
            "scc_status": "ACTIVE",
            "riskRating": "N/A",
            "accountID": "connector-project-redlock",
            "resourceRegionId": "global",
            "policyRecommendation": "1. Log in to the Console and make sure that the user indeed had the permissions to make the changes to the configuration that was reported.\n\t     2. Make sure that the configuration changes do not put the cloud resources in a vulnerable state.\n\t     3. If the user was not authorized to perform the reported changes, make sure that the IAM permissions (Console > IAM & Admin > IAM) are correctly set.",
            "resourceType": "Audit Event",
            "resourceRegion": "global",
            "alertTs": "1520957313045",
            "url": "https://app-demo.redlock.io/alerts?filters#alert.status=open&timeType=absolute&startTime=1520956413304&endTime=1520957313552&alertRule.name=RedLock-CSCC-Integration&cloud.account=RedLock-Google-CSCC-DoNotDelete&alert.id=P-51307",
            "alertAttribution": "BLANK",
            "policyLabels": "[\"GCP\"]",
            "scc_source_category_id": "Sensitive IAM updates"
        },
        "securityMarks": {
            "name": "organizations/688851828130/sources/250821172470083347/findings/e0d6193111244e3289aa9abe2dd4308e/securityMarks"
        },
        "eventTime": "2018-03-13T16:08:33.045Z",
        "createTime": "2018-03-13T16:08:33.045Z"
    },
    {
        "name": "organizations/688851828130/sources/250821172470083347/findings/e62c34ec008e462b9904d05552e3b5a6",
        "parent": "organizations/688851828130/sources/250821172470083347",
        "resourceName": "//cloudresourcemanager.googleapis.com/projects/520732501711",
        "state": "ACTIVE",
        "category": "Primitive IAM roles should not be used - CSCC",
        "externalUri": "https://app-demo.redlock.io/alerts?filters#alert.status=open&timeType=absolute&startTime=1521000467246&endTime=1521005927269&alertRule.name=RedLock-CSCC-Integration&cloud.account=RedLock-Google-CSCC-DoNotDelete&alert.id=P-51320",
        "sourceProperties": {
            "resourceConfig": "{\"role\":\"roles/viewer\",\"members\":[\"serviceAccount:readlock-readonly-integration@connector-project-redlock.iam.gserviceaccount.com\"]}",
            "cloudType": "Google Cloud Platform",
            "accountName": "RedLock-Google-CSCC-DoNotDelete",
            "severity": "medium",
            "alertRemediationCli": "BLANK",
            "policyDescription": "Primitive roles are Roles that existed prior to Cloud IAM. Primitive roles are built-in and provide a broader access to resources making them prone to attacks and privilege escalation. Predefined roles provide more granular controls than primitive roles and therefore Predefined roles should be used.",
            "scc_status": "ACTIVE",
            "riskRating": "C",
            "accountID": "connector-project-redlock",
            "resourceRegionId": "global",
            "policyRecommendation": "Review the projects / resources that have Primitive roles assigned to them and replace them with equivalent Predefined roles.",
            "resourceType": "IAM Policy",
            "resourceRegion": "global",
            "alertTs": "1521005926847",
            "url": "https://app-demo.redlock.io/alerts?filters#alert.status=open&timeType=absolute&startTime=1521000467246&endTime=1521005927269&alertRule.name=RedLock-CSCC-Integration&cloud.account=RedLock-Google-CSCC-DoNotDelete&alert.id=P-51320",
            "alertAttribution": "BLANK",
            "policyLabels": "[\"GCP\",\"CSCC\"]",
            "scc_source_category_id": "Primitive IAM roles should not be used - CSCC"
        },
        "securityMarks": {
            "name": "organizations/688851828130/sources/250821172470083347/findings/e62c34ec008e462b9904d05552e3b5a6/securityMarks"
        },
        "eventTime": "2018-03-14T05:38:46.847Z",
        "createTime": "2018-03-14T05:38:46.847Z"
    },
    {
        "name": "organizations/688851828130/sources/9300364871731100004/findings/022c268b387649bb8cf15d9a2f4f3d3f",
        "parent": "organizations/688851828130/sources/9300364871731100004",
        "resourceName": "//cloudresourcemanager.googleapis.com/projects/760319584329",
        "state": "ACTIVE",
        "category": "VM Instance with service 'Hadoop Name Node' (TCP:9000) is exposed to a wide network scope",
        "externalUri": "https://secure.dome9.com/v2/compliance-engine/result/150621",
        "sourceProperties": {
            "remediation": "Configure your database to only allow access from internal networks and limited access scope.\rIf public interface exists, remove it and limit the access scope within the network only to applications or instances that requires access.\rSee https://cloud.google.com/compute/docs/networking for further reading about GCP networking and Firewall rules.",
            "bundleDescription": "Dome9 Network Alerts for Google Cloud Platform",
            "severity": "Medium",
            "findingSourceId": "DOME9",
            "name": "VM Instance with service 'Hadoop Name Node' (TCP:9000) is exposed to a wide network scope",
            "complianceTag": "Dome9 NetSec",
            "scc_status": "ACTIVE",
            "dome9Id": "8|8fa07261-9340-489c-b420-991d880e48d6|Region|us-east1|Zone|us-east1-b|Instance|bastion",
            "project": "https://www.googleapis.com/compute/beta/projects/sound-decoder-195010",
            "callbackURL": "https://secure.dome9.com/v2/compliance-engine/result/150621",
            "entityType": "vmInstance",
            "assessmentId": "150621",
            "logic": "VMInstance where nics contain-any [inboundRules contain [ destinationPort<=9000 and destinationPortTo >=9000 and protocol in ('TCP','ALL')]] should not have nics contain-any [inboundRules contain [ destinationPort<=9000 and destinationPortTo >=9000 and protocol in ('TCP','ALL')] and inboundRules allowedHostsForPort(9000) > 256 ]",
            "url": "https://secure.dome9.com/v2/compliance-engine/result/150621",
            "description": "Dome9 Network Alerts for Google Cloud Platform",
            "bundleName": "Dome9 Network Alerts for GCP",
            "scc_source_category_id": "VM Instance with service 'Hadoop Name Node' (TCP:9000) is exposed to a wide network scope",
            "triggeredBy": "ContinuousCompliancePolicy"
        },
        "securityMarks": {
            "name": "organizations/688851828130/sources/9300364871731100004/findings/022c268b387649bb8cf15d9a2f4f3d3f/securityMarks"
        },
        "eventTime": "2018-03-19T20:54:55Z",
        "createTime": "2018-03-19T20:54:55Z"
    },
    {
        "name": "organizations/688851828130/sources/9300364871731100004/findings/030daf93f89a445db0e7a0d521fadf46",
        "parent": "organizations/688851828130/sources/9300364871731100004",
        "resourceName": "//cloudresourcemanager.googleapis.com/projects/760319584329",
        "state": "ACTIVE",
        "category": "VM Instance with service 'MSSQL Debugger' (TCP:135) is exposed to a wide network scope",
        "externalUri": "https://secure.dome9.com/v2/compliance-engine/result/150621",
        "sourceProperties": {
            "remediation": "Configure your database to only allow access from internal networks and limited access scope.\rIf public interface exists, remove it and limit the access scope within the network only to applications or instances that requires access.\rSee https://cloud.google.com/compute/docs/networking for further reading about GCP networking and Firewall rules.",
            "bundleDescription": "Dome9 Network Alerts for Google Cloud Platform",
            "severity": "Medium",
            "findingSourceId": "DOME9",
            "name": "VM Instance with service 'MSSQL Debugger' (TCP:135) is exposed to a wide network scope",
            "complianceTag": "Dome9 NetSec",
            "scc_status": "ACTIVE",
            "dome9Id": "8|8fa07261-9340-489c-b420-991d880e48d6|Region|us-east1|Zone|us-east1-b|Instance|bastion",
            "project": "https://www.googleapis.com/compute/beta/projects/sound-decoder-195010",
            "callbackURL": "https://secure.dome9.com/v2/compliance-engine/result/150621",
            "entityType": "vmInstance",
            "assessmentId": "150621",
            "logic": "VMInstance where nics contain-any [inboundRules contain [ destinationPort<=135 and destinationPortTo >=135 and protocol in ('TCP','ALL')]] should not have nics contain-any [inboundRules contain [ destinationPort<=135 and destinationPortTo >=135 and protocol in ('TCP','ALL')] and inboundRules allowedHostsForPort(135) > 256 ]",
            "url": "https://secure.dome9.com/v2/compliance-engine/result/150621",
            "description": "Dome9 Network Alerts for Google Cloud Platform",
            "bundleName": "Dome9 Network Alerts for GCP",
            "scc_source_category_id": "VM Instance with service 'MSSQL Debugger' (TCP:135) is exposed to a wide network scope",
            "triggeredBy": "ContinuousCompliancePolicy"
        },
        "securityMarks": {
            "name": "organizations/688851828130/sources/9300364871731100004/findings/030daf93f89a445db0e7a0d521fadf46/securityMarks"
        },
        "eventTime": "2018-03-19T20:54:55Z",
        "createTime": "2018-03-19T20:54:55Z"
    }]


def mock_asset_network_state_active_and_added():
    return [
        {
            "asset": {
                "name": "organizations/688851828130/assets/3995505764686144800",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/asset-dev-project/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/138150943629",
                    "resourceOwners": [
                        "user:dandrade@gcp-sec-demo-org.joonix.net",
                        "user:lucasbr@gcp-sec-demo-org.joonix.net",
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-02-22T05:51:04.672-08:00",
                    "kind": "compute#network",
                    "name": "default",
                    "subnetworks": "[https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-south1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/asia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/australia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west2/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west3/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/europe-west4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/northamerica-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/southamerica-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-central1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-east4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/asset-dev-project/regions/us-west1/subnetworks/default]",
                    "autoCreateSubnetworks": "true",
                    "description": "Default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/asset-dev-project/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": 2032409055311655900
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/3995505764686144800/securityMarks"
                },
                "createTime": "2018-04-20T17:34:14.579Z",
                "updateTime": "1970-01-01T00:00:00Z"
            },
            "state": "ACTIVE"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/5059612515522354630",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/connector-project/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/520732501711",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/520732501711",
                    "resourceOwners": [
                        "user:andychang@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-03-16T19:13:01.367-07:00",
                    "kind": "compute#network",
                    "name": "default",
                    "subnetworks": "[https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-south1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/asia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/australia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west2/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west3/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/europe-west4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/northamerica-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/southamerica-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-central1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-east4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/connector-project/regions/us-west1/subnetworks/default]",
                    "autoCreateSubnetworks": "true",
                    "description": "Default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/connector-project/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": 1071120697868273500
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/5059612515522354630/securityMarks"
                },
                "createTime": "2018-04-20T17:34:19.079Z",
                "updateTime": "1970-01-01T00:00:00Z"
            },
            "state": "ADDED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/17786314765363260009",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/marine-physics-196005/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/1000586090784",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/1000586090784",
                    "resourceOwners": [
                        "serviceAccount:catman-demo-controller@marine-physics-196005.iam.gserviceaccount.com",
                        "user:iben@google.com"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-03-16T06:13:11.665-07:00",
                    "kind": "compute#network",
                    "name": "default",
                    "subnetworks": "[https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/asia-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/asia-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/asia-south1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/asia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/australia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/europe-west1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/europe-west2/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/europe-west3/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/europe-west4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/northamerica-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/southamerica-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/us-central1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/us-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/us-east4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/marine-physics-196005/regions/us-west1/subnetworks/default]",
                    "autoCreateSubnetworks": "true",
                    "description": "Default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/marine-physics-196005/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": 5656321160515058700
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/17786314765363260009/securityMarks"
                },
                "createTime": "2018-04-20T17:34:21.078Z",
                "updateTime": "1970-01-01T00:00:00Z"
            },
            "state": "ADDED"
        },
        {
            "asset": {
                "name": "organizations/688851828130/assets/3799708671966037529",
                "securityCenterProperties": {
                    "resourceName": "//compute.googleapis.com/projects/processor-project/global/networks/default",
                    "resourceType": "google.compute.Network",
                    "resourceParent": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceProject": "//cloudresourcemanager.googleapis.com/projects/1091116670070",
                    "resourceOwners": [
                        "user:walves@gcp-sec-demo-org.joonix.net"
                    ]
                },
                "resourceProperties": {
                    "creationTimestamp": "2018-02-27T09:37:01.267-08:00",
                    "kind": "compute#network",
                    "name": "default",
                    "subnetworks": "[https://www.googleapis.com/compute/v1/projects/processor-project/regions/asia-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/asia-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/asia-south1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/asia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/australia-southeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/europe-west1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/europe-west2/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/europe-west3/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/europe-west4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/northamerica-northeast1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/southamerica-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/us-central1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/us-east1/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/us-east4/subnetworks/default, https://www.googleapis.com/compute/v1/projects/processor-project/regions/us-west1/subnetworks/default]",
                    "autoCreateSubnetworks": "true",
                    "description": "Default network for the project",
                    "selfLink": "https://www.googleapis.com/compute/v1/projects/processor-project/global/networks/default",
                    "routingConfig": "{\"routingMode\":\"REGIONAL\"}",
                    "id": 1057398560828959200
                },
                "securityMarks": {
                    "name": "organizations/688851828130/assets/3799708671966037529/securityMarks"
                },
                "createTime": "2018-04-20T17:34:23.576Z",
                "updateTime": "1970-01-01T00:00:00Z"
            },
            "state": "ACTIVE"
        }
    ]