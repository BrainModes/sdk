from client.api.base_class import BaseAPIClass
from config import ConfigClass


class ProjectUsersApis(BaseAPIClass):
    def list_users(self, project_geid):

        url = ConfigClass.project_list_user_url % project_geid
        res = self._send_request(url, method='GET')

        return res.json().get('result', {})

    def update_user_role(self, project_geid, username, old_role, new_role):

        payload = {
            'old_role': old_role,
            'new_role': new_role,
        }

        url = ConfigClass.project_user_ops_url % (project_geid, username)
        res = self._send_request(url, method='PUT', json=payload)

        return res.json().get('result', {})
