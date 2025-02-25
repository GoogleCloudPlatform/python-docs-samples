# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
from typing import Generator, Tuple
import uuid

from google.api_core import retry
from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import dlp, modelarmor_v1
import pytest

from create_template import create_model_armor_template
from create_template_with_advanced_sdp import (
    create_model_armor_template_with_advanced_sdp,
)
from create_template_with_basic_sdp import create_model_armor_template_with_basic_sdp
from create_template_with_labels import create_model_armor_template_with_labels
from create_template_with_metadata import create_model_armor_template_with_metadata
from delete_template import delete_model_armor_template
from get_folder_floor_settings import get_folder_floor_settings
from get_organization_floor_settings import get_organization_floor_settings
from get_project_floor_settings import get_project_floor_settings
from get_template import get_model_armor_template
from list_templates import list_model_armor_templates
from list_templates_with_filter import list_model_armor_templates_with_filter
from quickstart import quickstart
from sanitize_model_response import sanitize_model_response
from sanitize_model_response_with_user_prompt import (
    sanitize_model_response_with_user_prompt,
)
from sanitize_user_prompt import sanitize_user_prompt
from screen_pdf_file import screen_pdf_file
from update_folder_floor_settings import update_folder_floor_settings
from update_organizations_floor_settings import update_organization_floor_settings
from update_project_floor_settings import update_project_floor_settings
from update_template import update_model_armor_template
from update_template_lables import update_model_armor_template_labels
from update_template_metadata import update_model_armor_template_metadata
from update_template_with_mask_configuration import (
    update_model_armor_template_with_mask_configuration,
)

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
TEMPLATE_ID = f"test-model-armor-{uuid.uuid4()}"


@pytest.fixture()
def project_id() -> str:
    return os.environ["GOOGLE_CLOUD_PROJECT"]


@pytest.fixture()
def location_id() -> str:
    return "us-central1"


@pytest.fixture()
def client(location_id: str) -> modelarmor_v1.ModelArmorClient:
    """Provides a ModelArmorClient instance."""
    return modelarmor_v1.ModelArmorClient(
        client_options=ClientOptions(
            api_endpoint=f"modelarmor.{location_id}.rep.googleapis.com"
        )
    )


@retry.Retry()
def retry_ma_delete_template(
    client: modelarmor_v1.ModelArmorClient,
    name: str,
) -> None:
    print(f"Deleting template {name}")
    return client.delete_template(name=name)


@retry.Retry()
def retry_ma_create_template(
    client: modelarmor_v1.ModelArmorClient,
    parent: str,
    template_id: str,
    filter_config_data: modelarmor_v1.FilterConfig,
) -> modelarmor_v1.Template:
    print(f"Creating template {template_id}")

    template = modelarmor_v1.Template(filter_config=filter_config_data)

    create_request = modelarmor_v1.CreateTemplateRequest(
        parent=parent, template_id=template_id, template=template
    )
    return client.create_template(request=create_request)


@pytest.fixture()
def template_id(
    project_id: str, location_id: str, client: modelarmor_v1.ModelArmorClient
) -> Generator[str, None, None]:
    template_id = f"modelarmor-template-{uuid.uuid4()}"

    yield template_id

    try:
        time.sleep(5)
        retry_ma_delete_template(
            client,
            name=f"projects/{project_id}/locations/{location_id}/templates/{template_id}",
        )
    except NotFound:
        # Template was already deleted, probably in the test
        print(f"Template {template_id} was not found.")


@pytest.fixture()
def sdp_templates(
    project_id: str, location_id: str
) -> Generator[Tuple[str, str], None, None]:
    inspect_template_id = f"model-armour-inspect-template-{uuid.uuid4()}"
    deidentify_template_id = f"model-armour-deidentify-template-{uuid.uuid4()}"
    api_endpoint = f"dlp.{location_id}.rep.googleapis.com"
    parent = f"projects/{project_id}/locations/{location_id}"
    info_types = [
        {"name": "EMAIL_ADDRESS"},
        {"name": "PHONE_NUMBER"},
        {"name": "US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER"},
    ]

    inspect_response = dlp.DlpServiceClient(
        client_options=ClientOptions(api_endpoint=api_endpoint)
    ).create_inspect_template(
        request={
            "parent": parent,
            "location_id": location_id,
            "inspect_template": {
                "inspect_config": {"info_types": info_types},
            },
            "template_id": inspect_template_id,
        }
    )

    deidentify_response = dlp.DlpServiceClient(
        client_options=ClientOptions(api_endpoint=api_endpoint)
    ).create_deidentify_template(
        request={
            "parent": parent,
            "location_id": location_id,
            "template_id": deidentify_template_id,
            "deidentify_template": {
                "deidentify_config": {
                    "info_type_transformations": {
                        "transformations": [
                            {
                                "info_types": [],
                                "primitive_transformation": {
                                    "replace_config": {
                                        "new_value": {"string_value": "[REDACTED]"}
                                    }
                                },
                            }
                        ]
                    }
                }
            },
        }
    )

    yield inspect_response.name, deidentify_response.name
    try:
        time.sleep(5)
        dlp.DlpServiceClient(
            client_options=ClientOptions(api_endpoint=api_endpoint)
        ).delete_inspect_template(name=inspect_response.name)
        dlp.DlpServiceClient(
            client_options=ClientOptions(api_endpoint=api_endpoint)
        ).delete_deidentify_template(name=deidentify_response.name)
    except NotFound:
        # Template was already deleted, probably in the test
        print("SDP Templates were not found.")


