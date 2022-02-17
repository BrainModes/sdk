import time
import unittest

from client.api.project_files import ProjectFilesApis
from client.api.projects import ProjectApis
from client.client import PILOT


class TestAuthentication(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = self.client = PILOT(username='admin', password='admin')
        self.project_apis = ProjectApis(self.client)
        self.project_apis.track_off()

        self.project_files_apis = ProjectFilesApis(self.client)
        # self.project_files_apis.track_off()

        res = self.project_apis.list_projects()

        self.test_geid = res[0].get('global_entity_id')
        self.test_project = res[0].get('code')

    def test_01_list_files(self):
        res = self.project_files_apis.list_child_entities(project_geid=self.test_geid)
        self.__class__.current_file_number = len(res)

    def test_02_upload_files(self):
        res = self.project_files_apis.fput_file_entity(self.test_project, './requirements.txt')
        self.__class__.file_geid = res['payload'].get('source_geid')

    def test_03_list_files(self):
        res = self.project_files_apis.list_child_entities(project_geid=self.test_geid)
        assert self.current_file_number + 1 == len(res)

    def test_04_down_files(self):
        res = self.project_files_apis.fget_file_entity(project_code=self.test_project, source_geids=[self.file_geid])

        assert res.get('status') == 'READY_FOR_DOWNLOADING'

    def test_05_remove_file(self):
        res = self.project_files_apis.delete_entity(project_geid=self.test_geid, targets=[{'geid': self.file_geid}])

        assert res.get('status') == 'SUCCEED'
