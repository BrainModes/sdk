# Project File APIs

## client.api.ProjectFilesApis

The children class of BaseAPIClass for the project file operation

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
**list_child_entities** | **public** | file/folder nodes list | list file/folder under the target folder or project |
**copy_to_core** | **public** | file/folder nodes list | copy file/folder under project from greenroom to core zone |
**delete_entity** | **public** | deleted file/folder entity | remove the nodes by the input targets list |
**fput_file_entity** | **public** | upload local file to project | file node detail |
**fput_file_entity** | **public** | download files to local | file job detail |

## Example

```
from client.client import PILOT
from client.api.project_files import ProjectFilesApis

pilot_client = PILOT(<PILOT_backend>, <username>, <password>)
PFA = ProjectFilesApis(pilot_client)

# list all the folder/files under the project(not the grandchild)
res = PFA.list_child_entities(<project_geid>)

# list all the folder/files under the folder in project
res = PFA.list_child_entities(<project_geid>, folder_geid="<some_folder_geid>")

# list folder/files with the name query
res = PFA.list_child_entities(<project_geid>, query={"name":"<file_name>"})


PFA = ProjectFilesApis(pilot_client)
res = PFA.delete_entity("<project_geid>", targets=[{"geid":"<file_geid>"}])


# upload file under the root
PFA.fput_file_entity(<project_code>, <your_file_path>, target_path="test0913")

# upload file to some subfolder
PFA.fput_file_entity(<project_code>, <your_file_path>, target_path="test0913")

# download files from project
res = PFA.fget_file_entity(<project_code>, [<geid1>, <geid2>])

```

---