@pytest.fixture()
def simple_template(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str,
    template_id: str,
) -> Generator[Tuple[str, modelarmor_v1.FilterConfig], None, None]:
    filter_config_data = modelarmor_v1.FilterConfig(
        pi_and_jailbreak_filter_settings=modelarmor_v1.PiAndJailbreakFilterSettings(
            filter_enforcement=modelarmor_v1.PiAndJailbreakFilterSettings.PiAndJailbreakFilterEnforcement.ENABLED,
            confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
        ),
        malicious_uri_filter_settings=modelarmor_v1.MaliciousUriFilterSettings(
            filter_enforcement=modelarmor_v1.MaliciousUriFilterSettings.MaliciousUriFilterEnforcement.ENABLED,
        ),
    )
    retry_ma_create_template(
        client,
        parent=f"projects/{project_id}/locations/{location_id}",
        template_id=template_id,
        filter_config_data=filter_config_data,
    )

    yield template_id, filter_config_data


@pytest.fixture()
def basic_sdp_template(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str,
    template_id: str,
) -> Generator[Tuple[str, modelarmor_v1.FilterConfig], None, None]:
    filter_config_data = modelarmor_v1.FilterConfig(
        rai_settings=modelarmor_v1.RaiFilterSettings(
            rai_filters=[
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.DANGEROUS,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.HARASSMENT,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.HATE_SPEECH,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.SEXUALLY_EXPLICIT,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
            ]
        ),
        sdp_settings=modelarmor_v1.SdpFilterSettings(
            basic_config=modelarmor_v1.SdpBasicConfig(
                filter_enforcement=modelarmor_v1.SdpBasicConfig.SdpBasicConfigEnforcement.ENABLED
            )
        ),
    )

    retry_ma_create_template(
        client,
        parent=f"projects/{project_id}/locations/{location_id}",
        template_id=template_id,
        filter_config_data=filter_config_data,
    )

    yield template_id, filter_config_data


@pytest.fixture()
def advance_sdp_template(
    client: modelarmor_v1.ModelArmorClient,
    project_id: str,
    location_id: str,
    template_id: str,
    sdp_templates: Tuple,
) -> Generator[Tuple[str, modelarmor_v1.FilterConfig], None, None]:
    inspect_id, deidentify_id = sdp_templates
    advance_sdp_filter_config_data = modelarmor_v1.FilterConfig(
        rai_settings=modelarmor_v1.RaiFilterSettings(
            rai_filters=[
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.DANGEROUS,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.HARASSMENT,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.MEDIUM_AND_ABOVE,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.HATE_SPEECH,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
                modelarmor_v1.RaiFilterSettings.RaiFilter(
                    filter_type=modelarmor_v1.RaiFilterType.SEXUALLY_EXPLICIT,
                    confidence_level=modelarmor_v1.DetectionConfidenceLevel.HIGH,
                ),
            ]
        ),
        sdp_settings=modelarmor_v1.SdpFilterSettings(
            advanced_config=modelarmor_v1.SdpAdvancedConfig(
                inspect_template=inspect_id,
                deidentify_template=deidentify_id,
            )
        ),
    )
    retry_ma_create_template(
        client,
        parent=f"projects/{project_id}/locations/{location_id}",
        template_id=template_id,
        filter_config_data=advance_sdp_filter_config_data,
    )

    yield template_id, advance_sdp_filter_config_data


@pytest.fixture()
def floor_settings_project_id(project_id: str) -> Generator[str, None, None]:
    client = modelarmor_v1.ModelArmorClient(transport="rest")

    yield project_id
    try:
        time.sleep(5)
        client.update_floor_setting(
            request=modelarmor_v1.UpdateFloorSettingRequest(
                floor_setting=modelarmor_v1.FloorSetting(
                    name=f"projects/{project_id}/locations/global/floorSetting",
                    filter_config=modelarmor_v1.FilterConfig(
                        rai_settings=modelarmor_v1.RaiFilterSettings(rai_filters=[])
                    ),
                    enable_floor_setting_enforcement=False,
                )
            )
        )
    except GoogleAPIError:
        print("Floor settings not set or not authorized to set floor settings")

