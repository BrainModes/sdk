import json
import math
import os
import time
import uuid
from functools import wraps

import jwt

from client.api.base_class import BaseAPIClass
from client.api.projects import ProjectApis
from client.model.file_task import ProjectFileTaskManager
from config import ConfigClass


class ProjectFilesApis(BaseAPIClass):
    FILE_COPY_JOB = 'data_transfer'
    FILE_DELE_JOB = 'data_delete'

    def _wait_file_task(job_type):
        def decorator(func):
            def wrapper(self, project_geid, *args, **kwargs):
                # print('====== Running long polling for', job_type)
                if not project_geid:
                    project_geid = kwargs.get('project_geid')

                res = func(self, project_geid, *args, **kwargs)

                session_id = res[0].get('session_id', None)
                # the job status long pulling
                project_apis = ProjectApis(self.client)
                # project_apis.track_off()
                res = project_apis.get_project_by_geid(project_geid)
                project_code = res.get('code', None)

                # long polling to wait for job done
                file_task_manager = ProjectFileTaskManager(self.client)
                while 1:
                    res = file_task_manager.check_status(job_type, project_code, session_id)
                    if res.get('status') != 'RUNNING':
                        return res
                    time.sleep(2)

                return project_geid

            return wrapper

        return decorator

    def list_child_entities(
        self,
        project_geid,
        folder_geid=None,
        page=0,
        page_size=10,
        order_by='time_created',
        order_type='desc',
        query={'archived': False},
        partial=[],
        zone='Greenroom',
        source_type='Folder',
    ):

        """Function Summary: The function will list the folder and files under the target geid.

        Args:
            project_geid (string): unique identifier of entity
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
            partial (list): ?
            zone (string): "Greenroom" or "Core"
            source_type (string): 'Project', 'Folder', 'TrashFile', 'Collection'

        Returns:
            list of file and folder node

        Examples:
            >>> PFA = ProjectFilesApis(pilot_client)
            >>> # list all the folder/files under the project(not the grandchild)
            >>> res = PFA.list_child_entities(<project_geid>)

            >>> # list all the folder/files under the folder in project
            >>> res = PFA.list_child_entities(<project_geid>, folder_geid="<some_folder_geid>")

            >>> # list folder/files with the name query
            >>> res = PFA.list_child_entities(<project_geid>, query={"name":"<file_name>"})
        """

        query.update({'archived': False})
        query_params = {
            'project_geid': project_geid,
            'page': page,
            'page_size': page_size,
            'order_by': order_by,
            'order_type': order_type,
            'zone': zone,
            'source_type': source_type,
            'partial': json.dumps(partial),
            'query': json.dumps(query),
        }

        url = ConfigClass.project_file_meta_url
        if folder_geid:
            url += folder_geid
        res = self._send_request(url, method='GET', params=query_params)

        return res.json().get('result', {}).get('data', [])

    @_wait_file_task(job_type=FILE_COPY_JOB)
    def copy_to_core(self, project_geid, source_geids: list, target_geid: str):
        """Function Summary: The function will copy a list of file from greenroom to the core zone.

        Args:
            project_geid (string): unique identifier of entity
            source_geids (list): a list of geid for copy. Note the geid must from
                target project geid.
            target_geid (string): the destination folder geid.

        Returns:
            list of file and folder node has been copied

        Examples:
            >>> PFA = ProjectFilesApis(pilot_client)
            >>> res = PFA.copy_to_core("<project_geid>", source_geids=[{"geid":"<file_geid>"}])
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {
            'payload': {'targets': source_geids, 'destination': target_geid},
            'operator': self.client.username,
            'operation': 'copy',
            'project_geid': project_geid,
        }
        header = {
            'Session-ID': session_id,
        }

        url = ConfigClass.project_file_action_url
        copy_res = self._send_request(url, method='POST', json=payload, headers=header)

        return copy_res.json().get('result', [])

    @_wait_file_task(job_type=FILE_DELE_JOB)
    def delete_entity(self, project_geid, targets: list):
        """Function Summary: The function will delete a list of file under the project.

        Args:
            project_geid (string): unique identifier of entity
            targets (list): a list of geid for deletion. Note the geid must from
                target project geid.

        Returns:
            list of file and folder node has been deleted

        Examples:
            >>> PFA = ProjectFilesApis(pilot_client)
            >>> res = PFA.delete_entity("<project_geid>", targets=[{"geid":"<file_geid>"}])
        """

        session_id = self.client.username + '-' + str(uuid.uuid4())
        payload = {
            'operation': 'delete',
            'operator': self.client.username,
            'payload': {'targets': targets},
            'project_geid': project_geid,
            'session_id': session_id,
        }
        header = {
            'Session-ID': session_id,
        }

        url = ConfigClass.project_file_action_url
        delete_res = self._send_request(url, method='POST', json=payload, headers=header)

        # todo update return in original api
        res_json = delete_res.json().get('result', [])
        res_json.append({'session_id': session_id})

        return res_json

    def fput_file_entity(self, project_code, source_file_path, target_path=''):
        """Function Summary: The function will read the input file and upload with chunks(2MB). The defualt path is user
        name space. if target path is specified than it will upload to <username>/<target_path>

        Args:
            project_code (string): project code
            source_file_path (string): the file path on the local file system
            target_path (string): the optional params for the upload to some subfolder

        Returns:
            the status of the file operation

        Examples:
            >>> PFA = ProjectFilesApis(pilot_client)
            >>> # under the root
            >>> PFA.fput_file_entity(<project_code>, <your_file_path>)

            >>> # to some subfolder
            >>> PFA.fput_file_entity(<project_code>, <your_file_path>, target_path="test0913")
        """

        filename = os.path.basename(source_file_path)
        # TODO unify the sessionid
        session_id = self.client.username + '-' + str(uuid.uuid4())

        resumable_relative_path = self.client.username + '/' + target_path if target_path else self.client.username
        # do pre upload
        pre_payload = {
            'project_code': project_code,
            'operator': self.client.username,
            'job_type': 'AS_FILE',
            'data': [{'resumable_filename': filename, 'resumable_relative_path': resumable_relative_path}],
            'upload_message': '',
            'current_folder_node': target_path,
        }
        header = {
            'Session-ID': session_id,
        }

        url = ConfigClass.pre_upload_url
        upload_pre_res = self._send_request(url, method='POST', json=pre_payload, headers=header)
        print(upload_pre_res.json())
        upload_pre_res = upload_pre_res.json().get('result')[0]
        resumable_identifier = upload_pre_res.get('payload', {}).get('resumable_identifier')

        # for loop to cut the chunks
        chunk_size = 1024 * 1024 * 2  # 2MB TODO update to config
        chunk_number = 1
        total_file_size = os.path.getsize(source_file_path)
        total_chunk_number = math.ceil(total_file_size / chunk_size)
        # print(total_file_size, total_chunk_number)

        f = open(source_file_path, 'rb')
        while 1:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            chunk_payload = {
                'project_code': project_code,
                'operator': self.client.username,
                'resumable_identifier': resumable_identifier,
                'resumable_filename': filename,
                'resumable_relative_path': resumable_relative_path,
                'resumable_dataType': 'SINGLE_FILE_DATA',
                'resumable_chunk_number': chunk_number,
                'resumable_chunk_size': chunk_size,
                'resumable_total_chunks': total_chunk_number,
                'resumable_total_size': total_file_size,
                'dcm_id': None,
                'tags': [],
            }

            files = {'chunk_data': chunk}

            upload_url = ConfigClass.chunk_upload_url
            upload_pre_res = self._send_request(
                upload_url, method='POST', data=chunk_payload, headers=header, files=files
            )
            print(upload_pre_res.json())

            chunk_number += 1  # uploaded successfully

        print('chunk uploading done..')

        # do combine chunks
        combine_payload = {
            'project_code': project_code,
            'operator': self.client.username,
            'resumable_identifier': resumable_identifier,
            'resumable_filename': filename,
            'resumable_relative_path': resumable_relative_path,
            'resumable_total_chunks': total_chunk_number,
            'resumable_total_size': total_file_size,
        }

        combine_url = ConfigClass.combine_chunk_url
        combine_res = self._send_request(combine_url, method='POST', json=combine_payload, headers=header)
        # print(combine_res.json())
        job_id = combine_res.json().get('result', {}).get('job_id')
        # print(job_id)

        # get the status
        task_url = ConfigClass.upload_status_url
        task_param = {
            'project_code': project_code,
            'operator': self.client.username,
        }
        while 1:
            res = self._send_request(task_url, method='GET', params=task_param, headers=header)
            status = res.json().get('result', [])[0]
            if status.get('status') == 'SUCCEED':
                break
            time.sleep(2)

        return status

    def fget_file_entity(self, project_code, source_geids: list):
        """Function Summary: The function will send the request to PILOT service to prepare the download. if the job
        status changed from `ZIPPING`. it will request the file stream and read it byte by byte to the local file.

        Args:
            project_code (string): project code
            source_geids (list of string): the file geid from system

        Returns:
            the status of the download file operation

        Examples:
            >>> PFA = ProjectFilesApis(pilot_client)
            >>> res = PFA.fget_file_entity(<project_code>, [<geid1>, <geid2>])
        """

        # send pre download request
        session_id = self.client.username + '-' + str(uuid.uuid4())
        pre_payload = {
            'files': [{'geid': x} for x in source_geids],
            'project_code': project_code,
            'operator': self.client.username,
            'session_id': session_id,
        }
        header = {
            'Session-ID': session_id,
        }

        url = ConfigClass.pre_download_url
        upload_pre_res = self._send_request(url, method='POST', json=pre_payload, headers=header)
        hash_code = upload_pre_res.json().get('result', {}).get('payload', {}).get('hash_code', None)
        # zone = upload_pre_res.json().get("result", {}).get("payload", {}).get("zone", "")

        # loop to check if file prepared
        # TODO after update the task api change to task object
        task_url = ConfigClass.download_status_url % (hash_code)
        while 1:
            file_download_res = self._send_request(task_url, method='GET', headers=header)
            status = file_download_res.json().get('result', {})
            if status.get('status') != 'ZIPPING':
                break
            time.sleep(2)

        # download to local
        download_url = ConfigClass.download_url % (hash_code)
        download_name = jwt.decode(hash_code, options={'verify_signature': False}, algorithms=['HS256'])
        download_name = os.path.basename(download_name.get('full_path'))
        # here the request is in stream mode, since we request the file which might
        # be very large. It will save the file byte by byte to avoid blowing up the memory
        with self._send_request(download_url, method='GET', stream=True) as r:
            r.raise_for_status()
            with open(download_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        return file_download_res.json().get('result', {})
