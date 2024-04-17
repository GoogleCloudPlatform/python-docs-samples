import pytest
import os
import re

from google.cloud.iam_admin_v1 import Role

from snippets.disable_role import disable_role
from snippets.edit_role import edit_role
from snippets.get_role import get_role
from snippets.delete_role import delete_role, undelete_role
from snippets.list_roles import list_roles


PROJECT_ID = os.environ["IAM_PROJECT_ID"]


def test_retrieve_role(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    # Test role retrieval, given the iam role id.
    get_role(PROJECT_ID, iam_role)
    out, _ = capsys.readouterr()
    assert re.search(f"Retrieved role: {iam_role}", out)


def test_delete_undelete_role(
    capsys: "pytest.CaptureFixture[str]", iam_role: str
) -> None:
    deleted_role = delete_role(PROJECT_ID, iam_role)
    out, _ = capsys.readouterr()
    assert re.search(f"Deleted role: {iam_role}", out)
    assert deleted_role.deleted

    undeleted_role = undelete_role(PROJECT_ID, iam_role)
    out, _ = capsys.readouterr()
    assert re.search(f"Undeleted role: {iam_role}", out)
    assert not undeleted_role.deleted


def test_list_roles(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    # Test role list retrieval, given the iam role id should be listed.
    list_roles(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert re.search(iam_role, out)
    assert re.search("iam roles", out)


def test_edit_role(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    role = get_role(PROJECT_ID, iam_role)
    title = "updated role title"
    role.title = title
    edit_role(role)
    out, _ = capsys.readouterr()
    assert re.search(f"Edited role: {role.name}", out)
    assert re.search(f'title: "{title}"', out)


def test_disable_role(capsys: "pytest.CaptureFixture[str]", iam_role: str) -> None:
    role = disable_role(PROJECT_ID, iam_role)
    out, _ = capsys.readouterr()
    assert re.search(f"Disabled role: {iam_role}", out)
    assert role.stage == Role.RoleLaunchStage.DISABLED