@pytest.fixture()
def pdf_content_base64() -> str:
   return ("JVBERi0xLjQKJdPr6eEKMSAwIG9iago8PC9UaXRsZSAoVW50aXRsZWQgZG9jdW1lbnQpCi9Qcm9kdWNlciAoU2tp"
        "YS9QREYgbTEzNSBHb29nbGUgRG9jcyBSZW5kZXJlcik+PgplbmRvYmoKMyAwIG9iago8PC9jYSAxCi9CTSAvTm9y"
        "bWFsPj4KZW5kb2JqCjUgMCBvYmoKPDwvRmlsdGVyIC9GbGF0ZURlY29kZQovTGVuZ3RoIDExMzA+PiBzdHJlYW0K"
        "eJytWdtuG0cMfd+v2B/IeHgbzgCGAUuJgz4EaAv9QdsEKNCHJP8PlCO52d2Io2rHYxmytOOleDkkDymYoz3egT1p"
        "wfmPf6avU1A5X/3vr12EuT5+/zhfXnz7Mj18pPnL96meZ0gzREnzt7+mz9NvP0lQrL8mI54vmYzLi0XGw6/z4+PD"
        "p+Mv7+3y09Ph/XE6nKaHF56BQ6o/Op8+T7CoGlhLBqUyn6rcd0ABVYkpz6c/58cY8fA0n/6eIAbJjMpkN11O+Hg+"
        "sRskAZflQPR8wCEqFBVd7nhp3MH5fJADCEDUvIiS88GH0y47iAPGSBEdeyJ1ScwmBtE0czx0bJgrqeejuISkSFqG"
        "KS8UlJmEPeUvDi5BVVJk/KE8cutAe3TIFLK9Jb1plYP4nIJwwiQ3gf/h03ENfhgE/puaQYQQCwqWParhqLw8doHr"
        "B0hHgctylqkIeOASaKR1M9/bB12o42jIz5RpmLnMIWMk8QpBs+4JdqWthsjEPK6KJQgAwuBFX55bdf61BpvhOSaW"
        "VUz2N4Dco3bBEKUMxGxJAcgckfYEkQ8taDbd0FX/AXIolEv0MqrPXkAKEWL2QMt8u/Veh73toZYj+OIIDYQZUO7m"
        "A3vNTBggJrcUdTouGVI0A7hIaVnVAsprGXAOmrnXxlaztD73GIpQghVxGOY5RMMHUvSStttBe3WQGEos4gWv0yrh"
        "YO9cJiXxEkQ07plV40r7dVPDO9Li0KVbibU1GVEaZm2x5C+YXN7YRT+wWG1Lbt3t5OXRKhslN8QbmK3dvqp4lb/5"
        "ha3AG6sREQRL2jyOxxNJSETZi/B2TMsl+SWE+P+tffH/f03Ntm6TRRADLJIAuqxUC2lJeSBIVAOkfIffpLw16EWs"
        "5DCOa0FUrDJr8kjgtm1sYt6EeN9IismyrOhAGk3RqCgkLzk2wLTR02+s+Fa2wNYdOMu49GRrDiLqArcdqnXP89Pq"
        "in812ob0jUi5BLHX49i10ZRgCrsShRrWcqNHbryg6YpcX3th7c+0rC2kqxgJ5WCmuBNT5zKGMQgBeLm0KdW1Tb5R"
        "eaE6SQwcIEVyHSTIHSQa2dliP1u+xHEJ1WYkwSvOu3fojWi8iNI4bmvXCM9LOsPjG4fDVhY3lwh7BrXLZ6eA1pY0"
        "Lw7ua8xss5DEVAnmz+Z3oikGRKOXcC2wj15aATbOmmq2DtIwBzKDC+6IeDtO1MJI31bEhhuFWKnGGGONuhhzKaXs"
        "gXffoA4QiAVhGJQAJDBYxjhYurHZaoaquYZsbiy6mi/U1bw1wlpQBzlCNFiql9pf7o9icwdUGhNqX9gr1UhMaZix"
        "lWmYECcFXuOxoyAPXj0jnjGeHUD2blTOEFcvPblLIJGFI2dHYKeGpEb8rJk7OdhejtzFf9fMrw98qGAzDA6rOKgS"
        "wDzvheP5Di4LsuKmrQVRizrdw303vmy6v3PM5ViZlAzLZGK2bCnihGeTyQ3nbEeJ3fudQ+OGzgVGtkZavDxdf51Y"
        "vxb8FzWXmOYKZW5kc3RyZWFtCmVuZG9iagoyIDAgb2JqCjw8L1R5cGUgL1BhZ2UKL1Jlc291cmNlcyA8PC9Qcm9j"
        "U2V0IFsvUERGIC9UZXh0IC9JbWFnZUIgL0ltYWdlQyAvSW1hZ2VJXQovRXh0R1N0YXRlIDw8L0czIDMgMCBSPj4K"
        "L0ZvbnQgPDwvRjQgNCAwIFI+Pj4+Ci9NZWRpYUJveCBbMCAwIDYxMiA3OTJdCi9Db250ZW50cyA1IDAgUgovU3Ry"
        "dWN0UGFyZW50cyAwCi9UYWJzIC9TCi9QYXJlbnQgNiAwIFI+PgplbmRvYmoKNiAwIG9iago8PC9UeXBlIC9QYWdl"
        "cwovQ291bnQgMQovS2lkcyBbMiAwIFJdPj4KZW5kb2JqCjkgMCBvYmoKPDwvVHlwZSAvU3RydWN0RWxlbQovUyAv"
        "UAovUCA4IDAgUgovUGcgMiAwIFIKL0sgMD4+CmVuZG9iagoxMCAwIG9iago8PC9UeXBlIC9TdHJ1Y3RFbGVtCi9T"
        "IC9QCi9QIDggMCBSCi9QZyAyIDAgUgovSyAxPj4KZW5kb2JqCjExIDAgb2JqCjw8L1R5cGUgL1N0cnVjdEVsZW0K"
        "L1MgL1AKL1AgOCAwIFIKL1BnIDIgMCBSCi9LIDI+PgplbmRvYmoKOCAwIG9iago8PC9UeXBlIC9TdHJ1Y3RFbGVt"
        "Ci9TIC9Eb2N1bWVudAovUCA3IDAgUgovSyBbOSAwIFIgMTAgMCBSIDExIDAgUl0+PgplbmRvYmoKMTIgMCBvYmoK"
        "WzkgMCBSIDEwIDAgUiAxMSAwIFJdCmVuZG9iagoxMyAwIG9iago8PC9UeXBlIC9QYXJlbnRUcmVlCi9OdW1zIFsw"
        "IDEyIDAgUl0+PgplbmRvYmoKNyAwIG9iago8PC9UeXBlIC9TdHJ1Y3RUcmVlUm9vdAovSyA4IDAgUgovUGFyZW50"
        "VHJlZU5leHRLZXkgMQovUGFyZW50VHJlZSAxMyAwIFI+PgplbmRvYmoKMTQgMCBvYmoKPDwvVHlwZSAvQ2F0YWxv"
        "ZwovUGFnZXMgNiAwIFIKL01hcmtJbmZvIDw8L1R5cGUgL01hcmtJbmZvCi9NYXJrZWQgdHJ1ZT4+Ci9TdHJ1Y3RU"
        "cmVlUm9vdCA3IDAgUgovVmlld2VyUHJlZmVyZW5jZXMgPDwvVHlwZSAvVmlld2VyUHJlZmVyZW5jZXMKL0Rpc3Bs"
        "YXlEb2NUaXRsZSB0cnVlPj4KL0xhbmcgKGVuKT4+CmVuZG9iagoxNSAwIG9iago8PC9MZW5ndGgxIDI4OTk2Ci9G"
        "aWx0ZXIgL0ZsYXRlRGVjb2RlCi9MZW5ndGggMTYzMDg+PiBzdHJlYW0KeJztfAl8FEUW96vqnu6ZnqvnyNzJTDKZ"
        "ScgEAjkIgUgGSACN3IcJJhKOyC2nCIoSVhFEVFbXe1fwWM91GULEgO6SVXTXg4X1XHURVFR0F2VdREWT+V5Vz4Qg"
        "sJ/f9/u+3/fb77c91L9eV1VXV9d79eq91x2AAIADQYS+I6prhtOr6BUA1IOldSPGjpmwRtg8AUBowPPWERMmDVV+"
        "L28EIAk87ztmQlHxCtfTXmy/CM+bJlePqht769yvAXqpALZfzFgwbZHoF67G+v1Yv3HG8mWh+wNv/x1Avg5Amnjp"
        "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"
        "7U7dnXdf5+bX2ZKHtishMQSsAnUr4f/niiX5xg57BRRiwgW+zVGBT1SfDl7EtP9TZXFjOhjVvRTPdTCVzDWyw83U"
        "cljIE0ht1zO7HqsSSx7bubnsvB1bu9qeeazX26ii7z1se5le1nnXK3vppd+/S1c99cM+1NXZXeOEL1BX++g89II8"
        "2stj7WszbsVxtIqpFyvH40VaQI+/VuFo0lpoIT6OZs3MMqVf2MT5WzvNBEuZDZmK0yoYhYDXapeMkiNut4aMcVPI"
        "yn1Hq7co5jvg8+z1eVWW8SgEV07+7dYA+/ju/fiCQEW+c7J1qyLEzXErtYby+5aqDGSTwe4ye+x5xjxTnrm/qb+5"
        "zHK3zZhvz3eMdNXb6x31GXPscxxzMlZKy80rbVc6r8xYa95g22jf6LjBeZfyqPFZ9RnbLufnyqfOr82d6nfOZCAr"
        "rRRcDmPAL1qrrddZBau3e/halMSeWtG4j1utJhVXJG7iXqfDEbErTjyxmnDJRYwKOuGKg30ebJRYBxBQA7QosDtA"
        "A+206ikrzkXc2U4nxo1V9ridTrXvtlN7Oxm6w0pyoMavsCo+W/GQqa9pjEkYa0qaqAlbbC9iHybSqjZ/aBUuP5y8"
        "TvYXOrj3sz/Q8ajHD3vVw42Lj/o86lFOgYe5D2wNMkNAz/5cR4fLzIIE4JPgwqqs1OPasqBMe1Cmn0GP6wgYk0dI"
        "T4l2Jt/fUV6h5JRX4BZ65KmMCltOBpPqWD0zgAHNCZTm06UWYo487ZsP/J0yKlBBopW72jmosHKk2xbVGbsWPHcg"
        "lhOMfdTWNX9Ibt9Vk0u7Zj2m5uf651kzxfzOuy9fs2o5nff9n7YOrZ8A/wN/P7tSCmVuZHN0cmVhbQplbmRvYmoK"
        "MTYgMCBvYmoKPDwvVHlwZSAvRm9udERlc2NyaXB0b3IKL0ZvbnROYW1lIC9BQUFBQUErQXJpYWxNVAovRmxhZ3Mg"
        "NAovQXNjZW50IDkwNS4yNzM0NAovRGVzY2VudCAtMjExLjkxNDA2Ci9TdGVtViA0NS44OTg0MzgKL0NhcEhlaWdo"
        "dCA3MTUuODIwMzEKL0l0YWxpY0FuZ2xlIDAKL0ZvbnRCQm94IFstNjY0LjU1MDc4IC0zMjQuNzA3MDMgMjAwMCAx"
        "MDA1Ljg1OTM4XQovRm9udEZpbGUyIDE1IDAgUj4+CmVuZG9iagoxNyAwIG9iago8PC9UeXBlIC9Gb250Ci9Gb250"
        "RGVzY3JpcHRvciAxNiAwIFIKL0Jhc2VGb250IC9BQUFBQUErQXJpYWxNVAovU3VidHlwZSAvQ0lERm9udFR5cGUy"
        "Ci9DSURUb0dJRE1hcCAvSWRlbnRpdHkKL0NJRFN5c3RlbUluZm8gPDwvUmVnaXN0cnkgKEFkb2JlKQovT3JkZXJp"
        "bmcgKElkZW50aXR5KQovU3VwcGxlbWVudCAwPj4KL1cgWzAgWzc1MF0gMyAxNyAyNzcuODMyMDMgMzYgMzcgNjY2"
        "Ljk5MjE5IDM5IDQzIDcyMi4xNjc5NyA0NCBbMjc3LjgzMjAzXSA2OCBbNTU2LjE1MjM0XSA3MSA3NSA1NTYuMTUy"
        "MzQgNzYgNzkgMjIyLjE2Nzk3IDgwIFs4MzMuMDA3ODFdIDgxIDgzIDU1Ni4xNTIzNCA4NSBbMzMzLjAwNzgxXSA4"
        "NyBbMjc3LjgzMjAzIDU1Ni4xNTIzNF0gOTAgWzcyMi4xNjc5N11dCi9EVyA1MDA+PgplbmRvYmoKMTggMCBvYmoK"
        "PDwvRmlsdGVyIC9GbGF0ZURlY29kZQovTGVuZ3RoIDMwNT4+IHN0cmVhbQp4nF2Rz26DMAzG73mKHLtDBaQFNgkh"
        "dWyVOOyPxvYAkJgu0ghRSA+8/RK77aRFgujn+Pts2UnTPrVGe568u1l24PmojXKwzGcngQ9w0oZlgist/YXwL6fe"
        "siSIu3XxMLVmnFlVcZ58hNfFu5VvDmoe4I4lb06B0+bEN19NF7g7W/sDExjPU1bXXMEYnF56+9pPwBOUbVsV3rVf"
        "t0Hzl/G5WuACOaNu5Kxgsb0E15sTsCoNp+bVMZyagVH/3nNSDaP87h1m70J2moq0jpRlRM9IokTa75HCFanIkPIG"
        "qXzAKhe/4up+a0aQSOTkRFrxSEGy2N+TfXElrLKj4IGClFmUFDwi5dR50VA/VCEnQSkubVEjcQ5xX7chy7NzYb64"
        "VBxsHKk2cNu7nW1Uxe8X++2cOQplbmRzdHJlYW0KZW5kb2JqCjQgMCBvYmoKPDwvVHlwZSAvRm9udAovU3VidHlw"
        "ZSAvVHlwZTAKL0Jhc2VGb250IC9BQUFBQUErQXJpYWxNVAovRW5jb2RpbmcgL0lkZW50aXR5LUgKL0Rlc2NlbmRh"
        "bnRGb250cyBbMTcgMCBSXQovVG9Vbmljb2RlIDE4IDAgUj4+CmVuZG9iagp4cmVmCjAgMTkKMDAwMDAwMDAwMCA2"
        "NTUzNSBmIAowMDAwMDAwMDE1IDAwMDAwIG4gCjAwMDAwMDEzNDYgMDAwMDAgbiAKMDAwMDAwMDEwOCAwMDAwMCBu"
        "IAowMDAwMDE5NzA1IDAwMDAwIG4gCjAwMDAwMDAxNDUgMDAwMDAgbiAKMDAwMDAwMTU2MyAwMDAwMCBuIAowMDAw"
        "MDAxOTk4IDAwMDAwIG4gCjAwMDAwMDE4MjEgMDAwMDAgbiAKMDAwMDAwMTYxOCAwMDAwMCBuIAowMDAwMDAxNjg1"
        "IDAwMDAwIG4gCjAwMDAwMDE3NTMgMDAwMDAgbiAKMDAwMDAwMTkwNSAwMDAwMCBuIAowMDAwMDAxOTQzIDAwMDAw"
        "IG4gCjAwMDAwMDIwODggMDAwMDAgbiAKMDAwMDAwMjI4MiAwMDAwMCBuIAowMDAwMDE4Njc4IDAwMDAwIG4gCjAw"
        "MDAwMTg5MTQgMDAwMDAgbiAKMDAwMDAxOTMyOSAwMDAwMCBuIAp0cmFpbGVyCjw8L1NpemUgMTkKL1Jvb3QgMTQg"
        "MCBSCi9JbmZvIDEgMCBSPj4Kc3RhcnR4cmVmCjE5ODQ0CiUlRU9GCg==")


