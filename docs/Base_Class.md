# Base Class

## client.api.BaseAPIClass

The base class contains some private functions for the API class inherent

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client** | **PILOT object** | the client object init by password or token |
**track_flag** | **bool** | the boolean variable to control the detail logs |

## Class Method

Name | Type | Return | Description | Notes
------------ | ------------- |------------- | ------------- | -------------
**_send_request** | **private** | Response | wrapper function to send the request with credential header | returns request.Response
**track_on** | **public** | None | turn on the detail logger |
**track_off** | **public** | None | turn off the detail logger |

## Example

```
from client.client import PILOT

pilot_client = PILOT(<PILOT_backend>, <username>, <password>)
ba = BaseAPIClass(pilot_client)

# if you have access token and refresh token
ba._send_request(<url>, method="POST", json={})

# turn on/off the tracker
ba.track_on()
ba.track_off()

```

---
