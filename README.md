## What to solve?

NACOS is a great framework for service discovery. But the vanilla sdk
lacks logic to self-register python service.

This package seeks to simplify the setup of a NACOS-compatible python service

## Install 

```
python3 -m pip install https://github.com/shouldsee/nacos_pyext/tarball/master
```

## Example

```python
from nacos_pyext import NacosClientService
import os
__version__='v0.0.1'
x = NacosClientService(os.environ['NACOS_URL'],
    os.environ['NACOS_SERVICE_NAME'],
    os.environ['NACOS_SERVICE_IP'],
    int(os.environ['NACOS_SERVICE_PORT']),
    ephemeral=True,
    )
x.start_register_thread(metadata={'version':__version__,'app_name':'my_app'})
x.start_heartbeat_thread()    
```
