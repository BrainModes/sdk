import time
import unittest

from client.api.datasets import DatasetApis
from client.client import PILOT


class TestDataset(unittest.TestCase):

    test_dataset = 'pilotsdktestdataset%s' % (int(time.time()))

    client = None

    @classmethod
    def setUpClass(self):
        self.client = PILOT(username='admin', password='admin')
        self.dataset_apis = DatasetApis(self.client)
        self.dataset_apis.track_off()

    def test_01_list_dataset(self):

        res = self.dataset_apis.list_dataset()

        assert len(res) > 0

    def test_02_create_dataset(self):

        res = self.dataset_apis.create_dataset(
            title=self.test_dataset,
            code=self.test_dataset,
            description=self.test_dataset,
        )

        assert res.get('code') == self.test_dataset
