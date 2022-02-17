# Project APIs

## client.api.ProjectApis

The children class of BaseAPIClass for the project related apis

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
**list_projects** | **public** | project list | get list of project by query |
**create_project** | **public** | new project detail | create new project |
**get_project_by_geid** | **public** | project detail | get detail project info by geid |

## Example

```
from client.client import PILOT
from client.api.projects import ProjectApis

pilot_client = PILOT(<PILOT_backend>, <username>, <password>)
PA = ProjectApis(pilot_client)

# list all project
res = PA.list_projects()
# list only first 10 project
res = PA.list_projects(page_size=10)

# create new project with name and code
res = PA.create_project(<new_name>, <new_code>)
# create private project
res = PA.create_project(<new_name>, <new_code>, discoverable=False)

# fetch the detail of the project
res = PA.get_project_by_geid(<project_geid>)


```

---
