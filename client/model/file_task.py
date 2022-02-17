from client.api.base_class import BaseAPIClass
from config import ConfigClass

# TODO since upload/download/delete have different status enum
# so might be have a base class. and give an abstraction for the enum


class ProjectFileTaskManager(BaseAPIClass):

    project_file_task_url = ConfigClass.project_file_task_url
    label = 'Container'

    def check_status(self, action, project_code, session_id, job_id='*'):

        query_params = {
            'action': action,
            'project_code': project_code,
            'session_id': session_id,
            # "job_id": job_id,
        }

        res = self._send_request(self.project_file_task_url, method='GET', params=query_params)

        # since we only do operation per file
        return res.json().get('result')[0]
