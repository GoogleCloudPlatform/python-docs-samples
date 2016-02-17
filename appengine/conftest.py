import testing.appengine


def pytest_configure(config):
    testing.appengine.setup_sdk_imports()


def pytest_runtest_call(item):
    testing.appengine.import_appengine_config()
