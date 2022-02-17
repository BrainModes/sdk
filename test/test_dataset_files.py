import time
import unittest

from client.api.dataset_files import DatasetFileApis
from client.api.datasets import DatasetApis
from client.api.projects import ProjectApis
from client.client import PILOT


class TestDatasetFiles(unittest.TestCase):

    test_dataset = 'pilotsdktestdataset%s' % (int(time.time()))

    test_project = 'indoctestproject'

    file_set = [
        'c985a301-0ab6-4ea5-af25-20471f424d8d-1626980567',  # File
        'cf11a0dc-eda4-4a15-91c8-c8ba3af24956-1626711449',  # Folder
    ]

    @classmethod
    def setUpClass(self):
        # initialize the api object
        client = PILOT(username='admin', password='admin')
        self.dataset_files_apis = DatasetFileApis(client)
        # self.dataset_files_apis.track_off()

        self.dataset_apis = DatasetApis(client)
        self.dataset_apis.track_off()

        self.project_apis = ProjectApis(client)
        self.project_apis.track_off()

        # # create new dataset
        # res = self.dataset_apis.create_dataset(
        #     title=self.test_dataset,
        #     code=self.test_dataset,
        #     description=self.test_dataset,
        # )
        self.test_dataset_geid = '39a13d12-7d62-4eba-9110-128af0e4068f-1645068638'

        # get source project
        res = self.project_apis.list_projects(code=self.test_project, is_all=True)
        self.test_project_geid = res[0].get('global_entity_id')

    def test_01_import_files(self):
        self.dataset_files_apis.import_files(
            dataset_geid=self.test_dataset_geid, source_project_geid=self.test_project_geid, source_list=self.file_set
        )

        time.sleep(1)

    def test_02_list_files(self):
        res = self.dataset_files_apis.list_files(
            dataset_geid=self.test_dataset_geid,
        )

        # first item is folder, second is file
        self.__class__.dataset_files = res

        assert len(res) == 2

    def test_03_rename_files(self):
        res = self.dataset_files_apis.rename_file(
            dataset_geid=self.test_dataset_geid,
            file_geid=self.dataset_files[1].get('global_entity_id'),
            new_name='new_name.txt',
        )
        assert res[-1]['payload']['payload'].get('name') == 'new_name.txt'
        self.__class__.dataset_files[1] = res[-1]['payload']['payload']

        time.sleep(1)

    def test_04_move_files(self):
        self.dataset_files_apis.move_files(
            dataset_geid=self.test_dataset_geid,
            source_files=[self.dataset_files[1].get('global_entity_id')],
            target_folder_geid=self.dataset_files[0].get('global_entity_id'),
        )

        # print(res)
        time.sleep(1)

    def test_05_duplicate_import_file(self):
        # since above we move one file into folder
        # if we import again, then one of the file will be duplicate
        # block one import
        res = self.dataset_files_apis.import_files(
            dataset_geid=self.test_dataset_geid, source_project_geid=self.test_project_geid, source_list=self.file_set
        )

        time.sleep(1)

    def test_06_list_files(self):
        res = self.dataset_files_apis.list_files(
            dataset_geid=self.test_dataset_geid,
        )

        # first item is folder, second is file
        self.__class__.dataset_files = res

        assert len(res) == 2

    def test_07_duplicate_move_file(self):
        # since above we move one file into folder
        # if we import again, then one of the file will be duplicate
        # block one import
        t1, t2 = self.dataset_files[0].get('global_entity_id'), self.dataset_files[1].get('global_entity_id')
        file_geid, folder_geid = (t1, t2) if self.dataset_files[0].get('labels') == ['File'] else (t2, t1)

        res = self.dataset_files_apis.move_files(
            dataset_geid=self.test_dataset_geid, source_files=[file_geid], target_folder_geid=folder_geid
        )

        # print(res)
        time.sleep(1)

    def test_08_delete_files(self):
        res = self.dataset_files_apis.delete_files(
            dataset_geid=self.test_dataset_geid, source_list=[x.get('global_entity_id') for x in self.dataset_files]
        )

        # print(res)
        time.sleep(1)

    def test_09_list_files_empty(self):
        res = self.dataset_files_apis.list_files(
            dataset_geid=self.test_dataset_geid,
        )

        assert len(res) == 0
