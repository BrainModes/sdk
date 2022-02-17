import json
import uuid

from client.api.base_class import BaseAPIClass
from client.model.file_task_socket import DatasetFileTaskManager
from config import ConfigClass


class DatasetFileApis(BaseAPIClass):
    def import_files(self, dataset_geid, source_project_geid, source_list: list):

        """Function Summary: The function import the designated folders/files(geid) from source project to the dataset.
        Note for now the dataset will only allow to import from same project.

        Args:
            dataset_geid (string): unique identifier of entity for dataset
            source_project_geid (string): unique identifier of entity for project
            source_list (list of string): list of folder/files geid will be import
                to dataset

        Returns:
            the job status of each file. The status will have the detail of new node

        Examples:
            >>> DFA = DatasetFileApis(pilot_client)
            >>> # res = DFA.import_files(
                    dataset_geid=<dataset_geid>,
                    source_project_geid=<project_geid>,
                    source_list=[<file_geid>, <folder_geid>])
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {
            'source_list': source_list,
            'operator': self.client.username,
            'project_geid': source_project_geid,
        }
        cookies = {
            'sessionId': session_id,
        }

        url = ConfigClass.dataset_files_url % (dataset_geid)
        res = self._send_request(url, method='PUT', json=payload, cookies=cookies)

        # NOTE: we might have the duplicate import, base on the return to waiting
        # the message for the job status. if all files are block we just quit.
        processed_geid = [x.get('global_entity_id') for x in res.json().get('result')['processing']]

        # todo update endpoint to config
        if len(processed_geid) > 0:
            task_manager = DatasetFileTaskManager(
                socketio_endpoint=ConfigClass.socketio_endpoint,
                dataset_geid=dataset_geid,
                source_geids=processed_geid,
                action='dataset_file_import',
                session_id=session_id,
            )
            # then use socketio to wait for the job done
            task_manager.wait_response()

        return res.json().get('result', {})

    def list_files(
        self, dataset_geid, folder_geid=None, page=0, page_size=25, order_by='create_time', order_type='desc', query={}
    ):

        """Function Summary: The function will list the folder and files under the target geid.

        Args:
            dataset_geid (string): unique identifier of entity
            folder_geid (string): will list the folder/file under the geid if specified
                else will list the folder/file under project.
            order_by (string): possible order string:
                - "time_created": project created time
                - "name": project name
                - "code": project code
            order_type (string): increasing order(asc) or decreasing order(desc)
            page_size (int): page size for the result(eg limit)
            page (int): page number(eg. skip = page_size*page)
            query (dict): dict of attribute that you want to search

        Returns:
            list of file and folder node under given dataset

        Examples:
            >>> DFA = DatasetFileApis(pilot_client)
            >>> # list all the folder/files under the dataset(not the grandchild)
            >>> res = DFA.list_child_entities(<dataset_geid>)

            >>> # list all the folder/files under the folder in dataset
            >>> res = DFA.list_child_entities(<dataset_geid>, folder_geid="<some_folder_geid>")
        """

        query_params = {
            'page': page,
            'page_size': page_size,
            'order_by': order_by,
            'order_type': order_type,
            'query': json.dumps(query),
        }
        if folder_geid:
            query_params.update({'folder_geid': folder_geid})

        url = ConfigClass.dataset_files_url % (dataset_geid)
        res = self._send_request(url, method='GET', params=query_params)

        return res.json().get('result', {}).get('data', [])

    def delete_files(self, dataset_geid, source_list: list):
        """Function Summary: The function delete the designated folders/files(geid) from target dataset.

        Args:
            dataset_geid (string): unique identifier of entity for dataset
            source_list (list of string): list of file/folder that will be deleted

        Returns:
            the job status of each file. The status will have the detail of new node

        Examples:
            >>> DFA = DatasetFileApis(pilot_client)
            >>> # res = DFA.delete_files(
                    dataset_geid=<dataset_geid>,
                    source_list=[<file_geid>, <folder_geid>])
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {
            'source_list': source_list,
            'operator': self.client.username,
        }
        cookies = {
            'sessionId': session_id,
        }

        url = ConfigClass.dataset_files_url % (dataset_geid)
        res = self._send_request(url, method='DELETE', json=payload, cookies=cookies)

        # NOTE: we might have the duplicate import, base on the return to waiting
        # the message for the job status. if all files are block we just quit.
        processed_geid = [x.get('global_entity_id') for x in res.json().get('result')['processing']]

        # todo update endpoint to config
        if len(processed_geid) > 0:
            task_manager = DatasetFileTaskManager(
                socketio_endpoint=ConfigClass.socketio_endpoint,
                dataset_geid=dataset_geid,
                source_geids=processed_geid,
                action='dataset_file_delete',
                session_id=session_id,
            )
            # then use socketio to wait for the job done
            task_res = task_manager.wait_response()

        return res.json().get('result', {})

    def move_files(self, dataset_geid, source_files: list, target_folder_geid: str):
        """Function Summary: The function move the designated folders/files(geid) within the dataset.

        Args:
            dataset_geid (string): unique identifier of entity for dataset
            source_files (list of string): list of file/folder that will be moved
            target_folder_geid (string): the target folder you want to move. this
                can be the datset geid.

        Returns:
            the job status of each file. The status will have the detail of new node

        Examples:
            >>> DFA = DatasetFileApis(pilot_client)
            >>> # res = DFA.move_files(
                    dataset_geid=<dataset_geid>,
                    target_folder_geid=<folder_geid>,
                    source_files=[<file_geid>, <folder_geid>])
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {'source_list': source_files, 'operator': self.client.username, 'target_geid': target_folder_geid}
        cookies = {
            'sessionId': session_id,
        }

        url = ConfigClass.dataset_files_url % (dataset_geid)
        res = self._send_request(url, method='POST', json=payload, cookies=cookies)
        # NOTE: we might have the duplicate import, base on the return to waiting
        # the message for the job status. if all files are block we just quit.
        processed_geid = [x.get('global_entity_id') for x in res.json().get('result')['processing']]

        # todo update endpoint to config
        if len(processed_geid) > 0:
            task_manager = DatasetFileTaskManager(
                socketio_endpoint=ConfigClass.socketio_endpoint,
                dataset_geid=dataset_geid,
                source_geids=processed_geid,
                action='dataset_file_move',
                session_id=session_id,
            )
            # then use socketio to wait for the job done
            task_res = task_manager.wait_response()

        return task_res

    def rename_file(self, dataset_geid, file_geid: str, new_name: str):

        """Function Summary: The function rename the target file into new name. cannot rename to the old name.

        Args:
            dataset_geid (string): unique identifier of entity for dataset
            file_geid (string): unique identifier of target file
            new_name (string): the new name string

        Returns:
            the job status of target file. The status will have the detail of new node

        Examples:
            >>> DFA = DatasetFileApis(pilot_client)
            >>> # res = DFA.rename_file(
                    dataset_geid=<dataset_geid>,
                    file_geid=<file_geid>,
                    new_name="new name")
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {
            'new_name': new_name,
            'operator': self.client.username,
        }
        cookies = {
            'sessionId': session_id,
        }

        url = ConfigClass.dataset_file_ops_url % (dataset_geid, file_geid)
        res = self._send_request(url, method='POST', json=payload, cookies=cookies)
        # NOTE: we might have the duplicate import, base on the return to waiting
        # the message for the job status. if all files are block we just quit.
        processed_geid = [x.get('global_entity_id') for x in res.json().get('result')['processing']]

        # todo update endpoint to config
        if len(processed_geid) > 0:
            task_manager = DatasetFileTaskManager(
                socketio_endpoint=ConfigClass.socketio_endpoint,
                dataset_geid=dataset_geid,
                source_geids=processed_geid,
                action='dataset_file_rename',
                session_id=session_id,
            )
            # then use socketio to wait for the job done
            task_res = task_manager.wait_response()

        return task_res
