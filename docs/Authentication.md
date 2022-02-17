# Authentication

## client.credentials.Credentials

The Credentials object will contain the access token and refresh token.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_token** | **str** | access key | immutable attribute
**refresh_token** | **str** | refresh key | [optional] immutable attribute

## Class Method

Name | Type | Return | Description | Notes
------------ | ------------- |------------- | ------------- | -------------

## Example

```
from client.credentials import Credentials

# if you only have access token
credential = Credentials(at)

# if you have access token and refresh token
credential = Credentials(at, refresh_token=rt)

```

---

## client.client.PILOT

The Authentication will send the request to the PILOT portal backend to fetch the credentials. Also the class support the optional parameter to directly use the fetched credentials.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**endpoint** | **str** | endpoint is the url point to the PILOT portal backend |
**username** | **str** | username is assigned by the system admin| [optional] if token provided
**password** | **str** | password is created by user when signup | [optional] if token provided
**token** | **Credentials** | If no username/password provided, the object will use the token credentials to do the ongoing operations. | [optional] if username/password provided

## Class Method

Name | Type | Return | Description | Notes
------------ | ------------- |------------- | ------------- | -------------
**_login** | **private** | credentials | perform the login action if username/password is provided |

## Example

```
from client.client import PILOT
from client.credentials import Credentials

# use the password authentication
pilot_client = PILOT(<PILOT_backend>, <username>, <password>)

# use the token based authentication
# some token fetching logic...
credential = Credentials(at, refresh_token=rt)
pilot_client = PILOT(<PILOT_backend>, token_crediential=credential)

```
