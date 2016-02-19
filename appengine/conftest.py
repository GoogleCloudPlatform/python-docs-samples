import pytest
import testing.appengine


def pytest_configure(config):
    testing.appengine.setup_sdk_imports()


def pytest_runtest_call(item):
    testing.appengine.import_appengine_config()


@pytest.yield_fixture
def testbed():
    testbed = testing.appengine.setup_testbed()
    yield testbed
    testbed.deactivate()


@pytest.fixture
def login(testbed):
    def _login(email='user@example.com', id='123', is_admin=False):
        testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)
    return _login


@pytest.fixture
def run_tasks(testbed):
    def _run_tasks(app):
        testing.appengine.run_tasks(testbed, app)
    return _run_tasks
