from client.api.base_class import BaseAPIClass
from client.model.validator import array_of_string_vali
from config import ConfigClass


class ProjectApis(BaseAPIClass):
    def list_projects(
        self,
        order_by='time_created',
        order_type='desc',
        page_size=10,
        page=0,
        name=None,
        code=None,
        tags=None,
        description=None,
        create_time_start=None,
        create_time_end=None,
        is_all=False,
    ):

        """Function Summary: List the project by the query parameters.

        Args:
            order_by (string): possible order string:
                - "time_created": project created time
                - "name": project name
                - "code": project code
            order_type (string): increasing order(asc) or decreasing order(desc)
            page_size (int): page size for the result(eg limit)
            page (int): page number(eg. skip = page_size*page)
            name (string): project name
            code (string): project code
            tags (list of string): searching parameter for list
            description (string): searching parameter for description
            create_time_start (int): start timestamp for searching create time range
            create_time_end (int): end timestamp for searching create time range
            is_all (bool): indicate if user want to fetch their own projects OR all projects

        Returns:
            list of projects

        Examples:
            >>> PA = ProjectApis(pilot_client)
            >>> # get all project
            >>> PA.list_projects()

            >>> # list first 10 project
            >>> res = PA.list_projects(page_size=10)
        """
        if not tags:
            tags = []

        query_params = {
            'order_by': order_by,
            'order_type': order_type,
            'page_size': page_size,
            'page': page,
            'name': name,
            'code': code,
            'tags': tags,
            'description': description,
            'create_time_start': create_time_start,
            'create_time_end': create_time_end,
        }

        res = None
        # we have two api to query the project, one is for all project, another
        # is to query own project
        if is_all:
            url = ConfigClass.list_all_project_url
            res = self._send_request(url, method='GET', params=query_params)
        else:
            url = ConfigClass.list_project_by_user_url % (self.client.username)
            res = self._send_request(url, method='POST', json=query_params)

        # TODO need object??
        return res.json().get('result', [])

    def create_project(self, name, code, tags=None, description='', discoverable=True):
        """Function Summary: create new project based on name/code.

        Args:
            name (string): project name
            code (string): project code
            tags (list of string): searching parameter for list
            description (string): searching parameter for description
            discoverable (bool): the flag to indicate if other can see the project

        Returns:
            project detail

        Examples:
            >>> PA = ProjectApis(pilot_client)
            >>> # create project
            >>> PA.create_project(<your_project_name>, <your_project_code>)

            >>> # create private project
            >>> PA.create_project(<your_project_name>, <your_project_code>, discoverable=False)
        """
        if not tags:
            tags = []

        # validation for the array of string
        fields = {'tags': tags}
        for f_name, f_value in fields.items():
            array_of_string_vali(f_name, f_value)

        payload = {
            'name': name,
            'code': code,
            'tags': tags,
            'description': description,
            'type': 'project',
            'discoverable': discoverable,
        }

        url = ConfigClass.create_project_url
        res = self._send_request(url, method='POST', json=payload)

        return res.json().get('result', [])

    def get_project_by_geid(self, geid):
        """Function Summary: get project detail by geid.

        Args:
            geid (string): unique identifier for the project

        Returns:
            project detail

        Examples:
            >>> PA = ProjectApis(pilot_client)
            >>> # create project
            >>> res = PA.get_project_by_geid(<project_geid>)
        """

        url = ConfigClass.get_project_by_geid_url % (geid)
        res = self._send_request(url, method='GET')

        return res.json().get('result', [])
