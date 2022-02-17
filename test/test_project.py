import time
import unittest

from client.api.projects import ProjectApis
from client.client import PILOT
from client.exceptions import Conflict


class TestAuthentication(unittest.TestCase):

    test_project = 'pilotsdktestproject%s' % (int(time.time()))

    @classmethod
    def setUpClass(self):
        self.client = self.client = PILOT(username='admin', password='admin')
        self.project_apis = ProjectApis(self.client)
        self.project_apis.track_off()

    def test_01_create_project(self):

        self.project_apis.create_project(
            name=self.test_project,
            code=self.test_project,
            description=self.test_project,
        )

    def test_02_create_project_conflict(self):
        try:
            self.project_apis.create_project(
                name=self.test_project,
                code=self.test_project,
                description=self.test_project,
            )
        except Conflict:
            assert True
        except Exception:
            raise AssertionError()

    def test_03_list_all(self):

        res = self.project_apis.list_projects()

        assert len(res) > 0

    def test_04_list_all_filter_name(self):

        res = self.project_apis.list_projects(code=self.test_project, is_all=True)
        assert len(res) > 0
        assert res[0].get('code') == self.test_project

        self.__class__.project_geid = res[0].get('global_entity_id')

    def test_05_get_project_by_geid(self):

        res = self.project_apis.get_project_by_geid(self.project_geid)
        assert len(res) > 0
        assert res.get('code') == self.test_project
