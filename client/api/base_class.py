import requests

from client.exceptions import BadRequest
from client.exceptions import Conflict
from client.exceptions import Forbiden
from client.exceptions import InternalServerError
from client.exceptions import NotFound
from client.exceptions import Unauthorized
from client.logger import SrvLoggerFactory


class BaseAPIClass:

    _logger = SrvLoggerFactory().get_logger()

    def __init__(self, api_client):
        """Function Summary: The base class for all apis class. It will include some common functions for api
        operations. Normally, it will be inherient by other classes.

        Args:
            api_client (PILOT): the client instance that initialize by password or token
            based authentication

        Examples:
            >>> # some login operations
            >>> api_client = PILOT(endpoint, user, pass)
            >>> BAC = BaseAPIClass(api_client)
        """
        self.client = api_client
        self.track_flag = True

    def _send_request(
        self, api_endpoint, method='GET', json={}, params={}, headers={}, data={}, cookies={}, files=None, stream=False
    ):
        """Function Summary: private function for sending the request. Since all the api will need to send with
        `Authorization` and `Refresh-token` in headers. it is a wrapper for request sending.

        Args:
            api_endpoint (string): the relative path for the api endpoints
            method (string): HTTP methods: GET, POST, DELETE, PUT
            json (dict): the payload for the api logics
            params (dict): the args for the api logics
            headers (dict): the extra headers for the api logic, by default, api will add
                two more attribute: `Authorization` and `Refresh-token`
            files (file stream): to update the file
            stream (stream): flag for return to handle the large reponse

        Examples:
            >>> # get request
            >>> self._send_request(<relative_path>)
        """

        # add the at and rt into headers if there is no provided new token in header
        if not headers.get('Authorization', None):
            headers.update({'Authorization': 'Bearer ' + self.client.token.access_token})
            headers.update({'Refresh-token': self.client.token.refresh_token})

        res = requests.request(
            method=method,
            url=self.client.base_url + api_endpoint,
            json=json,
            params=params,
            headers=headers,
            data=data,
            cookies=cookies,
            files=files,
            stream=stream,
        )

        # if we request large return eg(files) we will return it right away
        if stream:
            return res

        try:
            self._track_print('====== ')
            self._track_print('calling:', method, self.client.base_url + api_endpoint)
            self._track_print('request parameter:', params)
            self._track_print('request json payload:', json)
            self._track_print('request headers:', headers)
            self._track_print('request result:', res.json())
            self._track_print('====== ')

            # response error mapping if not 200 raise the exception
            exception_mapping = {
                400: lambda msg: BadRequest(msg),
                401: lambda msg: Unauthorized(msg),
                403: lambda msg: Forbiden(msg),
                404: lambda msg: NotFound(msg),
                409: lambda msg: Conflict(msg),
            }
            isr = lambda msg: InternalServerError

            code = res.json().get('code', 200)
            if code >= 300:
                raise exception_mapping.get(code, isr)(res.json())

        except Exception as e:
            self._logger.error(res.__dict__)
            raise e

        return res

    def track_on(self):
        """Function Summary: private function for flagging up the logger.

        Args:
            None

        Examples:
            >>> self._track_on()
        """

        self.track_flag = True

    def track_off(self):
        """Function Summary: private function for flagging down the logger.

        Args:
            None

        Examples:
            >>> self._track_off()
        """

        self.track_flag = False

    def _track_print(self, *message):
        """Function Summary: private function for conditional logger print.

        Args:
            None

        Examples:
            >>> self._track_print("message1", varibale1)
        """
        if self.track_flag:
            message = [str(m) for m in message]
            self._logger.info(' '.join(message))
