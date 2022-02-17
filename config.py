from functools import lru_cache

from pydantic import BaseSettings
from pydantic import Extra
from starlette.config import Config

config = Config('.env')


class Settings(BaseSettings):

    api_gateway: str
    hpc_endpoint: str
    socketio_endpoint: str

    def __init__(self):
        super().__init__()
        self.auth_url = '/portal/users/auth'

        # dataset related api
        self.user_dataset_url = '/portal/v1/users/%s/datasets'
        self.dataset_url = '/portal/v1/dataset'
        self.dataset_files_url = '/portal/v1/dataset/%s/files'
        self.dataset_file_ops_url = '/portal/v1/dataset/%s/files/%s'

        # file update related api
        self.pre_upload_url = '/upload/gr/v1/files/jobs'
        self.chunk_upload_url = '/upload/gr/v1/files/chunks'
        self.combine_chunk_url = '/upload/gr/v1/files'
        # TODO after update the task api change to task object
        self.upload_status_url = '/upload/gr/v1/files/jobs'

        # project related api
        self.project_file_task_url = '/portal/v1/files/actions/tasks'
        self.project_list_user_url = '/portal/v1/containers/%s/users'
        self.project_user_ops_url = '/portal/v1/containers/%s/users/%s'
        self.list_all_project_url = '/portal/v1/containers/'
        self.list_project_by_user_url = '/portal/v1/users/%s/containers'
        self.create_project_url = '/portal/v1/projects'
        self.get_project_by_geid_url = '/portal/v1/project/%s'

        # project files related api
        self.project_file_meta_url = '/portal/v1/files/entity/meta/'
        self.project_file_action_url = '/portal/v1/files/actions'

        # download related api
        self.pre_download_url = '/portal/v2/download/pre'
        self.download_status_url = '/portal/download/gr/v1/download/status/%s'
        self.download_url = '/portal/download/gr/v1/download/%s'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = Extra.allow

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return env_settings, init_settings, file_secret_settings


@lru_cache(1)
def get_settings():
    settings = Settings()
    return settings


ConfigClass = get_settings()
