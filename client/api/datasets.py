from client.api.base_class import BaseAPIClass
from client.model.validator import array_of_string_vali
from config import ConfigClass


class DatasetApis(BaseAPIClass):
    def list_dataset(self, order_by='time_created', order_type='desc', page=0, page_size=10, filters={}):

        """Function Summary: The function will list the dataset owned by authorized user.

        Args:
            order_by (string): possible order string:
                - "time_created": project created time
                - "name": project name
                - "code": project code
            order_type (string): increasing order(asc) or decreasing order(desc)
            page_size (int): page size for the result(eg limit)
            page (int): page number(eg. skip = page_size*page)
            filters (dict): dict of special query for the searching

        Returns:
            list of dataset detail

        Examples:
            >>> DA = DatasetApis(pilot_client)
            >>> res = DA.list_dataset()
        """

        query_params = {
            'order_by': order_by,
            'order_type': order_type,
            'page_size': page_size,
            'page': page,
            'filter': filters,
        }

        url = ConfigClass.user_dataset_url % (self.client.username)
        res = self._send_request(url, method='POST', json=query_params)

        return res.json().get('result', [])

    def create_dataset(
        self,
        title,
        code,
        description,
        type_='GENERAL',
        modality=[],
        authors=[],
        collection_method=[],
        license_='',
        tags=[],
    ):

        """Function Summary: The function will create new dataset by current authorized user.

        Args:
            title (string): project name
            code (string): project code
            description (string): searching parameter for description
            type_ (string): "GENERAL" or "BIDS",
            modality (list): modality
            authors (list): authors
            collection_method (list): collection_method,
            license_ (string): license_
            tags (list): tags

        Returns:
            new dataset detail

        Examples:
            >>> DA = DatasetApis(pilot_client)
            >>> res = DA.create_dataset(<title>, <code>, <description>)
        """

        # validation for the array of string
        fields = {'authors': authors, 'collection_method': collection_method, 'tags': tags}
        for f_name, f_value in fields.items():
            array_of_string_vali(f_name, f_value)

        url = ConfigClass.dataset_url
        create_payload = {
            'username': self.client.username,
            'title': title,
            'code': code,
            'authors': authors,
            'type': type_,
            'modality': modality,
            'collection_method': collection_method,
            'license': license_,
            'tags': tags,
            'description': description,
        }

        res = self._send_request(url, method='POST', json=create_payload)

        return res.json().get('result')