def test_create_template() -> None:
    template = create_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert template is not None


def test_get_template() -> None:
    template = get_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert TEMPLATE_ID in template.name


def test_list_templates() -> None:
    templates = list_model_armor_templates(PROJECT_ID, LOCATION)
    assert TEMPLATE_ID in str(templates)


def test_user_prompt() -> None:
    response = sanitize_user_prompt(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert (
        response.sanitization_result.filter_match_state
        == modelarmor_v1.FilterMatchState.MATCH_FOUND
    )


def test_update_templates() -> None:
    template = update_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert (
        template.filter_config.pi_and_jailbreak_filter_settings.confidence_level
        == modelarmor_v1.DetectionConfidenceLevel.LOW_AND_ABOVE
    )


def test_delete_template() -> None:
    delete_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    with pytest.raises(NotFound) as exception_info:
        get_model_armor_template(PROJECT_ID, LOCATION, TEMPLATE_ID)
    assert TEMPLATE_ID in str(exception_info.value)


def test_create_model_armor_template_with_basic_sdp(
    project_id: str, location_id: str, template_id: str
) -> None:
    """
    Tests that the create_model_armor_template function returns a template name
    that matches the expected format.
    """
    created_template = create_model_armor_template_with_basic_sdp(
        project_id, location_id, template_id
    )
    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        created_template.name == expected_name_format
    ), "Template name does not match the expected format."

    filter_enforcement = (
        created_template.filter_config.sdp_settings.basic_config.filter_enforcement
    )

    assert (
        filter_enforcement.name == "ENABLED"
    ), f"Expected filter_enforcement to be ENABLED, but got {filter_enforcement}"


