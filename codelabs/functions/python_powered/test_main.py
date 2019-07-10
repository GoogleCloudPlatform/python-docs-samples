from unittest import TestCase
from unittest.mock import Mock

from main import hello_name, hello_world


class TestHello(TestCase):
    def test_hello_world(self):
        req = Mock()

        # Call tested function
        assert hello_world(req) == "Hello World!"

    def test_hello_name_no_name(self):
        req = Mock(args={})

        # Call tested function
        assert hello_name(req) == "Hello World!"

    def test_hello_name_with_name(self):
        name = "test"
        req = Mock(args={"name": name})

        # Call tested function
        assert hello_name(req) == "Hello {}!".format(name)
