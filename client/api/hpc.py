from client.api.base_class import BaseAPIClass
from client.client import HPC


class HPCApis(BaseAPIClass):
    def __init__(self, api_client: HPC, slurm_host: str, protocol: str = 'http'):
        """Function Summary: The initialization for hpc componenets.

        Args:
            api_client (HPC): the object where user do the authentication first
            slurm_host (str): the http endpoint where the slurm worker node is located
            protocol (str): http or https protocol

        Returns:
            None

        Examples:
            >>> hpc_client = HPC(<slurm_host>, <hpc_service_endpoints, <username>, <password>)
            >>> hpc_api = HPCApis(hpc_client, <slurm_host>)
        """

        super().__init__(api_client)

        self.client = api_client
        self.slurm_host = slurm_host
        self.protocol = protocol

        # here customize the authorization heades since it dont have Bearer
        self.auth_header = {'Authorization': self.client.token.access_token}

    def list_nodes(self):
        """Function Summary: List the available running nodes.

        Args:
            None

        Returns:
            list of running node in json

        Examples:
            >>> res = hpc_api.list_nodes()
            >>> preint(res)
        """

        url = '/v1/hpc/nodes'
        params = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
        }
        res = self._send_request(url, method='GET', headers=self.auth_header, params=params)

        return res.json().get('result')

    def get_node_info(self, node_name):
        """Function Summary: get the information of specific running node.

        Args:
            node_name(string): the name of target node

        Returns:
            detail info of node in json

        Examples:
            >>> res = hpc_api.get_node_info("slurm-master-ubuntu2110")
            >>> preint(res)
        """

        url = '/v1/hpc/nodes/%s' % (node_name)
        params = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
        }
        res = self._send_request(url, method='GET', headers=self.auth_header, params=params)

        return res.json().get('result')

    def list_partitions(self):
        """Function Summary: List the available partitions.

        Args:
            None

        Returns:
            list of running partitions in json

        Examples:
            >>> res = hpc_api.list_partitions()
            >>> preint(res)
        """

        url = '/v1/hpc/partitions'
        params = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
        }
        res = self._send_request(url, method='GET', headers=self.auth_header, params=params)

        return res.json().get('result')

    def get_partition_info(self, partition_name):
        """Function Summary: get the information of specific running partition.

        Args:
            partition_name(string): the name of target partition

        Returns:
            detail info of partition in json

        Examples:
            >>> res = hpc_api.get_node_info("node_name")
            >>> res = hpc_api.get_partition_info("debug")
        """

        url = '/v1/hpc/partitions/%s' % (partition_name)
        params = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
        }
        res = self._send_request(url, method='GET', headers=self.auth_header, params=params)

        return res.json().get('result')

    # Job API
    def submit_job(self, job_info: dict) -> dict:
        # TODO add the class for job info

        url = '/v1/hpc/job'
        payload = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
            'job_info': job_info,
        }
        res = self._send_request(url, method='POST', headers=self.auth_header, json=payload)

        return res.json().get('result')

    def get_job_info(self, job_id: int):
        """Function Summary: fetch the job status by id.

        Args:
            job_id(int): the id of job

        Returns:
            detail info of job info in json

        Examples:
            >>> res = hpc_api.get_job_info(40)
        """

        url = '/v1/hpc/job/%s' % (job_id)
        params = {
            'username': self.client.username,
            'slurm_host': self.slurm_host,
            'protocol': self.protocol,
        }
        res = self._send_request(url, method='GET', headers=self.auth_header, params=params)

        return res.json()