def test_create_model_armor_template_with_advanced_sdp(
    project_id: str, location_id: str, template_id: str, sdp_templates: Tuple[str, str]
) -> None:
    """
    Tests that the create_model_armor_template function returns a template name
    that matches the expected format.
    """

    sdr_inspect_template_id, sdr_deidentify_template_id = sdp_templates
    created_template = create_model_armor_template_with_advanced_sdp(
        project_id,
        location_id,
        template_id,
        sdr_inspect_template_id,
        sdr_deidentify_template_id,
    )

    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        created_template.name == expected_name_format
    ), "Template name does not match the expected format."

    advanced_config = created_template.filter_config.sdp_settings.advanced_config
    assert (
        advanced_config.inspect_template == sdr_inspect_template_id
    ), f"Expected inspect_template to be {sdr_inspect_template_id}, but got {advanced_config.inspect_template}"

    assert (
        advanced_config.deidentify_template == sdr_deidentify_template_id
    ), f"Expected deidentify_template to be {sdr_deidentify_template_id}, but got {advanced_config.deidentify_template}"


def test_create_model_armor_template_with_metadata(
    project_id: str, location_id: str, template_id: str
) -> None:
    """
    Tests that the create_model_armor_template function returns a template name
    that matches the expected format.
    """
    created_template = create_model_armor_template_with_metadata(
        project_id,
        location_id,
        template_id,
    )
    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        created_template.name == expected_name_format
    ), "Template name does not match the expected format."
    assert created_template.template_metadata.ignore_partial_invocation_failures
    assert created_template.template_metadata.log_sanitize_operations


