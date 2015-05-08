import unittest
from test import RESOURCE_PATH
import json
import os


class BaseBigqueryTest(unittest.TestCase):

    def setUp(self):
        with open(
                os.path.join(RESOURCE_PATH, 'constants.json'),
                'r') as constants_file:

            self.constants = json.load(constants_file)
