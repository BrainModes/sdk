import requests

from client.credentials import Credentials
from client.exceptions import AuthenticationError
from config import ConfigClass


class PILOT:
    def __init__(
        self, end_point=ConfigClass.api_gateway, username=None, password=None, token_crediential: Credentials = None
    ):
        """Function Summary: The PILOT class is the client object. It allow to utilize all the apis and perform the
        operation.

        Args:
            endpoint (string): the connection to PILOT server
            username (string): the username in the PILOT system you will get it from
                system admin
            password (string): couple with username
            token_crediential (Credentials): token is the another way to fulfill the
                username/password authentication if you dont want to pass the username/password
                around the system

        Examples:
            >>> # password based auth
            >>> pilot_client = PILOT(endpoint, user, pass)

            >>> # token based auth
            >>> credential = Credentials(at, refresh_token=rt)
            >>> pilot_client = PILOT(endpoint, token_crediential=credential)
        """

        if not username and not password and not token_crediential:
            raise ValueError('Either username/password or tokens is required')

        self.base_url = end_point
        self.username = username
        self.password = password

        token = self._login()
        self.token = Credentials(token['access_token'], token['refresh_token'])

        # TODO add the token based if possible

    def _login(self):
        """Function Summary: private funtion to perform the user login.

        Args:
            None

        Retruns:
            dict: Contains the access token, refresh token and other login information

        Examples:

            >>> # with in the PILOT object
            >>> token = self._login()
        """

        payload = {
            'username': self.username,
            'password': self.password,
        }
        headers = {'Content-Type': 'application/json'}
        # TODO how they manage the api endpoints?????
        response = requests.post(self.base_url + ConfigClass.auth_url, json=payload, headers=headers)
        # print(response.json())

        # parse the token if return 200 else raise the error
        if response.status_code != 200:
            raise AuthenticationError('Failed to login. ' + str(response.json()))

        return response.json()['result']


class HPC:
    def __init__(
        self,
        token_issuer,
        end_point=ConfigClass.hpc_endpoint,
        username=None,
        password=None,
        token_crediential: Credentials = None,
    ):
        """Function Summary: The HPC class is the client object. It will perform login into hpc to fecth the token or
        store the existing token.

        Args:
            endpoint (string): the connection to PILOT server
            username (string): the username in the PILOT system you will get it from
                system admin
            password (string): couple with username
            token_crediential (Credentials): token is the another way to fulfill the
                username/password authentication if you dont want to pass the username/password
                around the system

        Examples:
            >>> # password based auth
            >>> hpc_client = HPC(endpoint, user, pass)

            >>> # token based auth
            >>> credential = Credentials(at)
            >>> hpc_client = HPC(endpoint, token_crediential=credential)
        """

        if not username and not password and not token_crediential:
            raise ValueError('Either username/password or tokens is required')

        self.base_url = end_point
        self.username = username
        self.password = password
        self.token_issuer = token_issuer

        token = self._login()
        self.token = Credentials(token)

        # TODO add the token based if possible

    def _login(self):
        """Function Summary: private funtion to perform the user login.

        Args:
            None

        Retruns:
            dict: Contains the access token, refresh token and other login information

        Examples:

            >>> # with in the PILOT object
            >>> token = self._login()
        """

        payload = {
            'username': self.username,
            'password': self.password,
            'token_issuer': self.token_issuer,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.base_url + '/v1/hpc/auth', json=payload, headers=headers)

        # parse the token if return 200 else raise the error
        if response.status_code != 200:
            raise AuthenticationError('Failed to login. ' + str(response.json()))

        return response.json()['result']
