# Dataset APIs

## client.api.DatasetApis

The children class of BaseAPIClass for the dataset related apis

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
**list_dataset** | **public** | dataset list | get list of own dataset by query |
**create_dataset** | **public** | new dataset detail | create new dataset |

## Example

```
from client.client import PILOT
from client.api.datasets import DatasetApis

pilot_client = PILOT(<PILOT_backend>, <username>, <password>)
DA = DatasetApis(pilot_client)

# list existing dataset own by myself
res = DA.list_dataset()
# pagination
res = DA.list_dataset(page=1, page_size=10)

# create new dataset
res = DA.create_dataset("testpilotsdk09213", "testpilotsdk09213", "testpilotsdk09213")

```

---
