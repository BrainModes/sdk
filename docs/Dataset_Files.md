# Dataset File APIs

## client.api.DatasetFilesApis

The children class of BaseAPIClass for the Dataset file operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client** | **PILOT object** | the client object init by password or token | inherent from BaseAPIClass
**track_flag** | **bool** | the boolean variable to control the detail logs | inherent from BaseAPIClass

## Class Method

Name | Type | Return | Description | Notes
------------ | ------------- |------------- | ------------- | -------------
**_send_request** | **private** | Response | wrapper function to send the request with credential header | returns request.Response | inherent from BaseAPIClass
**track_on** | **public** | None | turn on the detail logger | inherent from BaseAPIClass
**track_off** | **public** | None | turn off the detail logger | inherent from BaseAPIClass
**import_files** | **public** | list of job status | import the files from project to dataset |
**list_files** | **public** | list of file/folder node | list the child folder/file under dataset |
**delete_files** | **public** | list of job status | remove the folder/files from dataset |
**move_files** | **public** | list of job status | move the file/folder within the dataset |
**rename_file** | **public** | job status | rename a file under dataset |

## Example

```
from client.client import PILOT
from client.api.dataset_files import DatasetFileApis

DFA = DatasetFileApis(pilot_client)
# import files
res = DFA.import_files(
    dataset_geid=<dataset_geid>,
    source_project_geid=<project_geid>,
    source_list=[<file_list>])
# list files
res = DFA.list_files(<dataset_geid>)

# delete files
res = DFA.delete_files(
    dataset_geid=<dataset_geid>,
    source_list=[<file_list>])

# move files under dataset
res = DFA.move_files(
    dataset_geid=<dataset_geid>,
    source_files=[<file_list>],
    target_folder_geid=<folder_geid>)

res = DFA.rename_file(
    dataset_geid=<dataset_geid>,
    file_geid=<file_geid>,
    new_name=<new_names>)

```

---
