import unittest
import json

from ..flask_app import services

class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        return

    def test_time(self):
        server_time = services.get_time()
        self.assertIsNotNone(server_time)
        print(json.dumps(server_time.to_dict()))
