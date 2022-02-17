# PILOT SDK


[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg?style=for-the-badge)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.7](https://img.shields.io/badge/python-3.7-green?style=for-the-badge)](https://www.python.org/)

This is the SDK tool for python to connect with backend apis

## Installation

### Clone Repository

```
git clone https://github.com/PilotDataPlatform/sdk.git
```

### Install SDK

```
cd sdk
pip install .
```

## Usage

```
from pilot_sdk.client import PILOT

client = PILOT(end_point=<gateway_endpoint>, username=<username>, password=<password>)
```