def test_create_model_armor_template_with_labels(
    project_id: str, location_id: str, template_id: str
) -> None:
    """
    Tests that the test_create_model_armor_template_with_labels function returns a template name
    that matches the expected format.
    """
    expected_labels = {"name": "wrench", "count": "3"}

    created_template = create_model_armor_template_with_labels(
        project_id, location_id, template_id, labels=expected_labels
    )
    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        created_template.name == expected_name_format
    ), "Template name does not match the expected format."

    template_with_labels = get_model_armor_template(
        project_id, location_id, template_id
    )

    for key, value in expected_labels.items():
        assert (
            template_with_labels.labels.get(key) == value
        ), f"Label {key} does not match. Expected: {value}, Got: {template_with_labels.labels.get(key)}"


def test_list_model_armor_templates_with_filter(
    project_id: str,
    location_id: str,
    simple_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the list_model_armor_templates function returns a list of templates
    containing the created template.
    """
    template_id, _ = simple_template

    templates = list_model_armor_templates_with_filter(
        project_id, location_id, template_id
    )

    expected_template_name = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert any(
        template.name == expected_template_name for template in templates
    ), "Template does not exist in the list"


def test_model_response_with_basic_sdp_template(
    project_id: str,
    location_id: str,
    basic_sdp_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the model response is sanitized correctly with a basic sdp template
    """
    template_id, _ = basic_sdp_template

    model_response = "Here is my Email address: 1l6Y2@example.com Here is my phone number: 954-321-7890 Here is my ITIN: 988-86-1234"

    sanitized_response = sanitize_model_response(
        project_id, location_id, template_id, model_response
    )

    assert (
        "sdp" in sanitized_response.sanitization_result.filter_results
    ), "sdp key not found in filter results"

    sdp_filter_result = sanitized_response.sanitization_result.filter_results[
        "sdp"
    ].sdp_filter_result
    assert (
        sdp_filter_result.inspect_result.match_state.name == "MATCH_FOUND"
    ), "Match state was not MATCH_FOUND"

    info_type_found = any(
        finding.info_type == "US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER"
        for finding in sdp_filter_result.inspect_result.findings
    )
    assert (
        info_type_found
    ), "Info type US_INDIVIDUAL_TAXPAYER_IDENTIFICATION_NUMBER not found in any finding"


def test_model_response_with_advance_sdp_template(
    project_id: str,
    location_id: str,
    advance_sdp_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the model response is sanitized correctly with an advance sdp template
    """
    template_id, _ = advance_sdp_template
    model_response = "Here is my Email address: 1l6Y2@example.com Here is my phone number: 954-321-7890 Here is my ITIN: 988-86-1234"
    expected_value = "Here is my Email address: [REDACTED] Here is my phone number: [REDACTED] Here is my ITIN: [REDACTED]"

    sanitized_response = sanitize_model_response(
        project_id, location_id, template_id, model_response
    )
    assert (
        "sdp" in sanitized_response.sanitization_result.filter_results
    ), "sdp key not found in filter results"

    sanitized_text = next(
        (
            value.sdp_filter_result.deidentify_result.data.text
            for key, value in sanitized_response.sanitization_result.filter_results.items()
            if key == "sdp"
        ),
        "",
    )
    assert sanitized_text == expected_value


def test_update_model_armor_template_metadata(
    project_id: str,
    location_id: str,
    simple_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the update_model_armor_template function returns a template name
    that matches the expected format.
    """
    template_id, _ = simple_template

    updated_template = update_model_armor_template_metadata(
        project_id, location_id, template_id
    )

    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        updated_template.name == expected_name_format
    ), "Template name does not match the expected format."
    assert updated_template.template_metadata.ignore_partial_invocation_failures
    assert updated_template.template_metadata.log_sanitize_operations


def test_update_model_armor_template_labels(
    project_id: str,
    location_id: str,
    simple_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the test_update_model_armor_template_with_labels function returns a template name
    that matches the expected format.
    """
    expected_labels = {"name": "wrench", "count": "3"}

    template_id, _ = simple_template

    updated_template = update_model_armor_template_labels(
        project_id, location_id, template_id, expected_labels
    )
    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        updated_template.name == expected_name_format
    ), "Template name does not match the expected format."

    template_with_lables = get_model_armor_template(
        project_id, location_id, template_id
    )

    for key, value in expected_labels.items():
        assert (
            template_with_lables.labels.get(key) == value
        ), f"Label {key} does not match. Expected: {value}, Got: {template_with_lables.labels.get(key)}"


def test_update_model_armor_template_with_mask_configuration(
    project_id: str,
    location_id: str,
    simple_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    """
    Tests that the update_model_armor_template function returns a template name
    with mask configuration.
    """
    template_id, _ = simple_template

    updated_template = update_model_armor_template_with_mask_configuration(
        project_id, location_id, template_id
    )

    expected_name_format = (
        f"projects/{project_id}/locations/{location_id}/templates/{template_id}"
    )

    assert (
        updated_template.name == expected_name_format
    ), "Template name does not match the expected format."

    filter_enforcement = (
        updated_template.filter_config.sdp_settings.basic_config.filter_enforcement
    )
    assert (
        filter_enforcement.name != "ENABLED"
    ), f"Expected filter_enforcement not to be ENABLED, but got {filter_enforcement}"


def test_screen_pdf_file(
    project_id: str,
    location_id: str,
    basic_sdp_template: Tuple[str, modelarmor_v1.FilterConfig],
    pdf_content_base64: str,
) -> None:
    template_id, _ = basic_sdp_template

    response = screen_pdf_file(
        project_id, location_id, template_id, pdf_content_base64
    )

    assert (
        response.sanitization_result.filter_match_state
        == modelarmor_v1.FilterMatchState.MATCH_FOUND
    )


def test_sanitize_model_response_with_user_prompt(
    project_id: str,
    location_id: str,
    advance_sdp_template: Tuple[str, modelarmor_v1.FilterConfig],
) -> None:
    template_id, _ = advance_sdp_template

    user_prompt = "How can i make my email address test@dot.com make available to public for feedback"
    model_response = "You can make support email such as contact@email.com for getting feedback from your customer"

    sanitized_response = sanitize_model_response_with_user_prompt(
        project_id, location_id, template_id, model_response, user_prompt
    )

    assert (
        sanitized_response.sanitization_result.filter_match_state
        == modelarmor_v1.FilterMatchState.MATCH_FOUND
    )


def test_quickstart(project_id: str, location_id: str, template_id: str) -> None:
    quickstart(project_id, location_id, template_id)


def test_update_organization_floor_settings() -> None:
    organization_id = "123456789"
    response = update_organization_floor_settings(organization_id)

    assert response.enable_floor_setting_enforcement
    print("Organization floor settings updated successfully.")


def test_update_folder_floor_settings() -> None:
    folder_id = "987654321"
    response = update_folder_floor_settings(folder_id)

    assert response.enable_floor_setting_enforcement


def test_update_project_floor_settings(floor_settings_project_id: str) -> None:
    response = update_project_floor_settings(floor_settings_project_id)

    assert response.enable_floor_setting_enforcement


def test_get_organization_floor_settings() -> None:
    organization_id = "123456789"
    expected_floor_settings_name = (
        f"organizations/{organization_id}/locations/global/floorSetting"
    )
    response = get_organization_floor_settings(organization_id)

    assert response.name == expected_floor_settings_name
    print("Organization floor settings retrieved successfully.")


def test_get_folder_floor_settings() -> None:
    folder_id = "987654321"
    expected_floor_settings_name = f"folders/{folder_id}/locations/global/floorSetting"
    response = get_folder_floor_settings(folder_id)

    assert response.name == expected_floor_settings_name
    print("Folder floor settings retrieved successfully.")


def test_get_project_floor_settings(project_id: str) -> None:
    expected_floor_settings_name = (
        f"projects/{project_id}/locations/global/floorSetting"
    )
    response = get_project_floor_settings(project_id)

    assert response.name == expected_floor_settings_name
