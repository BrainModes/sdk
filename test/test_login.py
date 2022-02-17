import unittest

from client.client import PILOT
from client.exceptions import AuthenticationError


class TestAuthentication(unittest.TestCase):
    def test_01_login(self):
        pilot_client = self.client = PILOT(username='admin', password='admin')

    def test_02_login_fail(self):
        try:
            pilot_client = PILOT(username='admin', password='admin1')
        except AuthenticationError:
            pass
        except Exception as e:
            assert False
